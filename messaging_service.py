"""
Messaging Service - Claude AI Integration for SMS/WhatsApp
Handles incoming messages via Twilio and responds using Claude API
"""

import os
import anthropic
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from models import db, Job, Lead, Estimate, User
from datetime import datetime
from sqlalchemy import desc


class ClaudeMessagingService:
    """Service to handle messaging via Claude AI"""

    def __init__(self):
        self.anthropic_api_key = os.environ.get('ANTHROPIC_API_KEY')
        self.twilio_account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
        self.twilio_auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
        self.twilio_phone = os.environ.get('TWILIO_PHONE_NUMBER')

        # Initialize clients
        if self.anthropic_api_key:
            self.claude_client = anthropic.Anthropic(api_key=self.anthropic_api_key)
        else:
            self.claude_client = None

        if self.twilio_account_sid and self.twilio_auth_token:
            self.twilio_client = Client(self.twilio_account_sid, self.twilio_auth_token)
        else:
            self.twilio_client = None

    def get_contractorpro_context(self, user_id=None):
        """Get context about ContractorPro jobs, leads, and estimates"""
        context_parts = []

        try:
            # Get user context
            if user_id:
                user = User.query.get(user_id)
                if user:
                    context_parts.append(f"Company: {user.company_name}")

            # Get recent jobs
            jobs_query = Job.query
            if user_id:
                jobs_query = jobs_query.filter_by(user_id=user_id)

            recent_jobs = jobs_query.order_by(desc(Job.created_at)).limit(5).all()
            if recent_jobs:
                context_parts.append("\n📋 Recent Jobs:")
                for job in recent_jobs:
                    context_parts.append(
                        f"  - {job.title} ({job.status}) - Client: {job.client_name} - ${job.budget or 0:,.2f}"
                    )

            # Get recent leads
            leads_query = Lead.query
            if user_id:
                leads_query = leads_query.filter_by(user_id=user_id)

            recent_leads = leads_query.order_by(desc(Lead.created_at)).limit(5).all()
            if recent_leads:
                context_parts.append("\n🎯 Recent Leads:")
                for lead in recent_leads:
                    context_parts.append(
                        f"  - {lead.name} ({lead.status}) - {lead.project_type} - {lead.phone}"
                    )

            # Get pending estimates
            estimates_query = Estimate.query.filter_by(status='pending')
            if user_id:
                estimates_query = estimates_query.filter_by(user_id=user_id)

            pending_estimates = estimates_query.order_by(desc(Estimate.created_at)).limit(5).all()
            if pending_estimates:
                context_parts.append("\n💰 Pending Estimates:")
                for est in pending_estimates:
                    job = Job.query.get(est.job_id) if est.job_id else None
                    client = job.client_name if job else "Unknown"
                    context_parts.append(
                        f"  - {client} - ${est.total_amount:,.2f} - Created: {est.created_at.strftime('%Y-%m-%d')}"
                    )

            return "\n".join(context_parts) if context_parts else "No recent activity found."

        except Exception as e:
            return f"Error loading context: {str(e)}"

    def process_command(self, message, user_id=None):
        """Process special commands for ContractorPro data"""
        message_lower = message.lower().strip()

        # Quick command shortcuts
        if message_lower in ['jobs', 'show jobs', 'list jobs']:
            return self._format_jobs(user_id)

        elif message_lower in ['leads', 'show leads', 'list leads']:
            return self._format_leads(user_id)

        elif message_lower in ['estimates', 'show estimates', 'pending estimates']:
            return self._format_estimates(user_id)

        elif message_lower.startswith('job status'):
            # Extract job ID or name
            return self._get_job_status(message, user_id)

        elif message_lower in ['help', 'commands']:
            return self._get_help_message()

        return None  # No command matched

    def _format_jobs(self, user_id=None):
        """Format job list for text message"""
        query = Job.query
        if user_id:
            query = query.filter_by(user_id=user_id)

        jobs = query.order_by(desc(Job.created_at)).limit(10).all()

        if not jobs:
            return "No jobs found."

        response = "📋 Your Jobs:\n"
        for i, job in enumerate(jobs, 1):
            response += f"\n{i}. {job.title}\n"
            response += f"   Client: {job.client_name}\n"
            response += f"   Status: {job.status}\n"
            response += f"   Budget: ${job.budget or 0:,.2f}\n"

        return response

    def _format_leads(self, user_id=None):
        """Format lead list for text message"""
        query = Lead.query
        if user_id:
            query = query.filter_by(user_id=user_id)

        leads = query.order_by(desc(Lead.created_at)).limit(10).all()

        if not leads:
            return "No leads found."

        response = "🎯 Your Leads:\n"
        for i, lead in enumerate(leads, 1):
            response += f"\n{i}. {lead.name}\n"
            response += f"   Status: {lead.status}\n"
            response += f"   Project: {lead.project_type}\n"
            response += f"   Phone: {lead.phone}\n"

        return response

    def _format_estimates(self, user_id=None):
        """Format estimate list for text message"""
        query = Estimate.query
        if user_id:
            query = query.filter_by(user_id=user_id)

        estimates = query.order_by(desc(Estimate.created_at)).limit(10).all()

        if not estimates:
            return "No estimates found."

        response = "💰 Your Estimates:\n"
        for i, est in enumerate(estimates, 1):
            job = Job.query.get(est.job_id) if est.job_id else None
            client = job.client_name if job else "Unknown"
            response += f"\n{i}. {client}\n"
            response += f"   Amount: ${est.total_amount:,.2f}\n"
            response += f"   Status: {est.status}\n"
            response += f"   Date: {est.created_at.strftime('%Y-%m-%d')}\n"

        return response

    def _get_job_status(self, message, user_id=None):
        """Get specific job status"""
        # Simple implementation - can be enhanced
        return "Please specify the job name or ID after 'job status'"

    def _get_help_message(self):
        """Return help message with available commands"""
        return """🤖 ContractorPro AI Assistant

Quick Commands:
• jobs - List recent jobs
• leads - List recent leads
• estimates - List estimates
• help - Show this message

Or just ask me anything!
I can answer questions about your projects, provide business insights, or help with construction-related queries."""

    def get_claude_response(self, user_message, user_id=None, include_context=True):
        """Get response from Claude AI"""

        if not self.claude_client:
            return "Claude AI is not configured. Please add ANTHROPIC_API_KEY to your environment."

        # Check for quick commands first
        command_response = self.process_command(user_message, user_id)
        if command_response:
            return command_response

        # Build context for Claude
        system_message = """You are a helpful AI assistant integrated with ContractorPro,
a construction business management platform. You help contractors manage their jobs,
leads, estimates, and business operations via text message.

Keep responses concise and suitable for SMS/WhatsApp (under 1600 characters when possible).
Be professional but friendly. Focus on actionable insights."""

        # Add ContractorPro data context if requested
        if include_context:
            context_data = self.get_contractorpro_context(user_id)
            system_message += f"\n\nCurrent business data:\n{context_data}"

        try:
            # Call Claude API
            message = self.claude_client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1024,
                system=system_message,
                messages=[
                    {"role": "user", "content": user_message}
                ]
            )

            # Extract response
            response_text = message.content[0].text

            # Truncate if too long for SMS (1600 char limit)
            if len(response_text) > 1500:
                response_text = response_text[:1497] + "..."

            return response_text

        except Exception as e:
            return f"Error getting AI response: {str(e)}"

    def handle_incoming_message(self, from_number, message_body, user_id=None):
        """Handle incoming SMS/WhatsApp message and return response"""

        # Get Claude's response
        response = self.get_claude_response(message_body, user_id, include_context=True)

        # Create TwiML response
        twiml_response = MessagingResponse()
        twiml_response.message(response)

        return str(twiml_response)

    def send_outbound_message(self, to_number, message_body):
        """Send outbound SMS/WhatsApp message"""

        if not self.twilio_client:
            return {"success": False, "error": "Twilio is not configured"}

        try:
            message = self.twilio_client.messages.create(
                body=message_body,
                from_=self.twilio_phone,
                to=to_number
            )

            return {
                "success": True,
                "message_sid": message.sid,
                "status": message.status
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


# Singleton instance
messaging_service = ClaudeMessagingService()
