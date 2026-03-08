"""
LLM Service for intelligent scope analysis and contract generation.
This module handles all LLM interactions for analyzing project scopes and generating contracts.
"""

import json
import re
import os
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta

# Try to import OpenAI
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

class LLMService:
    """
    Service class for LLM-powered analysis and generation.
    This implementation uses rule-based logic as a fallback/demo.
    In production, replace with actual LLM API calls.
    """

    def __init__(self):
        self.project_templates = self._load_project_templates()
        self.task_templates = self._load_task_templates()
        self.contract_template = self._load_contract_template()
        self.pos_category_mapping = self._load_pos_category_mapping()

        # Initialize OpenAI if available and API key is set
        self.use_openai = False
        if OPENAI_AVAILABLE:
            api_key = os.getenv('OPENAI_API_KEY')
            if api_key:
                openai.api_key = api_key
                self.use_openai = True
                print("[OK] OpenAI integration enabled")
            else:
                print("[WARNING] OpenAI available but no API key found. Set OPENAI_API_KEY environment variable.")
        else:
            print("[INFO] OpenAI not installed. Using rule-based analysis. Install with: pip install openai")

    def analyze_scope(self, raw_scope: str) -> Dict:
        """
        Analyze raw scope text and extract structured information.

        Args:
            raw_scope: The original scope of work text

        Returns:
            Dictionary containing analyzed scope information
        """

        if self.use_openai:
            return self._analyze_scope_with_openai(raw_scope)
        else:
            return self._analyze_scope_rule_based(raw_scope)

    def _analyze_scope_with_openai(self, raw_scope: str) -> Dict:
        """Analyze scope using OpenAI API"""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{
                    "role": "system",
                    "content": """You are an expert construction project analyst. Analyze the scope of work and return a JSON response with:
                    {
                        "project_type": "specific project type",
                        "locations_identified": ["list", "of", "locations"],
                        "work_items": ["list", "of", "work", "items"],
                        "materials_needed": ["list", "of", "materials"],
                        "special_requirements": ["any", "special", "requirements"],
                        "complexity_score": 1-5,
                        "estimated_timeline": number_of_days,
                        "risk_factors": ["potential", "risks"]
                    }
                    Be specific and accurate."""
                }, {
                    "role": "user",
                    "content": f"Analyze this construction scope of work: {raw_scope}"
                }],
                temperature=0.3
            )

            # Parse the JSON response
            content = response.choices[0].message.content
            try:
                analysis_data = json.loads(content)
            except json.JSONDecodeError:
                # Fallback to rule-based if JSON parsing fails
                print("[WARNING] OpenAI response not valid JSON, falling back to rule-based")
                return self._analyze_scope_rule_based(raw_scope)

            # Add metadata
            analysis_data.update({
                'llm_processed': True,
                'analysis_complete': True
            })

            return analysis_data

        except Exception as e:
            print(f"[WARNING] OpenAI API error: {e}, falling back to rule-based")
            return self._analyze_scope_rule_based(raw_scope)

    def _analyze_scope_rule_based(self, raw_scope: str) -> Dict:
        """Fallback rule-based analysis"""
        analysis = {
            'project_type': self._extract_project_type(raw_scope),
            'locations_identified': self._extract_locations(raw_scope),
            'work_items': self._extract_work_items(raw_scope),
            'materials_needed': self._extract_materials(raw_scope),
            'special_requirements': self._extract_special_requirements(raw_scope),
            'complexity_score': self._calculate_complexity(raw_scope),
            'estimated_timeline': self._estimate_timeline(raw_scope),
            'risk_factors': self._identify_risks(raw_scope),
            'llm_processed': False,
            'analysis_complete': True
        }

        return analysis

    def generate_contract(self, project_data: Dict, analysis_data: Dict, pos_quotes: Optional[List] = None) -> Dict:
        """
        Generate a professional contract using LLM and POS data.

        Args:
            project_data: Project information (name, client, budget, etc.)
            analysis_data: Analyzed scope information
            pos_quotes: List of POSQuote objects (optional) for detailed scope generation

        Returns:
            Dictionary containing contract sections and metadata
        """

        # Extract POS line items if quotes provided
        pos_data = self._extract_pos_data(pos_quotes) if pos_quotes else None

        # Create comprehensive context for contract generation
        context = self._build_contract_context(project_data, analysis_data, pos_data)

        # In production, this would be an LLM API call:
        # contract_response = openai.chat.completions.create(
        #     model="gpt-4",
        #     messages=[{
        #         "role": "system",
        #         "content": self._get_contract_system_prompt()
        #     }, {
        #         "role": "user",
        #         "content": f"Generate a professional construction contract for: {context}"
        #     }]
        # )

        # For now, using template-based generation with intelligent customization
        contract = {
            'contract_text': self._generate_contract_text(context),
            'introduction': self._generate_introduction(context),
            'scope_section': self._generate_scope_section(context),
            'timeline_section': self._generate_timeline_section(context),
            'payment_terms': self._generate_payment_terms(context),
            'terms_conditions': self._generate_terms_conditions(context),
            'signatures_section': self._generate_signatures_section(context),
            'total_value': project_data.get('budget_estimate'),
            'payment_schedule': self._generate_payment_schedule(context),
            'llm_model_used': 'rule-based-v1',  # Would be 'gpt-4' in production
            'generation_prompt': 'Contract generation prompt',
            'generation_quality_score': 4
        }

        return contract

    def generate_task_list(self, project_data: Dict, analysis_data: Dict, preferred_start_date=None) -> List[Dict]:
        """
        Generate detailed task list with timeline using LLM.

        Args:
            project_data: Project information
            analysis_data: Analyzed scope information

        Returns:
            List of task dictionaries
        """

        project_type = analysis_data.get('project_type', 'general renovation')
        complexity = analysis_data.get('complexity_score', 3)
        locations = analysis_data.get('locations_identified', [])

        # Get base template
        base_tasks = self._get_task_template(project_type)

        # Customize based on analysis
        customized_tasks = self._customize_tasks(base_tasks, analysis_data)

        # Add timing and dependencies with user preferences
        scheduled_tasks = self._schedule_tasks(customized_tasks, complexity, preferred_start_date)

        return scheduled_tasks

    def _extract_project_type(self, scope: str) -> str:
        """Extract project type from scope text"""
        scope_lower = scope.lower()

        project_indicators = {
            'kitchen renovation': ['kitchen', 'cabinet', 'countertop', 'appliance', 'cook'],
            'bathroom remodel': ['bathroom', 'bath', 'shower', 'toilet', 'vanity', 'tub'],
            'home addition': ['addition', 'extend', 'expand', 'add room', 'square footage'],
            'roofing project': ['roof', 'shingle', 'gutter', 'flashing', 'leak'],
            'flooring installation': ['floor', 'carpet', 'hardwood', 'tile', 'laminate'],
            'interior painting': ['paint', 'color', 'primer', 'wall', 'ceiling'],
            'plumbing renovation': ['plumb', 'pipe', 'water', 'drain', 'faucet'],
            'electrical upgrade': ['electric', 'wire', 'outlet', 'switch', 'circuit'],
            'basement finishing': ['basement', 'finish', 'recreation', 'family room'],
            'deck construction': ['deck', 'patio', 'outdoor', 'railing', 'pergola']
        }

        detected_types = []
        for proj_type, keywords in project_indicators.items():
            if any(keyword in scope_lower for keyword in keywords):
                detected_types.append(proj_type)

        return ', '.join(detected_types) if detected_types else 'general renovation'

    def _extract_locations(self, scope: str) -> List[str]:
        """Extract locations mentioned in scope"""
        scope_lower = scope.lower()

        locations = {
            'Kitchen': ['kitchen', 'cook'],
            'Master Bathroom': ['master bath', 'main bath'],
            'Bathroom': ['bathroom', 'bath', 'powder room'],
            'Living Room': ['living room', 'family room', 'great room'],
            'Bedroom': ['bedroom', 'master bedroom', 'guest room'],
            'Basement': ['basement', 'lower level'],
            'Attic': ['attic', 'upper level', 'loft'],
            'Garage': ['garage', 'carport'],
            'Laundry Room': ['laundry', 'utility room'],
            'Dining Room': ['dining room', 'dining'],
            'Office': ['office', 'study', 'den'],
            'Entryway': ['entryway', 'foyer', 'entrance'],
            'Exterior': ['exterior', 'outside', 'siding', 'roof']
        }

        detected_locations = []
        for location, keywords in locations.items():
            if any(keyword in scope_lower for keyword in keywords):
                detected_locations.append(location)

        return detected_locations

    def _extract_work_items(self, scope: str) -> List[str]:
        """Extract specific work items from scope"""

        # Common construction verbs and their patterns
        work_patterns = [
            (r'install\s+([^.]+)', 'Install'),
            (r'replace\s+([^.]+)', 'Replace'),
            (r'repair\s+([^.]+)', 'Repair'),
            (r'remove\s+([^.]+)', 'Remove'),
            (r'paint\s+([^.]+)', 'Paint'),
            (r'build\s+([^.]+)', 'Build'),
            (r'renovate\s+([^.]+)', 'Renovate'),
            (r'update\s+([^.]+)', 'Update'),
            (r'remodel\s+([^.]+)', 'Remodel'),
            (r'add\s+([^.]+)', 'Add'),
            (r'construct\s+([^.]+)', 'Construct')
        ]

        work_items = []
        scope_lower = scope.lower()

        for pattern, action in work_patterns:
            matches = re.findall(pattern, scope_lower, re.IGNORECASE)
            for match in matches:
                item = f"{action} {match.strip()}"
                if len(item) < 100:  # Avoid overly long matches
                    work_items.append(item)

        return work_items

    def _extract_materials(self, scope: str) -> List[str]:
        """Extract materials mentioned in scope"""
        scope_lower = scope.lower()

        materials = [
            'cabinets', 'countertops', 'appliances', 'tiles', 'hardwood',
            'carpet', 'paint', 'fixtures', 'outlets', 'switches', 'pipes',
            'faucets', 'vanity', 'toilet', 'shower', 'tub', 'drywall',
            'insulation', 'flooring', 'trim', 'doors', 'windows'
        ]

        detected_materials = []
        for material in materials:
            if material in scope_lower:
                detected_materials.append(material.title())

        return detected_materials

    def _extract_special_requirements(self, scope: str) -> List[str]:
        """Extract special requirements or considerations"""
        scope_lower = scope.lower()

        requirements = []

        # Permit requirements
        if any(word in scope_lower for word in ['permit', 'code', 'inspection']):
            requirements.append('Building permits may be required')

        # Electrical work
        if any(word in scope_lower for word in ['electrical', 'wire', 'circuit']):
            requirements.append('Licensed electrician required')

        # Plumbing work
        if any(word in scope_lower for word in ['plumbing', 'pipe', 'water']):
            requirements.append('Licensed plumber required')

        # Structural work
        if any(word in scope_lower for word in ['structural', 'beam', 'load bearing']):
            requirements.append('Structural engineer consultation required')

        # HVAC work
        if any(word in scope_lower for word in ['hvac', 'heating', 'cooling', 'duct']):
            requirements.append('HVAC professional required')

        return requirements

    def _calculate_complexity(self, scope: str) -> int:
        """Calculate project complexity on 1-5 scale"""
        scope_lower = scope.lower()

        complexity_indicators = {
            5: ['structural', 'addition', 'new construction', 'gut renovation'],
            4: ['major renovation', 'move wall', 'rewire', 'replumb'],
            3: ['remodel', 'renovation', 'multiple rooms'],
            2: ['replace', 'install', 'update'],
            1: ['paint', 'repair', 'touch up', 'minor']
        }

        max_complexity = 1
        for level, keywords in complexity_indicators.items():
            if any(keyword in scope_lower for keyword in keywords):
                max_complexity = max(max_complexity, level)

        return max_complexity

    def _estimate_timeline(self, scope: str) -> int:
        """Estimate project timeline in days"""
        complexity = self._calculate_complexity(scope)
        work_items = len(self._extract_work_items(scope))

        base_timeline = {1: 3, 2: 7, 3: 14, 4: 30, 5: 60}

        return base_timeline[complexity] + (work_items * 2)

    def _identify_risks(self, scope: str) -> List[str]:
        """Identify potential project risks"""
        scope_lower = scope.lower()

        risks = []

        if 'old' in scope_lower or 'existing' in scope_lower:
            risks.append('Potential asbestos/lead paint in older materials')

        if any(word in scope_lower for word in ['electrical', 'wire']):
            risks.append('Electrical code compliance required')

        if any(word in scope_lower for word in ['plumbing', 'water']):
            risks.append('Potential water damage if leaks occur')

        if 'structural' in scope_lower:
            risks.append('Structural integrity must be maintained')

        if any(word in scope_lower for word in ['winter', 'cold', 'snow']):
            risks.append('Weather delays possible during winter months')

        return risks

    def _load_project_templates(self) -> Dict:
        """Load project-specific templates"""
        return {
            'kitchen': {
                'standard_timeline': 14,
                'required_permits': ['building', 'electrical', 'plumbing'],
                'common_materials': ['cabinets', 'countertops', 'appliances']
            },
            'bathroom': {
                'standard_timeline': 10,
                'required_permits': ['building', 'plumbing'],
                'common_materials': ['tiles', 'fixtures', 'vanity']
            }
        }

    def _load_task_templates(self) -> Dict:
        """Load task templates for different project types"""
        return {
            'kitchen renovation': [
                {'name': 'Design and Planning', 'days': 3, 'category': 'planning'},
                {'name': 'Obtain Permits', 'days': 5, 'category': 'administrative'},
                {'name': 'Demolition', 'days': 2, 'category': 'demolition'},
                {'name': 'Rough Electrical Work', 'days': 2, 'category': 'electrical'},
                {'name': 'Rough Plumbing Work', 'days': 3, 'category': 'plumbing'},
                {'name': 'Drywall and Painting', 'days': 4, 'category': 'finishing'},
                {'name': 'Flooring Installation', 'days': 3, 'category': 'flooring'},
                {'name': 'Cabinet Installation', 'days': 3, 'category': 'cabinets'},
                {'name': 'Countertop Installation', 'days': 1, 'category': 'countertops'},
                {'name': 'Appliance Installation', 'days': 1, 'category': 'appliances'},
                {'name': 'Final Electrical and Plumbing', 'days': 2, 'category': 'finish_utilities'},
                {'name': 'Final Inspection and Cleanup', 'days': 1, 'category': 'completion'}
            ],
            'bathroom remodel': [
                {'name': 'Design and Planning', 'days': 2, 'category': 'planning'},
                {'name': 'Obtain Permits', 'days': 3, 'category': 'administrative'},
                {'name': 'Demolition', 'days': 1, 'category': 'demolition'},
                {'name': 'Rough Plumbing', 'days': 2, 'category': 'plumbing'},
                {'name': 'Rough Electrical', 'days': 1, 'category': 'electrical'},
                {'name': 'Waterproofing', 'days': 1, 'category': 'waterproofing'},
                {'name': 'Tile Installation', 'days': 3, 'category': 'tiling'},
                {'name': 'Fixture Installation', 'days': 2, 'category': 'fixtures'},
                {'name': 'Final Plumbing and Electrical', 'days': 1, 'category': 'finish_utilities'},
                {'name': 'Final Inspection', 'days': 1, 'category': 'completion'}
            ],
            'general renovation': [
                {'name': 'Project Planning', 'days': 3, 'category': 'planning'},
                {'name': 'Permits and Approvals', 'days': 5, 'category': 'administrative'},
                {'name': 'Demolition Work', 'days': 3, 'category': 'demolition'},
                {'name': 'Structural Work', 'days': 5, 'category': 'structural'},
                {'name': 'Electrical Rough-in', 'days': 3, 'category': 'electrical'},
                {'name': 'Plumbing Rough-in', 'days': 3, 'category': 'plumbing'},
                {'name': 'Insulation and Drywall', 'days': 5, 'category': 'insulation'},
                {'name': 'Flooring Installation', 'days': 4, 'category': 'flooring'},
                {'name': 'Interior Painting', 'days': 3, 'category': 'painting'},
                {'name': 'Trim and Finish Work', 'days': 3, 'category': 'trim'},
                {'name': 'Final Utilities', 'days': 2, 'category': 'finish_utilities'},
                {'name': 'Final Inspection and Cleanup', 'days': 1, 'category': 'completion'}
            ]
        }

    def _build_contract_context(self, project_data: Dict, analysis_data: Dict, pos_data: Optional[Dict] = None) -> Dict:
        """Build context for contract generation with POS integration"""
        budget_estimate = project_data.get('budget_estimate')
        budget_value = float(budget_estimate) if budget_estimate else 0

        # If POS data exists, use it for budget
        if pos_data and pos_data.get('total_amount'):
            budget_value = float(pos_data['total_amount'])

        context = {
            'project_name': project_data.get('name', 'Renovation Project'),
            'client_name': project_data.get('client_name', 'Client'),
            'project_type': analysis_data.get('project_type', 'General Renovation'),
            'locations': analysis_data.get('locations_identified', []),
            'work_items': analysis_data.get('work_items', []),
            'timeline': analysis_data.get('estimated_timeline', 30),
            'complexity': analysis_data.get('complexity_score', 3),
            'budget': budget_value,
            'special_requirements': analysis_data.get('special_requirements', []),
            'raw_scope': project_data.get('raw_scope', ''),
            'pos_data': pos_data  # Add POS data to context
        }

        return context

    def _generate_contract_text(self, context: Dict) -> str:
        """Generate complete contract text using template"""

        # Use the loaded template and fill in placeholders
        contract_text = self.contract_template

        # Replace placeholders with actual values
        replacements = {
            '[CONTRACT_NUMBER]': f"CON-{datetime.now().strftime('%Y%m%d')}-{context.get('project_name', 'PROJECT')[:6].upper()}",
            '[CONTRACT_DATE]': datetime.now().strftime('%B %d, %Y'),
            '[CONTRACTOR_NAME]': '[Your Company Name]',
            '[CLIENT_NAME]': context.get('client_name', 'Client Name'),
            '[PROJECT_ADDRESS]': '[Project Address - To Be Specified]',
            '[PROJECT_TYPE]': context.get('project_type', 'General Renovation'),
            '[TOTAL_VALUE]': f"${context.get('budget', 0):,.2f}" if context.get('budget') else '[To Be Determined]',

            # Project-specific sections
            '[PROJECT_OBJECTIVES]': self._generate_project_objectives(context),
            '[DETAILED_SCOPE_OF_WORK]': self._generate_detailed_scope_of_work(context),
            '[DEMOLITION_WORK]': self._generate_demolition_scope(context),
            '[STRUCTURAL_WORK]': self._generate_structural_scope(context),
            '[ELECTRICAL_WORK]': self._generate_electrical_scope(context),
            '[PLUMBING_WORK]': self._generate_plumbing_scope(context),
            '[HVAC_WORK]': self._generate_hvac_scope(context),
            '[MILLWORK_DETAILS]': self._generate_millwork_scope(context),
            '[COUNTERTOP_TILE_WORK]': self._generate_countertop_tile_scope(context),
            '[FLOORING_PAINT_WORK]': self._generate_flooring_paint_scope(context),
            '[EXTERIOR_WORK]': self._generate_exterior_scope(context),
            '[ADDITIONAL_EXCLUSIONS]': self._generate_exclusions(context),
            '[ALLOWANCES_LIST]': self._generate_allowances(context),
            '[UNIT_PRICES]': self._generate_unit_prices(context),
            '[PROJECT_TIMELINE]': self._generate_project_timeline(context),

            # Payment terms
            '[PAYMENT_MILESTONE_1]': 'Contract Signing & Permits',
            '[AMOUNT_1]': f"${float(context.get('budget', 0)) * 0.20:,.2f}" if context.get('budget') else '[TBD]',
            '[PERCENTAGE_1]': '20',
            '[PAYMENT_MILESTONE_2]': 'Rough Work Complete',
            '[AMOUNT_2]': f"${float(context.get('budget', 0)) * 0.30:,.2f}" if context.get('budget') else '[TBD]',
            '[PERCENTAGE_2]': '30',
            '[PAYMENT_MILESTONE_3]': 'Substantial Completion',
            '[AMOUNT_3]': f"${float(context.get('budget', 0)) * 0.30:,.2f}" if context.get('budget') else '[TBD]',
            '[PERCENTAGE_3]': '30',
            '[PAYMENT_MILESTONE_4]': 'Final Completion',
            '[AMOUNT_4]': f"${float(context.get('budget', 0)) * 0.20:,.2f}" if context.get('budget') else '[TBD]',
            '[PERCENTAGE_4]': '20',
            '[PAYMENT_TERMS]': '10',
            '[INSURANCE_AMOUNT]': '1,000,000',
            '[WARRANTY_PERIOD]': '1 year',
            '[STATE]': '[Your State]'
        }

        # Replace all placeholders
        for placeholder, value in replacements.items():
            contract_text = contract_text.replace(placeholder, str(value))

        return contract_text

    def _format_materials_for_contract(self, context: Dict) -> str:
        """Format materials list for contract"""
        materials = context.get('materials_needed', [])
        if not materials:
            return 'Materials to be specified during project planning'

        formatted = []
        for material in materials[:5]:  # Limit to top 5
            formatted.append(f"• {material}")

        if len(materials) > 5:
            formatted.append(f"• And {len(materials) - 5} additional material types")

        return '\n'.join(formatted)

    def _generate_introduction(self, context: Dict) -> str:
        """Generate contract introduction"""
        return f"""CONSTRUCTION CONTRACT

Project: {context['project_name']}
Client: {context['client_name']}
Contractor: [Your Company Name]
Project Type: {context['project_type']}
Date: {datetime.now().strftime('%B %d, %Y')}

This agreement is entered into between the above-named Contractor and Client for the completion of construction work as detailed below."""

    def _generate_scope_section(self, context: Dict) -> str:
        """Generate comprehensive scope of work section with POS details"""
        locations_text = ', '.join(context['locations']) if context['locations'] else 'Various areas'

        scope = f"""SCOPE OF WORK:

==============================================================================
PROJECT OVERVIEW
==============================================================================

Project Description:
{context['raw_scope']}

Work Location(s): {locations_text}

Project Type: {context.get('project_type', 'General Construction')}
Estimated Timeline: {context.get('timeline', 'TBD')} days
Total Contract Value: ${context.get('budget', 0):,.2f}

==============================================================================
DETAILED SCOPE OF WORK BY CATEGORY
==============================================================================
"""

        # Add POS quote detailed breakdown if available
        if context.get('pos_data'):
            pos_data = context['pos_data']
            line_items_by_category = pos_data.get('line_items_by_category', {})

            # Group items by category and activity
            for category_name, items in line_items_by_category.items():
                scope += f"\n{'='*78}\n"
                scope += f"{category_name.upper()}\n"
                scope += f"{'='*78}\n\n"

                # Group items by activity within this category
                items_by_activity = {}
                for item in items:
                    activity = item.get('activity', 'General Work')
                    if activity not in items_by_activity:
                        items_by_activity[activity] = []
                    items_by_activity[activity].append(item)

                # Display items grouped by activity
                for activity_name, activity_items in items_by_activity.items():
                    scope += f"  {activity_name}:\n"
                    scope += f"  {'-'*74}\n"

                    for item in activity_items:
                        item_name = item.get('description', item.get('category', 'Item'))
                        qty = item.get('quantity', 1)
                        unit = item.get('unit', 'ea')
                        unit_price = item.get('unit_price', 0)
                        total = item.get('total', 0)

                        scope += f"    • {item_name}\n"
                        scope += f"      Quantity: {qty} {unit} @ ${unit_price:,.2f} per {unit}\n"
                        scope += f"      Line Total: ${total:,.2f}\n"

                    scope += "\n"

        # Add general work items if no POS data
        else:
            scope += "\nGeneral Work Items:\n"
            scope += "="*78 + "\n\n"
            for item in context['work_items'][:20]:  # Increased from 10 to 20
                scope += f"  • {item}\n"

        # Add materials and specifications
        scope += f"\n{'='*78}\n"
        scope += "MATERIALS & SPECIFICATIONS\n"
        scope += f"{'='*78}\n\n"
        scope += """All materials shall be:
  • New, first-quality materials from reputable manufacturers
  • Installed in accordance with manufacturer's specifications
  • Meet or exceed all applicable building codes and standards
  • Subject to contractor selection unless specifically designated by client
  • Guaranteed for quality and merchantability

All work shall be:
  • Performed in a workmanlike manner by qualified tradespeople
  • In compliance with all applicable building codes and regulations
  • Subject to inspection and approval by local building authorities
  • Warranted for one (1) year from date of substantial completion
"""

        if context['special_requirements']:
            scope += f"\n{'='*78}\n"
            scope += "SPECIAL REQUIREMENTS & SPECIFICATIONS\n"
            scope += f"{'='*78}\n\n"
            for req in context['special_requirements']:
                scope += f"  • {req}\n"

        # Add exclusions section
        scope += f"\n{'='*78}\n"
        scope += "EXCLUSIONS (NOT INCLUDED IN THIS CONTRACT)\n"
        scope += f"{'='*78}\n\n"
        scope += """The following items are specifically EXCLUDED from this contract unless
otherwise noted in writing:
  • Appliances (unless specified in line items above)
  • Furniture and window treatments
  • Landscaping and hardscaping (except as necessary for access)
  • Existing structure repairs not directly related to scope of work
  • Modifications required for concealed conditions discovered during work
  • Utility service upgrades required by utility company
  • Architectural or engineering design services
  • Homeowner association fees or approval processes
  • Deep cleaning or professional cleaning services
  • Painting of areas not specified in scope
  • Any work not specifically listed in the detailed scope above
"""

        return scope

    def _generate_timeline_section(self, context: Dict) -> str:
        """Generate timeline section"""
        timeline = context['timeline']
        start_date = datetime.now() + timedelta(days=7)
        end_date = start_date + timedelta(days=timeline)

        return f"""PROJECT TIMELINE:

Estimated Duration: {timeline} days
Anticipated Start Date: {start_date.strftime('%B %d, %Y')}
Anticipated Completion Date: {end_date.strftime('%B %d, %Y')}

Timeline is subject to change due to weather conditions, permit approvals, material availability, and change orders."""

    def _generate_payment_terms(self, context: Dict) -> str:
        """Generate payment terms"""
        budget = context.get('budget')

        if budget:
            return f"""PAYMENT TERMS:

Total Contract Value: ${budget:,.2f}

Payment Schedule:
• 20% deposit upon contract signing
• 30% upon completion of rough work
• 30% upon substantial completion
• 20% final payment upon project completion

All payments are due within 10 days of invoice."""
        else:
            return f"""PAYMENT TERMS:

Total Contract Value: To be determined based on final scope

Payment schedule will be established upon final cost agreement.
Standard terms: deposit, progress payments, final payment upon completion."""

    def _generate_terms_conditions(self, context: Dict) -> str:
        """Generate comprehensive terms and conditions based on industry standards"""
        return """TERMS AND CONDITIONS:

**1. PERMITS & INSPECTIONS**
* Contractor will obtain required building permits for work described in scope
* Client responsible for any design-related permits or variances
* All work subject to local building code compliance and inspection approval
* Re-inspection fees due to client changes are additional

**2. MATERIALS & WORKMANSHIP**
* All materials meet or exceed applicable building codes and manufacturer specifications
* Contractor warrants workmanship for **ONE (1) YEAR** from substantial completion
* Material warranties pass through from manufacturer to client
* Defects due to normal wear, abuse, or client modifications excluded

**3. CHANGE ORDERS & ADDITIONAL WORK**
* Written Change Order required for any scope modifications
* Additional work billed at unit prices listed or Time & Materials (T&M)
* Client approval required before proceeding with extra work
* Change Orders may affect project timeline and final completion date

**4. PAYMENT TERMS**
* Progress payments due within **10 calendar days** of invoice
* **1.5% monthly service charge** on overdue balances (18% APR)
* Final payment due upon substantial completion, before lien waiver release
* Client responsible for permit fees, utility connection charges, and inspection fees

**5. PROJECT TIMELINE & DELAYS**
* Timeline estimates based on normal material availability and weather conditions
* Contractor not liable for delays due to: weather, permit delays, client changes,
  material delivery issues, concealed conditions, or force majeure events
* Client-requested changes or delays may extend completion timeline

**6. INSURANCE & LIABILITY**
* Contractor maintains General Liability insurance ($1M minimum) and Workers' Compensation
* Client responsible for obtaining builder's risk/property insurance during construction
* Contractor liability limited to cost of remedial work, not consequential damages
* Client assumes risk for existing conditions and concealed defects

**7. SITE CONDITIONS & ACCESS**
* Client provides clear, safe access to work areas Monday-Friday, 7:30 AM - 5:00 PM
* Existing utilities assumed functional; additional costs apply for service issues
* Contractor not responsible for damage to landscaping in normal access areas
* Client responsible for protecting personal property and relocation of belongings

**8. CLEANUP & PROTECTION**
* Contractor maintains reasonably clean job site with daily broom-clean
* Construction dust and debris normal during active work periods
* Final cleanup included; deep cleaning of entire home is client responsibility
* Dust barriers provided where feasible without impeding work progress

**9. CONCEALED CONDITIONS**
* Contract based on visible conditions; concealed defects are additional work
* Examples: rotted framing, outdated wiring/plumbing, structural issues
* Discovery of concealed conditions requires immediate client notification
* Resolution by Change Order before work proceeds

**10. DISPUTE RESOLUTION**
* Good faith negotiation required before formal dispute resolution
* Disputes over $5,000 resolved through binding arbitration
* Prevailing party entitled to reasonable attorney fees and costs
* Contract governed by laws of [STATE] without regard to conflict provisions

**11. LIEN RIGHTS & FINAL PAYMENT**
* Contractor retains lien rights until final payment received
* Conditional lien waivers provided with progress payments
* Unconditional final lien waiver upon receipt of final payment
* 10-day right to cure notice required before lien filing

**12. COMPLETION & ACCEPTANCE**
* Substantial completion when work ready for intended use
* Client walkthrough and punch list creation within 5 business days
* Punch list items completed within 10 business days of creation
* Client acceptance evidenced by occupancy or 30 days after substantial completion"""

    def _generate_signatures_section(self, context: Dict) -> str:
        """Generate signatures section"""
        return """CONTRACT ACCEPTANCE:

By signing below, both parties agree to the terms and conditions set forth in this contract.


_____________________     Date: ___________
Contractor Signature


_____________________     Date: ___________
Client Signature


_____________________
Print Client Name"""

    def _generate_payment_schedule(self, context: Dict) -> List[Dict]:
        """Generate payment schedule milestones"""
        budget = context.get('budget', 0)
        if not budget:
            return []

        return [
            {'milestone': 'Contract Signing', 'percentage': 20, 'amount': budget * 0.20},
            {'milestone': 'Rough Work Complete', 'percentage': 30, 'amount': budget * 0.30},
            {'milestone': 'Substantial Completion', 'percentage': 30, 'amount': budget * 0.30},
            {'milestone': 'Final Completion', 'percentage': 20, 'amount': budget * 0.20}
        ]

    def _get_task_template(self, project_type: str) -> List[Dict]:
        """Get task template for project type"""
        # Clean project type for lookup
        clean_type = project_type.lower().split(',')[0].strip()

        # Map variations to standard templates
        type_mapping = {
            'kitchen renovation': 'kitchen renovation',
            'kitchen remodel': 'kitchen renovation',
            'bathroom remodel': 'bathroom remodel',
            'bathroom renovation': 'bathroom remodel'
        }

        template_key = type_mapping.get(clean_type, 'general renovation')
        return self.task_templates.get(template_key, self.task_templates['general renovation'])

    def _customize_tasks(self, base_tasks: List[Dict], analysis_data: Dict) -> List[Dict]:
        """Customize tasks based on analysis"""
        customized = []

        for task in base_tasks:
            custom_task = task.copy()

            # Adjust duration based on complexity
            complexity = analysis_data.get('complexity_score', 3)
            duration_multiplier = {1: 0.7, 2: 0.85, 3: 1.0, 4: 1.3, 5: 1.6}

            original_days = custom_task['days']
            adjusted_days = max(1, int(original_days * duration_multiplier[complexity]))
            custom_task['duration_days'] = adjusted_days

            # Add cost estimates (placeholder logic)
            custom_task['estimated_cost'] = adjusted_days * 500  # $500 per day baseline

            customized.append(custom_task)

        return customized

    def _schedule_tasks(self, tasks: List[Dict], complexity: int, preferred_start_date=None) -> List[Dict]:
        """Add scheduling information to tasks with user preferences"""
        if preferred_start_date:
            current_date = preferred_start_date
        else:
            current_date = datetime.now().date() + timedelta(days=7)  # Start in a week

        scheduled_tasks = []
        for i, task in enumerate(tasks):
            scheduled_task = task.copy()
            scheduled_task.update({
                'start_date': current_date,
                'end_date': current_date + timedelta(days=task['duration_days'] - 1),
                'order_index': i + 1,
                'is_critical_path': task['category'] in ['structural', 'electrical', 'plumbing'],
                'llm_generated': True,
                'generation_confidence': 4,
                'status': 'pending'
            })

            scheduled_tasks.append(scheduled_task)

            # Move to next task (with potential overlap for non-critical tasks)
            if task['category'] in ['planning', 'administrative']:
                current_date = scheduled_task['end_date'] + timedelta(days=1)
            else:
                # Allow some overlap for parallel work
                current_date = scheduled_task['start_date'] + timedelta(days=max(1, task['duration_days'] - 1))

        return scheduled_tasks

    def _load_contract_template(self) -> str:
        """Load contract template from file - prefers enhanced version"""
        # Try enhanced template first
        try:
            template_path = os.path.join(os.path.dirname(__file__), 'contract_template_enhanced.txt')
            with open(template_path, 'r', encoding='utf-8') as f:
                print("[OK] Loaded enhanced contract template")
                return f.read()
        except FileNotFoundError:
            pass

        # Fall back to original template
        try:
            template_path = os.path.join(os.path.dirname(__file__), 'contract_template.txt')
            with open(template_path, 'r', encoding='utf-8') as f:
                print("[OK] Loaded standard contract template")
                return f.read()
        except FileNotFoundError:
            print("[WARNING] Contract template files not found, using basic template")
            return self._get_basic_contract_template()
        except Exception as e:
            print(f"[WARNING] Error loading contract template: {e}")
            return self._get_basic_contract_template()

    def _get_basic_contract_template(self) -> str:
        """Fallback basic contract template"""
        return """
CONSTRUCTION CONTRACT

Project: [PROJECT_NAME]
Client: [CLIENT_NAME]
Contractor: [Your Company Name]
Date: [CONTRACT_DATE]

SCOPE OF WORK:
[DETAILED_SCOPE_OF_WORK]

PAYMENT TERMS:
Total Contract Value: [TOTAL_VALUE]
Payment Schedule:
• Contract Signing: [AMOUNT_1] (20%)
• Rough Work Complete: [AMOUNT_2] (30%)
• Substantial Completion: [AMOUNT_3] (30%)
• Final Completion: [AMOUNT_4] (20%)

TERMS AND CONDITIONS:
1. All work completed according to local building codes
2. Contractor obtains necessary permits
3. One year warranty on workmanship
4. Changes require written approval

SIGNATURES:

_____________________     _____________________
Contractor Signature      Client Signature

Date: _______________     Date: _______________
"""

    def _generate_project_objectives(self, context: Dict) -> str:
        """Generate project objectives based on scope analysis"""
        project_type = context.get('project_type', 'renovation').lower()
        work_items = context.get('work_items', [])

        objectives = []
        if 'kitchen' in project_type:
            objectives.append("* Modernize kitchen layout and functionality")
        if 'bathroom' in project_type:
            objectives.append("* Update bathroom with modern fixtures and finishes")
        if any('electrical' in item.lower() for item in work_items):
            objectives.append("* Update electrical to current code")
        if any('plumb' in item.lower() for item in work_items):
            objectives.append("* Relocate/update plumbing as needed")

        if not objectives:
            objectives.append(f"* Complete {project_type} renovation per scope requirements")

        return '\n'.join(objectives)

    def _generate_detailed_scope_of_work(self, context: Dict) -> str:
        """Generate comprehensive detailed scope from POS data or raw scope"""
        pos_data = context.get('pos_data')
        detailed_scope = []

        # If we have POS data, create detailed scope from line items grouped by category
        if pos_data and pos_data.get('line_items_by_category'):
            detailed_scope.append("The Contractor agrees to perform the following work:\n")

            for category, items in pos_data['line_items_by_category'].items():
                detailed_scope.append(f"**{category.upper()}:**")

                for item in items:
                    qty = item['quantity']
                    unit = item['unit']
                    activity = item['activity']
                    description = item.get('description', '')

                    # Format quantity text
                    if qty == 1 and unit == 'each':
                        qty_text = ""
                    elif unit == 'each':
                        qty_text = f"({qty} items) "
                    else:
                        qty_text = f"({qty} {unit}) "

                    detailed_scope.append(f"  * {activity} {qty_text}".strip())

                    if description:
                        detailed_scope.append(f"    - {description}")

                detailed_scope.append("")  # Blank line between categories

            # Add summary
            total_items = len(pos_data.get('all_line_items', []))
            total_value = pos_data.get('total_amount', 0)
            detailed_scope.append(f"\n**SCOPE SUMMARY:**")
            detailed_scope.append(f"* Total Line Items: {total_items}")
            detailed_scope.append(f"* Total Project Value: ${total_value:,.2f}")
            detailed_scope.append(f"* Source: {pos_data.get('quote_count', 0)} POS Quote(s)")

            return '\n'.join(detailed_scope)

        # Fallback to raw scope text or generic description
        raw_scope = context.get('raw_scope', '')
        if raw_scope:
            return f"The Contractor agrees to perform the following work:\n\n{raw_scope}"

        # Generic fallback
        project_type = context.get('project_type', 'renovation')
        return f"The Contractor agrees to complete a comprehensive {project_type} project including all necessary labor, materials, and equipment as detailed in the sections below."

    def _generate_demolition_scope(self, context: Dict) -> str:
        """Generate demolition work details from POS data or work items"""
        pos_data = context.get('pos_data')
        demo_items = []

        # First, try to get from POS data
        if pos_data and pos_data.get('line_items_by_section'):
            pos_demo_items = pos_data['line_items_by_section'].get('DEMOLITION_WORK', [])
            for item in pos_demo_items:
                qty_text = f"{item['quantity']} {item['unit']}" if item['quantity'] != 1 else ""
                demo_items.append(f"* {item['activity']} {qty_text}".strip())
                if item.get('description'):
                    demo_items.append(f"  - {item['description']}")

        # Fallback to work items analysis
        if not demo_items:
            work_items = context.get('work_items', [])
            for item in work_items:
                if any(word in item.lower() for word in ['remove', 'demo', 'tear out']):
                    demo_items.append(f"* {item}")

        # Default fallback
        if not demo_items:
            demo_items = ["* Remove existing fixtures and finishes as required for renovation work"]

        return '\n'.join(demo_items)

    def _generate_structural_scope(self, context: Dict) -> str:
        """Generate structural work details from POS data or work items"""
        pos_data = context.get('pos_data')
        structural_items = []

        # First, try to get from POS data
        if pos_data and pos_data.get('line_items_by_section'):
            pos_structural_items = pos_data['line_items_by_section'].get('STRUCTURAL_WORK', [])
            for item in pos_structural_items:
                qty_text = f"{item['quantity']} {item['unit']}" if item['quantity'] != 1 else ""
                structural_items.append(f"* {item['activity']} {qty_text}".strip())
                if item.get('description'):
                    structural_items.append(f"  - {item['description']}")

        # Fallback to work items analysis
        if not structural_items:
            work_items = context.get('work_items', [])
            for item in work_items:
                if any(word in item.lower() for word in ['frame', 'beam', 'support', 'header', 'structural']):
                    structural_items.append(f"* {item}")

        # Default fallback
        if not structural_items:
            return "* Structural work as required to support scope modifications"

        return '\n'.join(structural_items)

    def _generate_electrical_scope(self, context: Dict) -> str:
        """Generate electrical work details from POS data or work items"""
        pos_data = context.get('pos_data')
        electrical_items = []

        # First, try to get from POS data
        if pos_data and pos_data.get('line_items_by_section'):
            pos_electrical_items = pos_data['line_items_by_section'].get('ELECTRICAL_WORK', [])
            for item in pos_electrical_items:
                qty_text = f"{item['quantity']} {item['unit']}" if item['quantity'] != 1 else ""
                electrical_items.append(f"* {item['activity']} {qty_text}".strip())
                if item.get('description'):
                    electrical_items.append(f"  - {item['description']}")

        # Fallback to work items analysis
        if not electrical_items:
            work_items = context.get('work_items', [])
            for item in work_items:
                if any(word in item.lower() for word in ['electrical', 'outlet', 'light', 'circuit', 'panel']):
                    electrical_items.append(f"* {item}")

        # Default fallback
        if not electrical_items:
            electrical_items = [
                "* Update electrical circuits per current code requirements",
                "* Install outlets and lighting as specified"
            ]

        return '\n'.join(electrical_items)

    def _generate_plumbing_scope(self, context: Dict) -> str:
        """Generate plumbing work details from POS data or work items"""
        pos_data = context.get('pos_data')
        plumbing_items = []

        # First, try to get from POS data
        if pos_data and pos_data.get('line_items_by_section'):
            pos_plumbing_items = pos_data['line_items_by_section'].get('PLUMBING_WORK', [])
            for item in pos_plumbing_items:
                qty_text = f"{item['quantity']} {item['unit']}" if item['quantity'] != 1 else ""
                plumbing_items.append(f"* {item['activity']} {qty_text}".strip())
                if item.get('description'):
                    plumbing_items.append(f"  - {item['description']}")

        # Fallback to work items analysis
        if not plumbing_items:
            work_items = context.get('work_items', [])
            for item in work_items:
                if any(word in item.lower() for word in ['plumb', 'water', 'drain', 'pipe', 'sink', 'faucet']):
                    plumbing_items.append(f"* {item}")

        # Default fallback
        if not plumbing_items:
            return "* Plumbing work as required for fixture installations and relocations"

        return '\n'.join(plumbing_items)

    def _generate_hvac_scope(self, context: Dict) -> str:
        """Generate HVAC work details from POS data or work items"""
        pos_data = context.get('pos_data')
        hvac_items = []

        # First, try to get from POS data
        if pos_data and pos_data.get('line_items_by_section'):
            pos_hvac_items = pos_data['line_items_by_section'].get('HVAC_WORK', [])
            for item in pos_hvac_items:
                qty_text = f"{item['quantity']} {item['unit']}" if item['quantity'] != 1 else ""
                hvac_items.append(f"* {item['activity']} {qty_text}".strip())
                if item.get('description'):
                    hvac_items.append(f"  - {item['description']}")

        # Fallback to work items analysis
        if not hvac_items:
            work_items = context.get('work_items', [])
            for item in work_items:
                if any(word in item.lower() for word in ['hvac', 'heating', 'cooling', 'vent', 'duct']):
                    hvac_items.append(f"* {item}")

        # Default fallback
        if not hvac_items:
            return "* Reroute HVAC as needed to accommodate new layout; balance airflow after completion"

        return '\n'.join(hvac_items)

    def _generate_millwork_scope(self, context: Dict) -> str:
        """Generate millwork and cabinet details from POS data or work items"""
        pos_data = context.get('pos_data')
        millwork_items = []

        # First, try to get from POS data
        if pos_data and pos_data.get('line_items_by_section'):
            pos_millwork_items = pos_data['line_items_by_section'].get('MILLWORK_DETAILS', [])
            for item in pos_millwork_items:
                qty_text = f"{item['quantity']} {item['unit']}" if item['quantity'] != 1 else ""
                millwork_items.append(f"* {item['activity']} {qty_text}".strip())
                if item.get('description'):
                    millwork_items.append(f"  - {item['description']}")

        # Fallback to work items analysis
        if not millwork_items:
            work_items = context.get('work_items', [])
            for item in work_items:
                if any(word in item.lower() for word in ['cabinet', 'trim', 'millwork', 'vanity', 'built-in']):
                    millwork_items.append(f"* {item}")

        # Default fallback
        if not millwork_items:
            return "* Install trim and millwork to match existing or as specified"

        return '\n'.join(millwork_items)

    def _generate_countertop_tile_scope(self, context: Dict) -> str:
        """Generate countertop and tile work details from POS data or work items"""
        pos_data = context.get('pos_data')
        ct_tile_items = []

        # First, try to get from POS data
        if pos_data and pos_data.get('line_items_by_section'):
            pos_ct_items = pos_data['line_items_by_section'].get('COUNTERTOP_TILE_WORK', [])
            for item in pos_ct_items:
                qty_text = f"{item['quantity']} {item['unit']}" if item['quantity'] != 1 else ""
                ct_tile_items.append(f"* {item['activity']} {qty_text}".strip())
                if item.get('description'):
                    ct_tile_items.append(f"  - {item['description']}")

        # Fallback to work items analysis
        if not ct_tile_items:
            work_items = context.get('work_items', [])
            for item in work_items:
                if any(word in item.lower() for word in ['countertop', 'tile', 'backsplash', 'granite', 'quartz']):
                    ct_tile_items.append(f"* {item}")

        # Default fallback
        if not ct_tile_items:
            return "* Install countertops and tile work as specified"

        return '\n'.join(ct_tile_items)

    def _generate_flooring_paint_scope(self, context: Dict) -> str:
        """Generate flooring and paint details from POS data or work items"""
        pos_data = context.get('pos_data')
        flooring_paint_items = []

        # First, try to get from POS data
        if pos_data and pos_data.get('line_items_by_section'):
            pos_flooring_items = pos_data['line_items_by_section'].get('FLOORING_PAINT_WORK', [])
            for item in pos_flooring_items:
                qty_text = f"{item['quantity']} {item['unit']}" if item['quantity'] != 1 else ""
                flooring_paint_items.append(f"* {item['activity']} {qty_text}".strip())
                if item.get('description'):
                    flooring_paint_items.append(f"  - {item['description']}")

        # Fallback to work items analysis
        if not flooring_paint_items:
            work_items = context.get('work_items', [])
            for item in work_items:
                if any(word in item.lower() for word in ['floor', 'paint', 'carpet', 'hardwood', 'tile', 'lvp']):
                    flooring_paint_items.append(f"* {item}")

        # Default fallback
        if not flooring_paint_items:
            flooring_paint_items = [
                "* Install flooring per specifications",
                "* Prime and paint affected areas with two finish coats"
            ]

        return '\n'.join(flooring_paint_items)

    def _generate_exterior_scope(self, context: Dict) -> str:
        """Generate exterior work details from POS data or work items"""
        pos_data = context.get('pos_data')
        exterior_items = []

        # First, try to get from POS data
        if pos_data and pos_data.get('line_items_by_section'):
            pos_exterior_items = pos_data['line_items_by_section'].get('EXTERIOR_WORK', [])
            for item in pos_exterior_items:
                qty_text = f"{item['quantity']} {item['unit']}" if item['quantity'] != 1 else ""
                exterior_items.append(f"* {item['activity']} {qty_text}".strip())
                if item.get('description'):
                    exterior_items.append(f"  - {item['description']}")

        # Fallback to work items analysis
        if not exterior_items:
            work_items = context.get('work_items', [])
            for item in work_items:
                if any(word in item.lower() for word in ['exterior', 'siding', 'roof', 'window', 'door']):
                    exterior_items.append(f"* {item}")

        # Default fallback
        if not exterior_items:
            return "* No exterior work included in this scope"

        return '\n'.join(exterior_items)

    def _generate_exclusions(self, context: Dict) -> str:
        """Generate comprehensive exclusions based on industry best practices"""
        project_type = context.get('project_type', '').lower()

        # Standard exclusions for all projects
        base_exclusions = [
            "* **Architectural/engineering design services** (unless specified)",
            "* **Structural analysis or modifications** beyond described scope",
            "* **Hazardous material remediation** (asbestos, lead, mold testing/removal)",
            "* **Utility relocations** outside of normal rough-in adjustments",
            "* **Landscaping or hardscaping** restoration",
            "* **Furniture, window treatments, or decorative items**",
            "* **Pest control or extermination services**",
            "* **Security system installation or modifications**",
            "* **Work on weekends or holidays** (premium rates apply)",
            "* **Storage or relocation of client belongings**"
        ]

        # Project-specific exclusions
        project_exclusions = []
        if 'kitchen' in project_type:
            project_exclusions.extend([
                "* **Kitchen design services** beyond basic space planning",
                "* **Appliance delivery coordination** (client responsibility)",
                "* **Custom millwork** beyond standard cabinet installation",
                "* **Countertop templating delays** due to client selection changes",
                "* **Specialized lighting controls** or smart home integration"
            ])
        elif 'bathroom' in project_type:
            project_exclusions.extend([
                "* **Custom tile patterns** or mosaic work beyond standard installation",
                "* **Steam shower components** or luxury spa features",
                "* **Heated flooring systems** or in-wall speakers",
                "* **Custom glass work** beyond standard shower enclosures",
                "* **Bidet installation** or smart toilet features"
            ])
        elif 'addition' in project_type:
            project_exclusions.extend([
                "* **Soil testing or geotechnical reports**",
                "* **Utility service upgrades** to main panel or meter",
                "* **Septic system modifications** or well water testing",
                "* **Survey or boundary line verification**",
                "* **Zoning variances or special permits**"
            ])

        return '\n'.join(base_exclusions + project_exclusions)

    def _generate_allowances(self, context: Dict) -> str:
        """Generate allowances based on POS material items or project type"""
        pos_data = context.get('pos_data')
        allowances = []

        # First, try to generate from POS material items
        if pos_data and pos_data.get('material_items'):
            material_items = pos_data['material_items']

            # Group materials by category
            materials_by_category = {}
            for item in material_items:
                category = item['category']
                if category not in materials_by_category:
                    materials_by_category[category] = []
                materials_by_category[category].append(item)

            # Generate allowances from POS materials
            for category, items in materials_by_category.items():
                category_total = sum(item['total'] for item in items)
                item_names = ', '.join(set(item['activity'] for item in items[:3]))  # First 3 items
                if len(items) > 3:
                    item_names += f", and {len(items) - 3} more"
                allowances.append(f"* **{category} Materials**: ${category_total:,.2f} ({item_names})")

            if allowances:
                return '\n'.join(allowances)

        # Fallback to industry-standard allowances based on project type
        project_type = context.get('project_type', '').lower()
        budget = context.get('budget', 0)

        if 'kitchen' in project_type:
            allowances.extend([
                f"* **Appliance Package**: ${min(8000, budget * 0.15):,.0f} (refrigerator, range, dishwasher, microwave)",
                f"* **Countertop Material**: ${min(4500, budget * 0.08):,.0f} (quartz/granite including fabrication)",
                f"* **Cabinet Hardware**: ${min(1200, budget * 0.025):,.0f} (knobs, pulls, hinges, slides)",
                f"* **Lighting Package**: ${min(2500, budget * 0.05):,.0f} (recessed, under-cabinet, pendant)",
                f"* **Tile & Backsplash**: ${min(2000, budget * 0.04):,.0f} (material only, labor included)",
                f"* **Plumbing Fixtures**: ${min(1800, budget * 0.035):,.0f} (sink, faucet, disposal)",
                f"* **Paint & Primer**: ${min(800, budget * 0.015):,.0f} (premium interior paint)"
            ])
        elif 'bathroom' in project_type:
            allowances.extend([
                f"* **Plumbing Fixture Package**: ${min(3500, budget * 0.12):,.0f} (toilet, vanity, faucets, shower fixtures)",
                f"* **Tile Material**: ${min(2500, budget * 0.08):,.0f} (wall and floor tile including trim)",
                f"* **Vanity & Mirror**: ${min(2000, budget * 0.06):,.0f} (cabinet, countertop, mirror)",
                f"* **Lighting & Ventilation**: ${min(1200, budget * 0.04):,.0f} (vanity lights, exhaust fan)",
                f"* **Glass Shower Enclosure**: ${min(1500, budget * 0.05):,.0f} (if applicable)",
                f"* **Hardware & Accessories**: ${min(600, budget * 0.02):,.0f} (towel bars, hooks, grab bars)"
            ])
        elif 'addition' in project_type or 'home addition' in project_type:
            allowances.extend([
                f"* **Windows Package**: ${min(5000, budget * 0.08):,.0f} (energy efficient, installed)",
                f"* **Exterior Doors**: ${min(2500, budget * 0.04):,.0f} (entry and patio doors)",
                f"* **Flooring Material**: ${min(4000, budget * 0.06):,.0f} (hardwood, tile, or luxury vinyl)",
                f"* **Interior Doors & Trim**: ${min(2000, budget * 0.03):,.0f} (hollow core doors, casing, base)",
                f"* **Electrical Fixtures**: ${min(1800, budget * 0.03):,.0f} (lighting, switches, outlets)",
                f"* **HVAC Extensions**: ${min(3000, budget * 0.05):,.0f} (ductwork, vents, returns)"
            ])
        else:
            allowances.extend([
                f"* **General Material Package**: ${budget * 0.06:,.0f} (standard grade materials)",
                f"* **Fixture Allowance**: ${budget * 0.04:,.0f} (lighting, plumbing, hardware)",
                f"* **Finish Materials**: ${budget * 0.05:,.0f} (paint, trim, flooring accessories)"
            ])

        return '\n'.join(allowances)

    def _generate_unit_prices(self, context: Dict) -> str:
        """Generate comprehensive unit prices from POS activities or industry standards"""
        pos_data = context.get('pos_data')
        unit_prices = []

        # First, try to generate from POS line items
        if pos_data and pos_data.get('all_line_items'):
            # Group by activity to get unique items with their unit prices
            activities = {}
            for item in pos_data['all_line_items']:
                activity = item['activity']
                unit = item['unit']
                unit_price = item['unit_price']

                # Only include items with meaningful units (not 'each' or 'job')
                if unit in ['sqft', 'lnft', 'hour', 'day'] and unit_price > 0:
                    key = f"{activity}_{unit}"
                    if key not in activities:
                        activities[key] = {
                            'activity': activity,
                            'unit': unit,
                            'unit_price': unit_price
                        }

            # Generate unit price entries from POS
            for act in activities.values():
                unit_text = {
                    'sqft': 'sq ft',
                    'lnft': 'ln ft',
                    'hour': 'hour',
                    'day': 'day'
                }.get(act['unit'], act['unit'])

                unit_prices.append(f"* **{act['activity']}**: ${act['unit_price']:,.2f}/{unit_text}")

            # If we got POS-based prices, add some standard fallbacks
            if unit_prices:
                unit_prices.extend([
                    "",
                    "**Standard Labor & Service Rates:**",
                    "* **Permit amendment**: $150/ea (for scope changes requiring permits)",
                    "* **Cleanup - construction debris**: $85/hour (disposal included)"
                ])
                return '\n'.join(unit_prices)

        # Fallback to industry-standard unit prices
        project_type = context.get('project_type', '').lower()

        # Base unit prices applicable to all projects
        base_prices = [
            "* **Drywall patch/finish**: $4.75/sq ft (including texture match)",
            "* **Interior paint**: $2.85/sq ft (2 coats, primer if needed)",
            "* **Electrical outlet addition**: $195/ea (including wire run up to 25')",
            "* **Recessed light addition**: $225/ea (LED trim, up to 25' wire run)",
            "* **Switch addition/relocation**: $165/ea (standard location)",
            "* **Permit amendment**: $150/ea (for scope changes requiring permits)",
            "* **Cleanup - construction debris**: $85/hour (disposal included)"
        ]

        # Project-specific unit prices
        if 'kitchen' in project_type:
            kitchen_prices = [
                "* **Cabinet modification**: $125/linear ft (minor adjustments)",
                "* **Countertop extension**: $85/sq ft (matching material)",
                "* **Tile backsplash**: $12.50/sq ft (installed, standard subway)",
                "* **Under-cabinet lighting**: $45/linear ft (LED strip, hardwired)",
                "* **Appliance installation**: $150/ea (standard hookup)"
            ]
            return '\n'.join(base_prices + kitchen_prices)
        elif 'bathroom' in project_type:
            bathroom_prices = [
                "* **Tile installation**: $9.75/sq ft (wall) / $11.25/sq ft (floor)",
                "* **Plumbing rough-in relocation**: $285/fixture",
                "* **Vanity modification**: $195/linear ft",
                "* **Glass shelf addition**: $125/ea (tempered glass, brackets)",
                "* **Exhaust fan upgrade**: $185/ea (quiet operation, timer)"
            ]
            return '\n'.join(base_prices + bathroom_prices)
        else:
            general_prices = [
                "* **Flooring installation**: $8.50/sq ft (LVP) / $12.50/sq ft (hardwood)",
                "* **Interior door installation**: $285/ea (pre-hung, standard trim)",
                "* **Window trim**: $25/linear ft (painted wood casing)",
                "* **Baseboard installation**: $8.75/linear ft (including corners)",
                "* **Ceiling fan installation**: $195/ea (standard box, basic fan)"
            ]
            return '\n'.join(base_prices + general_prices)

    def _generate_project_timeline(self, context: Dict) -> str:
        """Generate project timeline with milestones"""
        timeline = context.get('timeline', 30)
        complexity = context.get('complexity', 3)

        if timeline <= 7:
            phases = [
                "* Permits & Mobilization: **2 days**",
                "* Execution: **3-4 days**",
                "* Completion & Cleanup: **1-2 days**"
            ]
        elif timeline <= 14:
            phases = [
                "* Permits & Mobilization: **3 days**",
                "* Demo & Rough Work: **5 days**",
                "* Finishes: **4 days**",
                "* Completion & Cleanup: **2 days**"
            ]
        elif timeline <= 30:
            phases = [
                "* Mobilization & Permits: **1 week**",
                "* Demo & Rough Work: **2 weeks**",
                "* MEP & Inspections: **1 week**",
                "* Finishes & Installation: **1 week**",
                "* Completion: **3 days**"
            ]
        else:
            phases = [
                "* Mobilization & Permits: **2 weeks**",
                "* Demo & Structural: **2 weeks**",
                "* MEP Rough-ins: **3 weeks**",
                "* Inspections & Close-up: **2 weeks**",
                "* Finishes & Installation: **3 weeks**",
                "* Completion & Closeout: **1 week**"
            ]

        return '\n'.join(phases)

    def _load_pos_category_mapping(self) -> Dict:
        """Map POS categories to contract template sections"""
        return {
            # POS Category Name → Contract Section Key
            'Kitchen Remodel': {
                'sections': ['MILLWORK_DETAILS', 'COUNTERTOP_TILE_WORK', 'FLOORING_PAINT_WORK'],
                'trades': ['electrical', 'plumbing', 'hvac']
            },
            'Bathroom Remodel': {
                'sections': ['PLUMBING_WORK', 'COUNTERTOP_TILE_WORK', 'FLOORING_PAINT_WORK'],
                'trades': ['electrical', 'plumbing']
            },
            'Roofing': {
                'sections': ['EXTERIOR_WORK'],
                'trades': []
            },
            'Flooring': {
                'sections': ['FLOORING_PAINT_WORK'],
                'trades': []
            },
            'Deck & Patio': {
                'sections': ['EXTERIOR_WORK', 'STRUCTURAL_WORK'],
                'trades': []
            },
            'Siding & Exterior': {
                'sections': ['EXTERIOR_WORK'],
                'trades': []
            },
            'Painting': {
                'sections': ['FLOORING_PAINT_WORK'],
                'trades': []
            },
            'Basement Finishing': {
                'sections': ['STRUCTURAL_WORK', 'FLOORING_PAINT_WORK', 'MILLWORK_DETAILS'],
                'trades': ['electrical', 'plumbing', 'hvac']
            },
            'Home Addition': {
                'sections': ['STRUCTURAL_WORK', 'EXTERIOR_WORK', 'FLOORING_PAINT_WORK'],
                'trades': ['electrical', 'plumbing', 'hvac']
            },
            'HVAC': {
                'sections': ['HVAC_WORK'],
                'trades': ['hvac']
            },
            'Electrical Work': {
                'sections': ['ELECTRICAL_WORK'],
                'trades': ['electrical']
            },
            'Plumbing Work': {
                'sections': ['PLUMBING_WORK'],
                'trades': ['plumbing']
            },
            'Demolition': {
                'sections': ['DEMOLITION_WORK'],
                'trades': []
            }
        }

    def _extract_pos_data(self, pos_quotes: List) -> Dict:
        """Extract and organize POS quote data for contract generation"""
        import json
        from decimal import Decimal

        line_items_by_category = {}
        line_items_by_section = {
            'DEMOLITION_WORK': [],
            'STRUCTURAL_WORK': [],
            'ELECTRICAL_WORK': [],
            'PLUMBING_WORK': [],
            'HVAC_WORK': [],
            'MILLWORK_DETAILS': [],
            'COUNTERTOP_TILE_WORK': [],
            'FLOORING_PAINT_WORK': [],
            'EXTERIOR_WORK': []
        }

        all_line_items = []
        total_amount = Decimal('0.00')
        material_items = []
        labor_items = []

        for quote in pos_quotes:
            # Only process accepted or draft quotes
            if hasattr(quote, 'status') and quote.status in ['draft', 'accepted']:
                try:
                    items = json.loads(quote.line_items) if quote.line_items else []

                    for item in items:
                        category = item.get('category_name', 'Miscellaneous')
                        activity_name = item.get('activity_name', 'Unknown')
                        quantity = item.get('quantity', 1)
                        unit = item.get('unit', 'each')
                        unit_price = float(item.get('unit_price', 0))
                        total = float(item.get('total', 0))
                        description = item.get('description', '')

                        # Create structured line item
                        structured_item = {
                            'category': category,
                            'activity': activity_name,
                            'quantity': quantity,
                            'unit': unit,
                            'unit_price': unit_price,
                            'total': total,
                            'description': description,
                            'quote_number': quote.quote_number if hasattr(quote, 'quote_number') else 'Unknown'
                        }

                        all_line_items.append(structured_item)
                        total_amount += Decimal(str(total))

                        # Group by category
                        if category not in line_items_by_category:
                            line_items_by_category[category] = []
                        line_items_by_category[category].append(structured_item)

                        # Map to contract sections
                        mapping = self.pos_category_mapping.get(category, {})
                        sections = mapping.get('sections', [])

                        for section in sections:
                            if section in line_items_by_section:
                                line_items_by_section[section].append(structured_item)

                        # Categorize as material or labor
                        activity_lower = activity_name.lower()
                        if any(word in activity_lower for word in ['install', 'labor', 'service', 'work']):
                            labor_items.append(structured_item)
                        else:
                            material_items.append(structured_item)

                except (json.JSONDecodeError, TypeError, AttributeError) as e:
                    print(f"[WARNING] Error parsing POS quote data: {e}")
                    continue

        return {
            'line_items_by_category': line_items_by_category,
            'line_items_by_section': line_items_by_section,
            'all_line_items': all_line_items,
            'total_amount': float(total_amount),
            'material_items': material_items,
            'labor_items': labor_items,
            'quote_count': len(pos_quotes)
        }