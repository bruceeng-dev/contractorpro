import os
from flask import Flask, render_template, request, redirect, url_for, flash, current_app, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
from datetime import datetime, date, timedelta
from decimal import Decimal
import uuid

from models import db, User, Job, Lead, Document, ProgressPhoto, Estimate, EstimateLineItem, EmailNotification, JobLocation, TaskTemplate, Task, Contract, JobSpecification, POSCategory, POSActivity, POSSubitem, POSCategorySpecMapping, POSSession, POSQuote
from config import config

# Import LLM service for AI-powered features
try:
    from llm_contract_service import LLMService
    llm_service = LLMService()
    LLM_AVAILABLE = True
except Exception as e:
    print(f"[WARNING] LLM Service not available: {e}")
    llm_service = None
    LLM_AVAILABLE = False

def create_app(config_name=None):
    app = Flask(__name__)
    
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    mail = Mail(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Create upload directory
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'photos'), exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'documents'), exist_ok=True)
    
    return app, migrate, mail

app, migrate, mail = create_app()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

# Authentication Routes
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid username or password', 'error')
    
    return render_template("login.html", title="Login")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        company_name = request.form.get('company_name', '')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
        elif User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
        else:
            user = User(username=username, email=email, company_name=company_name)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash('Registration successful!', 'success')
            return redirect(url_for('dashboard'))
    
    return render_template("register.html", title="Register")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Main Routes
@app.route("/")
@login_required
def dashboard():
    total_jobs = Job.query.filter_by(user_id=current_user.id).count()
    active_jobs = Job.query.filter_by(user_id=current_user.id, status='active').count()
    total_leads = Lead.query.filter_by(user_id=current_user.id).count()

    # Recent activity
    recent_jobs = Job.query.filter_by(user_id=current_user.id).order_by(Job.created_date.desc()).limit(5).all()
    recent_leads = Lead.query.filter_by(user_id=current_user.id).order_by(Lead.created_date.desc()).limit(3).all()

    # UNIFIED QUOTES: Combine POS quotes and traditional estimates
    pos_quotes = POSQuote.query.filter_by(user_id=current_user.id).all()
    estimates = Estimate.query.filter_by(user_id=current_user.id).all()

    # Calculate total quotes (POS + Estimates)
    total_quotes = len(pos_quotes) + len(estimates)

    return render_template("dashboard.html", title="Dashboard",
                         total_jobs=total_jobs,
                         total_leads=total_leads,
                         active_jobs=active_jobs,
                         recent_jobs=recent_jobs,
                         recent_leads=recent_leads,
                         pos_quotes=pos_quotes,
                         estimates=estimates,
                         total_quotes=total_quotes)

@app.route("/jobs")
@login_required
def jobs_list():
    jobs = Job.query.filter_by(user_id=current_user.id).order_by(Job.created_date.desc()).all()
    return render_template("jobs.html", title="Job Management", jobs=jobs)

@app.route("/jobs/new", methods=['GET', 'POST'])
@login_required
def new_job():
    if request.method == 'POST':
        # Server-side validation for required fields
        if not request.form.get('client_name'):
            flash('Client name is required', 'error')
            return render_template("new_job.html", title="New Job")

        if not request.form.get('project_type'):
            flash('Project type is required', 'error')
            return render_template("new_job.html", title="New Job")

        if not request.form.get('address'):
            flash('Project address is required', 'error')
            return render_template("new_job.html", title="New Job")

        if not request.form.get('start_date'):
            flash('Start date is required', 'error')
            return render_template("new_job.html", title="New Job")

        if not request.form.get('budget'):
            flash('Budget is required', 'error')
            return render_template("new_job.html", title="New Job")

        try:
            job = Job(
                user_id=current_user.id,
                client_name=request.form['client_name'],
                project_type=request.form['project_type'],
                address=request.form['address'],
                start_date=datetime.strptime(request.form['start_date'], '%Y-%m-%d').date(),
                budget=Decimal(request.form['budget']),
                description=request.form.get('description', ''),
                client_email=request.form.get('client_email', ''),
                client_phone=request.form.get('client_phone', ''),
                # New fields
                build_type=request.form.get('build_type', 'remodel'),
                total_square_footage=Decimal(request.form['total_square_footage']) if request.form.get('total_square_footage') else None,
                lot_square_footage=Decimal(request.form['lot_square_footage']) if request.form.get('lot_square_footage') else None,
                linear_footage=Decimal(request.form['linear_footage']) if request.form.get('linear_footage') else None,
                stories=int(request.form.get('stories', 1)),
                bedrooms=int(request.form['bedrooms']) if request.form.get('bedrooms') else None,
                bathrooms=Decimal(request.form['bathrooms']) if request.form.get('bathrooms') else None,
                permit_required=request.form.get('permit_required') == 'on'
            )
            db.session.add(job)
            db.session.commit()
            flash(f'New job created successfully for {job.client_name}!', 'success')
            return redirect(url_for('jobs_list'))
        except ValueError as e:
            flash(f'Invalid data format: {str(e)}', 'error')
            return render_template("new_job.html", title="New Job")
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating job: {str(e)}', 'error')
            return render_template("new_job.html", title="New Job")

    return render_template("new_job.html", title="New Job")

@app.route("/jobs/<int:job_id>")
@login_required
def job_detail(job_id):
    job = Job.query.filter_by(id=job_id, user_id=current_user.id).first_or_404()
    progress_photos = ProgressPhoto.query.filter_by(job_id=job_id).order_by(ProgressPhoto.uploaded_date.desc()).all()
    documents = Document.query.filter_by(job_id=job_id).order_by(Document.uploaded_date.desc()).all()
    estimates = Estimate.query.filter_by(job_id=job_id).all()

    # Calculate budget metrics
    total_actual = job.actual_cost if job.actual_cost else Decimal('0.00')
    budget = job.budget if job.budget else Decimal('0.00')
    budget_remaining = budget - total_actual
    budget_percentage = (total_actual / budget * 100) if budget > 0 else 0
    budget_used_pct = float(budget_percentage)

    return render_template("job_detail.html", title=f"Job: {job.client_name}",
                         job=job, progress_photos=progress_photos, documents=documents,
                         estimates=estimates, date=date,
                         total_actual=total_actual, budget_remaining=budget_remaining,
                         budget_percentage=budget_percentage, budget_used_pct=budget_used_pct)

@app.route("/leads")
@login_required
def leads_list():
    leads = Lead.query.filter_by(user_id=current_user.id).order_by(Lead.created_date.desc()).all()
    return render_template("leads.html", title="Lead Management", leads=leads)

@app.route("/leads/new", methods=['GET', 'POST'])
@login_required
def new_lead():
    if request.method == 'POST':
        lead = Lead(
            user_id=current_user.id,
            name=request.form['name'],
            email=request.form.get('email', ''),
            phone=request.form.get('phone', ''),
            project_type=request.form.get('project_type', ''),
            budget_range=request.form.get('budget_range', ''),
            notes=request.form.get('notes', ''),
            address=request.form.get('address', ''),
            lead_source=request.form.get('lead_source', ''),
            follow_up_date=datetime.strptime(request.form['follow_up_date'], '%Y-%m-%d').date() if request.form.get('follow_up_date') else None
        )
        db.session.add(lead)
        db.session.commit()
        flash('New lead added successfully!', 'success')
        return redirect(url_for('leads_list'))
    return render_template("new_lead.html", title="New Lead")

@app.route("/documentation")
@login_required
def documentation():
    return render_template("documentation.html", title="Documentation")

@app.route("/reports")
@login_required
def reports():
    return render_template("reports.html", title="Reports & Analytics")

# Photo Progress Tracking
@app.route("/jobs/<int:job_id>/photos/upload", methods=['POST'])
@login_required
def upload_progress_photo(job_id):
    job = Job.query.filter_by(id=job_id, user_id=current_user.id).first_or_404()
    
    if 'photo' not in request.files:
        flash('No file selected', 'error')
        return redirect(url_for('job_detail', job_id=job_id))
    
    file = request.files['photo']
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('job_detail', job_id=job_id))
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'photos', unique_filename)
        file.save(file_path)
        
        progress_photo = ProgressPhoto(
            job_id=job_id,
            filename=unique_filename,
            file_path=file_path,
            photo_type=request.form.get('photo_type', 'progress'),
            caption=request.form.get('caption', ''),
            location=request.form.get('location', ''),
            is_milestone=request.form.get('is_milestone') == 'on',
            milestone_percentage=int(request.form.get('milestone_percentage', 0)) if request.form.get('milestone_percentage') else None,
            taken_date=datetime.strptime(request.form['taken_date'], '%Y-%m-%d').date() if request.form.get('taken_date') else date.today()
        )
        
        db.session.add(progress_photo)
        db.session.commit()
        
        # Send notification if it's a milestone
        if progress_photo.is_milestone and current_app.config.get('ENABLE_EMAIL_NOTIFICATIONS'):
            send_milestone_notification(job, progress_photo)
        
        flash('Progress photo uploaded successfully!', 'success')
    else:
        flash('Invalid file type', 'error')
    
    return redirect(url_for('job_detail', job_id=job_id))

# Estimates System
@app.route("/estimates")
@login_required
def estimates_list():
    estimates = Estimate.query.filter_by(user_id=current_user.id).order_by(Estimate.created_date.desc()).all()
    pos_quotes = POSQuote.query.filter_by(user_id=current_user.id).order_by(POSQuote.created_date.desc()).all()
    return render_template("estimates.html", title="Estimates", estimates=estimates, pos_quotes=pos_quotes)

@app.route("/estimates/new", methods=['GET', 'POST'])
@login_required
def new_estimate():
    if request.method == 'POST':
        estimate = Estimate(
            user_id=current_user.id,
            estimate_number=f"EST-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}",
            client_name=request.form['client_name'],
            project_description=request.form.get('project_description', ''),
            labor_cost=Decimal(request.form.get('labor_cost', 0)),
            material_cost=Decimal(request.form.get('material_cost', 0)),
            equipment_cost=Decimal(request.form.get('equipment_cost', 0)),
            overhead_percentage=Decimal(request.form.get('overhead_percentage', 10.0)),
            profit_percentage=Decimal(request.form.get('profit_percentage', 15.0)),
            job_id=int(request.form['job_id']) if request.form.get('job_id') else None
        )
        estimate.calculate_total()
        db.session.add(estimate)
        db.session.commit()
        
        flash('Estimate created successfully!', 'success')
        return redirect(url_for('estimate_detail', estimate_id=estimate.id))
    
    # Get jobs for dropdown
    jobs = Job.query.filter_by(user_id=current_user.id).all()
    return render_template("new_estimate.html", title="New Estimate", jobs=jobs)

@app.route("/estimates/<int:estimate_id>")
@login_required
def estimate_detail(estimate_id):
    estimate = Estimate.query.filter_by(id=estimate_id, user_id=current_user.id).first_or_404()
    line_items = EstimateLineItem.query.filter_by(estimate_id=estimate_id).all()
    return render_template("estimate_detail.html", title=f"Estimate {estimate.estimate_number}", 
                         estimate=estimate, line_items=line_items)

@app.route("/estimates/<int:estimate_id>/line-items", methods=['POST'])
@login_required
def add_line_item(estimate_id):
    estimate = Estimate.query.filter_by(id=estimate_id, user_id=current_user.id).first_or_404()
    
    line_item = EstimateLineItem(
        estimate_id=estimate_id,
        description=request.form['description'],
        category=request.form.get('category', 'other'),
        quantity=Decimal(request.form.get('quantity', 1)),
        unit=request.form.get('unit', 'each'),
        unit_cost=Decimal(request.form['unit_cost']),
        notes=request.form.get('notes', '')
    )
    line_item.calculate_total()
    db.session.add(line_item)
    
    # Recalculate estimate total
    estimate.calculate_total()
    db.session.commit()
    
    flash('Line item added successfully!', 'success')
    return redirect(url_for('estimate_detail', estimate_id=estimate_id))

@app.route("/estimates/<int:estimate_id>/edit", methods=['GET', 'POST'])
@login_required
def edit_estimate(estimate_id):
    estimate = Estimate.query.filter_by(id=estimate_id, user_id=current_user.id).first_or_404()
    
    if request.method == 'POST':
        estimate.job_id = int(request.form['job_id']) if request.form.get('job_id') else None
        estimate.client_name = request.form['client_name']
        estimate.project_description = request.form.get('project_description', '')
        db.session.commit()
        flash('Estimate updated successfully!', 'success')
        return redirect(url_for('estimate_detail', estimate_id=estimate_id))
    
    jobs = Job.query.filter_by(user_id=current_user.id).all()
    return render_template("edit_estimate.html", estimate=estimate, jobs=jobs)

@app.before_request
def log_request_info():
    if request.path.endswith('/send'):
        print(f"SEND REQUEST: {request.method} {request.path}")
        print(f"USER: {current_user.is_authenticated if hasattr(current_user, 'is_authenticated') else 'No user'}")

@app.route("/estimates/<int:estimate_id>/send", methods=['POST'])
@login_required  
def send_estimate(estimate_id):
    print(f"=== SEND ESTIMATE DEBUG - ESTIMATE ID: {estimate_id} ===")
    estimate = Estimate.query.filter_by(id=estimate_id, user_id=current_user.id).first_or_404()
    print(f"Found estimate: {estimate.estimate_number}")
    
    if not estimate.job_id:
        print("ERROR: No job_id associated with estimate")
        flash('Cannot send estimate without associated job', 'error')
        return redirect(url_for('estimate_detail', estimate_id=estimate_id))
    
    job = Job.query.get(estimate.job_id)
    print(f"Found job: {job.client_name}")
    
    if not job.client_email:
        print("ERROR: No client email in job")
        flash('Client email required to send estimate', 'error')
        return redirect(url_for('estimate_detail', estimate_id=estimate_id))
    
    print(f"Client email: {job.client_email}")
    
    # Send email
    email_result = send_estimate_email(estimate, job)
    print(f"Email function returned: {email_result}")
    
    if email_result:
        estimate.status = 'sent'
        db.session.commit()
        print("SUCCESS: Estimate marked as sent")
        flash('Estimate sent successfully!', 'success')
    else:
        print("ERROR: Email function returned False")
        flash('Failed to send estimate', 'error')
    
    return redirect(url_for('estimate_detail', estimate_id=estimate_id))

# Test Email Route
@app.route("/test-email")
@login_required
def test_email():
    print("=== TEST EMAIL ROUTE ACCESSED ===")
    
    # Check what estimates exist
    all_estimates = Estimate.query.filter_by(user_id=current_user.id).all()
    print(f"Found {len(all_estimates)} estimates for user {current_user.id}")
    
    for est in all_estimates:
        print(f"Estimate {est.id}: job_id={est.job_id}, client={est.client_name}")
        if est.job_id:
            job = Job.query.get(est.job_id)
            if job:
                print(f"  Job found: {job.client_name}, email: {job.client_email}")
            else:
                print(f"  Job {est.job_id} not found!")
    
    # Find first estimate with job
    estimate = Estimate.query.filter_by(user_id=current_user.id).join(Job).first()
    if estimate and estimate.job:
        print(f"Testing with estimate {estimate.id} and job {estimate.job.id}")
        result = send_estimate_email(estimate, estimate.job)
        return f"Test email result: {result}<br>Check console for debug output<br><a href='/estimates'>Back to estimates</a>"
    
    return f"No estimate with job found. Found {len(all_estimates)} total estimates.<br><a href='/estimates'>Back to estimates</a>"

# =============================================================================
# NEW CONSOLIDATED ROUTES
# =============================================================================

# Unified Quote Builder Route
@app.route("/quotes/builder")
@login_required
def quote_builder():
    """Unified quote builder with tabs for AI, Manual (POS), and Quick Estimate modes"""
    job_id = request.args.get('job_id', type=int)
    mode = request.args.get('mode', 'manual')  # ai, manual, or quick

    job = None
    if job_id:
        job = Job.query.filter_by(id=job_id, user_id=current_user.id).first()

    jobs = Job.query.filter_by(user_id=current_user.id).order_by(Job.created_date.desc()).all()

    return render_template("quote_builder.html",
                         title="Quote Builder",
                         mode=mode,
                         job=job,
                         jobs=jobs,
                         llm_available=LLM_AVAILABLE)

# Contracts List Route
@app.route("/contracts")
@login_required
def contracts_list():
    """List all contracts across all jobs"""
    contracts = Contract.query.join(Job).filter(Job.user_id == current_user.id).order_by(Contract.created_date.desc()).all()
    return render_template("contracts_list.html",
                         title="Contracts",
                         contracts=contracts)

# Unified Contract Route (replaces contract_generator and contract_view)
@app.route("/jobs/<int:job_id>/contract")
@login_required
def unified_contract(job_id):
    """Unified contract interface with view, edit, and AI modes"""
    job = Job.query.filter_by(id=job_id, user_id=current_user.id).first_or_404()
    mode = request.args.get('mode', 'view')  # view, edit, or ai

    # Get or create contract
    contract = Contract.query.filter_by(job_id=job_id).first()
    if not contract:
        contract = Contract(
            job_id=job_id,
            contract_number=f"CON-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}",
            title=f"{job.project_type} Contract - {job.client_name}"
        )
        db.session.add(contract)
        db.session.commit()

    # Get contract data
    locations = JobLocation.query.filter_by(job_id=job_id).order_by(JobLocation.order_index).all()
    tasks = Task.query.filter_by(job_id=job_id).order_by(Task.order_index).all()
    pos_quotes = POSQuote.query.filter_by(job_id=job_id, user_id=current_user.id).all()

    return render_template("unified_contract.html",
                         title=f"Contract - {job.client_name}",
                         job=job,
                         contract=contract,
                         locations=locations,
                         tasks=tasks,
                         pos_quotes=pos_quotes,
                         mode=mode,
                         llm_available=LLM_AVAILABLE)

# =============================================================================
# END NEW CONSOLIDATED ROUTES
# =============================================================================

# Legacy Contract Generator Routes (keeping for backward compatibility temporarily)
@app.route("/jobs/<int:job_id>/contract/legacy")
@login_required
def contract_generator(job_id):
    job = Job.query.filter_by(id=job_id, user_id=current_user.id).first_or_404()
    locations = JobLocation.query.filter_by(job_id=job_id).order_by(JobLocation.order_index).all()
    tasks = Task.query.filter_by(job_id=job_id).order_by(Task.order_index).all()

    # Get existing contract or create new one
    contract = Contract.query.filter_by(job_id=job_id).first()
    if not contract:
        contract = Contract(
            job_id=job_id,
            contract_number=f"CON-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}",
            title=f"{job.project_type} Contract - {job.client_name}"
        )
        db.session.add(contract)
        db.session.commit()

    return render_template("contract_generator.html", title="Contract Generator",
                         job=job, locations=locations, tasks=tasks, contract=contract)

@app.route("/jobs/<int:job_id>/contract/view")
@login_required
def contract_view(job_id):
    """View the final contract document"""
    import json

    job = Job.query.filter_by(id=job_id, user_id=current_user.id).first_or_404()
    contract = Contract.query.filter_by(job_id=job_id).first()

    if not contract:
        flash('No contract found for this job. Please create one first.', 'warning')
        return redirect(url_for('contract_generator', job_id=job_id))

    # Get locations and tasks for contract
    locations = JobLocation.query.filter_by(job_id=job_id).order_by(JobLocation.order_index).all()
    tasks = Task.query.filter_by(job_id=job_id, included_in_contract=True).order_by(Task.order_index).all()

    # Get POS quotes for this job
    pos_quotes = POSQuote.query.filter_by(job_id=job_id, user_id=current_user.id).order_by(POSQuote.created_date.desc()).all()

    # Process POS quotes to extract line items for contract
    pos_line_items_by_category = {}
    total_pos_amount = 0

    for quote in pos_quotes:
        if quote.status in ['draft', 'accepted']:  # Include draft and accepted quotes
            try:
                line_items = json.loads(quote.line_items) if quote.line_items else []
                for item in line_items:
                    category = item.get('category_name', 'Miscellaneous')
                    if category not in pos_line_items_by_category:
                        pos_line_items_by_category[category] = []

                    pos_line_items_by_category[category].append({
                        'activity_name': item.get('activity_name', 'Unknown'),
                        'quantity': item.get('quantity', 1),
                        'unit_price': float(item.get('unit_price', 0)),
                        'total': float(item.get('total', 0)),
                        'quote_number': quote.quote_number,
                        'description': item.get('description', '')
                    })
                    total_pos_amount += float(item.get('total', 0))
            except (json.JSONDecodeError, TypeError) as e:
                print(f"Error parsing POS line items: {e}")
                continue

    return render_template("contract_view.html", title=f"Contract - {job.client_name}",
                         job=job, contract=contract, locations=locations, tasks=tasks,
                         pos_quotes=pos_quotes,
                         pos_line_items_by_category=pos_line_items_by_category,
                         total_pos_amount=total_pos_amount,
                         date=datetime)

@app.route("/jobs/<int:job_id>/contract/document-templates")
@login_required
def contract_document_templates(job_id):
    """Room specifications and POS integration for contracts - includes POS categories and mapping"""
    job = Job.query.filter_by(id=job_id, user_id=current_user.id).first_or_404()
    contract = Contract.query.filter_by(job_id=job_id).first()

    # Get POS quotes for this job
    pos_quotes = POSQuote.query.filter_by(job_id=job_id, user_id=current_user.id).order_by(POSQuote.created_date.desc()).all()

    # Get locations
    locations = JobLocation.query.filter_by(job_id=job_id).order_by(JobLocation.order_index).all()

    # Get POS categories for mapping
    pos_categories = POSCategory.query.filter_by(user_id=current_user.id, is_active=True).order_by(POSCategory.name).all()

    # Initialize empty location-POS mapping
    location_pos_mapping = {}

    return render_template("contract_document_templates.html",
                         title="Contract Document Templates",
                         job=job, contract=contract,
                         pos_quotes=pos_quotes, locations=locations,
                         pos_categories=pos_categories,
                         location_pos_mapping=location_pos_mapping)

@app.route("/jobs/<int:job_id>/contract/save-inline", methods=['POST'])
@login_required
def save_contract_inline(job_id):
    """Save inline edits to contract"""
    job = Job.query.filter_by(id=job_id, user_id=current_user.id).first_or_404()
    contract = Contract.query.filter_by(job_id=job_id).first()

    if not contract:
        return jsonify({'success': False, 'message': 'Contract not found'}), 404

    data = request.get_json()

    # Update contract fields from inline edits
    if 'title' in data:
        contract.title = data['title']
    if 'introduction_text' in data:
        contract.introduction_text = data['introduction_text']
    if 'terms_and_conditions' in data:
        contract.terms_and_conditions = data['terms_and_conditions']
    if 'payment_terms' in data:
        contract.payment_terms = data['payment_terms']
    if 'warranty_info' in data:
        contract.warranty_info = data['warranty_info']

    db.session.commit()

    return jsonify({'success': True, 'message': 'Contract saved successfully'})

@app.route("/jobs/<int:job_id>/locations", methods=['POST'])
@login_required
def add_job_location(job_id):
    job = Job.query.filter_by(id=job_id, user_id=current_user.id).first_or_404()
    
    location = JobLocation(
        job_id=job_id,
        name=request.form['location_name'],
        description=request.form.get('description', ''),
        square_footage=Decimal(request.form['square_footage']) if request.form.get('square_footage') else None,
        order_index=int(request.form.get('order_index', 1))
    )
    db.session.add(location)
    db.session.commit()
    
    flash(f'Location "{location.name}" added successfully!', 'success')
    return redirect(url_for('contract_generator', job_id=job_id))

@app.route("/jobs/<int:job_id>/tasks", methods=['POST'])
@login_required
def add_job_task(job_id):
    job = Job.query.filter_by(id=job_id, user_id=current_user.id).first_or_404()
    
    task = Task(
        job_id=job_id,
        location_id=int(request.form['location_id']) if request.form.get('location_id') else None,
        task_name=request.form['task_name'],
        task_description=request.form.get('task_description', ''),
        cost=Decimal(request.form['cost']) if request.form.get('cost') else None,
        estimated_days=int(request.form['estimated_days']) if request.form.get('estimated_days') else None,
        priority=int(request.form.get('priority', 1)),
        is_critical_path=request.form.get('is_critical_path') == 'on',
        included_in_contract=request.form.get('included_in_contract') == 'on',
        order_index=int(request.form.get('order_index', 1))
    )
    db.session.add(task)
    db.session.commit()
    
    flash(f'Task "{task.task_name}" added successfully!', 'success')
    return redirect(url_for('contract_generator', job_id=job_id))

@app.route("/task-templates")
@login_required
def task_templates():
    templates = TaskTemplate.query.filter_by(user_id=current_user.id, is_active=True).order_by(TaskTemplate.location_type, TaskTemplate.task_name).all()
    return render_template("task_templates.html", title="Task Templates", templates=templates)

@app.route("/task-templates/new", methods=['GET', 'POST'])
@login_required
def new_task_template():
    if request.method == 'POST':
        template = TaskTemplate(
            user_id=current_user.id,
            location_type=request.form['location_type'],
            task_name=request.form['task_name'],
            task_description=request.form['task_description'],
            default_cost=Decimal(request.form['default_cost']) if request.form.get('default_cost') else None,
            estimated_days=int(request.form['estimated_days']) if request.form.get('estimated_days') else None,
            category=request.form.get('category', '')
        )
        db.session.add(template)
        db.session.commit()
        flash('Task template created successfully!', 'success')
        return redirect(url_for('task_templates'))
    return render_template("new_task_template.html", title="New Task Template")

@app.route("/api/task-templates/<location_type>")
@login_required
def get_location_templates(location_type):
    templates = TaskTemplate.query.filter_by(
        user_id=current_user.id, 
        location_type=location_type, 
        is_active=True
    ).all()
    
    template_data = []
    for template in templates:
        template_data.append({
            'id': template.id,
            'task_name': template.task_name,
            'task_description': template.task_description,
            'default_cost': float(template.default_cost) if template.default_cost else 0,
            'estimated_days': template.estimated_days,
            'category': template.category
        })
    
    return jsonify(template_data)

# Task List Management Routes
@app.route("/tasks")
@login_required
def task_list():
    # Get all tasks for current user, grouped by job
    jobs_with_tasks = db.session.query(Job).filter_by(user_id=current_user.id).join(Task).distinct().all()

    # Build trade categories (same as calendar and gantt)
    trade_categories = [
        {'name': 'Foundation', 'color': '#8B4513', 'icon': '🏗️'},
        {'name': 'Framing', 'color': '#D2691E', 'icon': '🪚'},
        {'name': 'Electrical', 'color': '#FFD700', 'icon': '⚡'},
        {'name': 'Plumbing', 'color': '#4169E1', 'icon': '🚰'},
        {'name': 'HVAC', 'color': '#87CEEB', 'icon': '❄️'},
        {'name': 'Drywall', 'color': '#F5F5DC', 'icon': '🧱'},
        {'name': 'Painting', 'color': '#FF6347', 'icon': '🎨'},
        {'name': 'Flooring', 'color': '#8B4513', 'icon': '🪵'},
        {'name': 'Cabinets', 'color': '#CD853F', 'icon': '🗄️'},
        {'name': 'Countertops', 'color': '#696969', 'icon': '⬛'},
        {'name': 'Tile', 'color': '#B0C4DE', 'icon': '◽'},
        {'name': 'Roofing', 'color': '#2F4F4F', 'icon': '🏠'},
        {'name': 'Exterior', 'color': '#556B2F', 'icon': '🌳'},
        {'name': 'Landscaping', 'color': '#228B22', 'icon': '🌿'},
        {'name': 'General', 'color': '#808080', 'icon': '🔧'}
    ]

    # Get task statistics
    total_tasks = Task.query.join(Job).filter(Job.user_id == current_user.id).count()
    completed_tasks = Task.query.join(Job).filter(Job.user_id == current_user.id, Task.status == 'completed').count()
    critical_path_tasks = Task.query.join(Job).filter(Job.user_id == current_user.id, Task.is_critical_path == True).count()
    overdue_tasks = Task.query.join(Job).filter(
        Job.user_id == current_user.id,
        Task.scheduled_end_date < date.today(),
        Task.status.in_(['not_started', 'in_progress'])
    ).count()

    return render_template("task_list.html", title="Task Management",
                         jobs_with_tasks=jobs_with_tasks,
                         total_tasks=total_tasks,
                         completed_tasks=completed_tasks,
                         critical_path_tasks=critical_path_tasks,
                         overdue_tasks=overdue_tasks,
                         trade_categories=trade_categories,
                         today=date.today())

@app.route("/tasks/<int:task_id>/update", methods=['POST'])
@login_required
def update_task(task_id):
    task = Task.query.join(Job).filter(Task.id == task_id, Job.user_id == current_user.id).first_or_404()
    
    # Update task fields
    task.assigned_to = request.form.get('assigned_to', task.assigned_to)
    task.priority = int(request.form.get('priority', task.priority))
    task.status = request.form.get('status', task.status)
    task.scheduled_start_date = datetime.strptime(request.form['scheduled_start_date'], '%Y-%m-%d').date() if request.form.get('scheduled_start_date') else task.scheduled_start_date
    task.scheduled_end_date = datetime.strptime(request.form['scheduled_end_date'], '%Y-%m-%d').date() if request.form.get('scheduled_end_date') else task.scheduled_end_date
    
    # Handle actual dates based on status
    if task.status == 'in_progress' and not task.actual_start_date:
        task.actual_start_date = date.today()
    elif task.status == 'completed' and not task.actual_end_date:
        task.actual_end_date = date.today()
        if not task.actual_start_date:
            task.actual_start_date = task.scheduled_start_date or date.today()
    
    task.updated_date = datetime.utcnow()
    db.session.commit()
    
    flash(f'Task "{task.task_name}" updated successfully!', 'success')
    return redirect(url_for('task_list'))

@app.route("/api/tasks/<int:task_id>/status", methods=['POST'])
@login_required
def update_task_status(task_id):
    task = Task.query.join(Job).filter(Task.id == task_id, Job.user_id == current_user.id).first_or_404()
    
    data = request.get_json()
    new_status = data.get('status')
    
    if new_status in ['not_started', 'in_progress', 'completed', 'on_hold']:
        task.status = new_status
        
        # Auto-update actual dates
        if new_status == 'in_progress' and not task.actual_start_date:
            task.actual_start_date = date.today()
        elif new_status == 'completed' and not task.actual_end_date:
            task.actual_end_date = date.today()
            if not task.actual_start_date:
                task.actual_start_date = task.scheduled_start_date or date.today()
        
        task.updated_date = datetime.utcnow()
        db.session.commit()
        
        return jsonify({'success': True, 'status': task.status})
    
    return jsonify({'success': False, 'error': 'Invalid status'}), 400

# Calendar and Scheduling Routes
@app.route("/calendar")
@login_required
def calendar_view():
    from calendar import monthrange
    import calendar as cal

    # Get current month or requested month
    month = int(request.args.get('month', datetime.now().month))
    year = int(request.args.get('year', datetime.now().year))
    job_id_filter = request.args.get('job_id', type=int)

    # Get filtered job if specified
    filtered_job = None
    if job_id_filter:
        filtered_job = Job.query.filter_by(id=job_id_filter, user_id=current_user.id).first()

    # Get all scheduled tasks for the user (optionally filtered by job)
    query = Task.query.join(Job).filter(
        Job.user_id == current_user.id,
        Task.scheduled_start_date != None
    )
    if job_id_filter:
        query = query.filter(Job.id == job_id_filter)
    scheduled_tasks = query.all()

    # Get all jobs for drag-and-drop
    jobs = Job.query.filter_by(user_id=current_user.id).all()

    # Get unscheduled tasks (optionally filtered by job)
    unscheduled_query = Task.query.join(Job).filter(
        Job.user_id == current_user.id,
        Task.scheduled_start_date == None
    )
    if job_id_filter:
        unscheduled_query = unscheduled_query.filter(Job.id == job_id_filter)
    unscheduled_tasks = unscheduled_query.all()

    # Generate calendar data
    _, num_days = monthrange(year, month)
    month_name = cal.month_name[month]

    # Calculate start_day (day of week for first day of month, 0=Monday)
    start_day = date(year, month, 1).weekday()

    # Build trade categories (hardcoded for demo - would come from database in production)
    trade_categories = [
        {'name': 'Foundation', 'color': '#8B4513', 'icon': '🏗️'},
        {'name': 'Framing', 'color': '#D2691E', 'icon': '🪚'},
        {'name': 'Electrical', 'color': '#FFD700', 'icon': '⚡'},
        {'name': 'Plumbing', 'color': '#4169E1', 'icon': '��'},
        {'name': 'HVAC', 'color': '#87CEEB', 'icon': '❄️'},
        {'name': 'Drywall', 'color': '#F5F5DC', 'icon': '🧱'},
        {'name': 'Painting', 'color': '#FF6347', 'icon': '🎨'},
        {'name': 'Flooring', 'color': '#8B4513', 'icon': '🪵'},
        {'name': 'Cabinets', 'color': '#CD853F', 'icon': '🗄️'},
        {'name': 'Countertops', 'color': '#696969', 'icon': '⬛'},
        {'name': 'Tile', 'color': '#B0C4DE', 'icon': '◽'},
        {'name': 'Roofing', 'color': '#2F4F4F', 'icon': '🏠'},
        {'name': 'Exterior', 'color': '#556B2F', 'icon': '🌳'},
        {'name': 'Landscaping', 'color': '#228B22', 'icon': '🌿'},
        {'name': 'General', 'color': '#808080', 'icon': '🔧'}
    ]

    # Calculate task tracks (vertical positioning for overlapping tasks)
    task_tracks = {}
    date_tracks = {}  # Track which track numbers are used for each date

    for task in scheduled_tasks:
        if task.scheduled_start_date and task.scheduled_end_date:
            # Find available track for this task
            current_date = task.scheduled_start_date
            track_number = 0

            # Check all dates this task spans
            while current_date <= task.scheduled_end_date:
                date_key = current_date.isoformat()
                if date_key not in date_tracks:
                    date_tracks[date_key] = set()

                # Find first available track number
                while track_number in date_tracks[date_key]:
                    track_number += 1

                current_date += timedelta(days=1)

            # Assign this track to all dates the task spans
            current_date = task.scheduled_start_date
            while current_date <= task.scheduled_end_date:
                date_key = current_date.isoformat()
                date_tracks[date_key].add(track_number)
                current_date += timedelta(days=1)

            task_tracks[task.id] = track_number

    # Previous and next month navigation
    prev_month = month - 1 if month > 1 else 12
    prev_year = year if month > 1 else year - 1
    next_month = month + 1 if month < 12 else 1
    next_year = year if month < 12 else year + 1

    return render_template("calendar.html", title="Project Calendar",
                         scheduled_tasks=scheduled_tasks,
                         jobs=jobs,
                         unscheduled_tasks=unscheduled_tasks,
                         current_month=month,
                         current_year=year,
                         month_name=month_name,
                         num_days=num_days,
                         start_day=start_day,
                         trade_categories=trade_categories,
                         task_tracks=task_tracks,
                         job_id_filter=job_id_filter,
                         filtered_job=filtered_job,
                         prev_month=prev_month,
                         prev_year=prev_year,
                         next_month=next_month,
                         next_year=next_year)

@app.route("/api/tasks/<int:task_id>/schedule", methods=['POST'])
@login_required
def schedule_task(task_id):
    task = Task.query.join(Job).filter(Task.id == task_id, Job.user_id == current_user.id).first_or_404()
    
    data = request.get_json()
    start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
    
    # Calculate end date based on estimated duration
    duration = task.estimated_days or 1
    end_date = start_date + timedelta(days=duration - 1)
    
    task.scheduled_start_date = start_date
    task.scheduled_end_date = end_date
    task.updated_date = datetime.utcnow()
    
    db.session.commit()
    
    return jsonify({
        'success': True, 
        'start_date': start_date.isoformat(),
        'end_date': end_date.isoformat()
    })

@app.route("/gantt")
@login_required
def gantt_chart():
    job_id_filter = request.args.get('job_id', type=int)

    # Get filtered job if specified
    filtered_job = None
    if job_id_filter:
        filtered_job = Job.query.filter_by(id=job_id_filter, user_id=current_user.id).first()

    # Get all jobs with their tasks for current user
    if job_id_filter:
        jobs_with_tasks = Job.query.filter_by(user_id=current_user.id, id=job_id_filter).join(Task).distinct().all()
    else:
        jobs_with_tasks = Job.query.filter_by(user_id=current_user.id).join(Task).distinct().all()

    # Build trade categories (same as calendar)
    trade_categories = [
        {'name': 'Foundation', 'color': '#8B4513', 'icon': '🏗️'},
        {'name': 'Framing', 'color': '#D2691E', 'icon': '🪚'},
        {'name': 'Electrical', 'color': '#FFD700', 'icon': '⚡'},
        {'name': 'Plumbing', 'color': '#4169E1', 'icon': '🚰'},
        {'name': 'HVAC', 'color': '#87CEEB', 'icon': '❄️'},
        {'name': 'Drywall', 'color': '#F5F5DC', 'icon': '🧱'},
        {'name': 'Painting', 'color': '#FF6347', 'icon': '🎨'},
        {'name': 'Flooring', 'color': '#8B4513', 'icon': '🪵'},
        {'name': 'Cabinets', 'color': '#CD853F', 'icon': '🗄️'},
        {'name': 'Countertops', 'color': '#696969', 'icon': '⬛'},
        {'name': 'Tile', 'color': '#B0C4DE', 'icon': '◽'},
        {'name': 'Roofing', 'color': '#2F4F4F', 'icon': '🏠'},
        {'name': 'Exterior', 'color': '#556B2F', 'icon': '🌳'},
        {'name': 'Landscaping', 'color': '#228B22', 'icon': '🌿'},
        {'name': 'General', 'color': '#808080', 'icon': '🔧'}
    ]

    # Calculate project timelines
    project_data = []
    for job in jobs_with_tasks:
        tasks = Task.query.filter_by(job_id=job.id).order_by(Task.order_index).all()

        if tasks:
            # Find earliest start and latest end dates
            start_dates = [t.scheduled_start_date for t in tasks if t.scheduled_start_date]
            end_dates = [t.scheduled_end_date for t in tasks if t.scheduled_end_date]

            project_start = min(start_dates) if start_dates else None
            project_end = max(end_dates) if end_dates else None

            project_data.append({
                'job': job,
                'tasks': tasks,
                'project_start': project_start,
                'project_end': project_end,
                'duration': (project_end - project_start).days + 1 if project_start and project_end else None
            })

    return render_template("gantt_chart.html", title="Project Gantt Chart",
                         project_data=project_data,
                         trade_categories=trade_categories,
                         job_id_filter=job_id_filter,
                         filtered_job=filtered_job,
                         timedelta=timedelta)

# Email Notification Functions
def send_milestone_notification(job, progress_photo):
    try:
        msg = Message(
            subject=f"Project Update: {job.project_type} for {job.client_name}",
            recipients=[job.client_email] if job.client_email else [],
            sender=current_app.config['MAIL_DEFAULT_SENDER']
        )
        
        msg.body = f"""
        Hello {job.client_name},

        We've reached a milestone on your {job.project_type} project!

        Milestone: {progress_photo.milestone_percentage}% Complete
        Location: {progress_photo.location}
        Notes: {progress_photo.caption}

        Thank you for choosing {current_user.company_name or 'our company'} for your project.

        Best regards,
        {current_user.username}
        """
        
        mail.send(msg)
        
        # Log notification
        notification = EmailNotification(
            user_id=current_user.id,
            recipient_email=job.client_email,
            subject=msg.subject,
            body=msg.body,
            notification_type='milestone_update',
            related_id=progress_photo.id,
            status='sent',
            sent_date=datetime.utcnow()
        )
        db.session.add(notification)
        db.session.commit()
        
        return True
    except Exception as e:
        print(f"Failed to send milestone notification: {e}")
        return False

def send_estimate_email(estimate, job):
    try:
        print(f"DEBUG: Starting send_estimate_email function")
        print(f"DEBUG: Estimate ID: {estimate.id}, Job ID: {job.id}")
        print(f"DEBUG: Client email: {job.client_email}")
        
        # Check if Flask-Mail is configured
        mail_server = current_app.config.get('MAIL_SERVER')
        print(f"DEBUG: Mail server config: {mail_server}")
        
        # For development, just simulate email sending
        if current_app.config.get('MAIL_SUPPRESS_SEND'):
            print("DEBUG: Mail suppression enabled - simulating email")
            
            email_content = f"""
            Dear {job.client_name},

            Please find your project estimate for {estimate.project_description}.

            Estimate Number: {estimate.estimate_number}
            Project: {job.project_type}
            Total Cost: ${estimate.total_cost:,.2f}

            Best regards,
            {current_user.company_name or current_user.username}
            """
            
            print(f"SIMULATED EMAIL CONTENT:\n{email_content}")
            print("✓ Email simulation successful")
            return True
        
        # Try to send real email
        msg = Message(
            subject=f"Project Estimate: {estimate.project_description}",
            recipients=[job.client_email],
            sender=current_app.config['MAIL_DEFAULT_SENDER']
        )
        
        msg.body = f"""
        Dear {job.client_name},

        Please find attached your project estimate for {estimate.project_description}.

        Estimate Number: {estimate.estimate_number}
        Project: {job.project_type}
        Total Cost: ${estimate.total_cost:,.2f}

        This estimate is valid until: {estimate.valid_until.strftime('%B %d, %Y') if estimate.valid_until else 'Further Notice'}

        Please contact us if you have any questions.

        Best regards,
        {current_user.company_name or current_user.username}
        """
        
        mail.send(msg)
        print("✓ Real email sent successfully")
        
        # Log notification
        notification = EmailNotification(
            user_id=current_user.id,
            recipient_email=job.client_email,
            subject=msg.subject,
            body=msg.body,
            notification_type='estimate_sent',
            related_id=estimate.id,
            status='sent',
            sent_date=datetime.utcnow()
        )
        db.session.add(notification)
        db.session.commit()
        
        return True
    except Exception as e:
        print(f"Failed to send estimate email: {e}")
        return False

# API Endpoints for AJAX functionality
@app.route("/api/jobs/<int:job_id>/progress")
@login_required
def job_progress_api(job_id):
    job = Job.query.filter_by(id=job_id, user_id=current_user.id).first_or_404()
    progress_photos = ProgressPhoto.query.filter_by(job_id=job_id, is_milestone=True).all()

    milestones = []
    for photo in progress_photos:
        milestones.append({
            'percentage': photo.milestone_percentage,
            'date': photo.taken_date.isoformat() if photo.taken_date else None,
            'caption': photo.caption,
            'location': photo.location
        })

    return jsonify({
        'job_id': job.id,
        'client_name': job.client_name,
        'milestones': milestones
    })

# ============================================================================
# POS Multi-Layer System Routes
# ============================================================================

@app.route("/pos/multilayer")
@app.route("/pos/multilayer/<int:job_id>")
@login_required
def pos_multilayer(job_id=None):
    """Main POS interface - Layer 1: Job Specifications"""
    # Check for job_id in path parameter or query parameter
    if not job_id:
        job_id = request.args.get('job_id', type=int)

    job = None
    if job_id:
        job = Job.query.filter_by(id=job_id, user_id=current_user.id).first_or_404()

    # Get all active job specifications
    job_specs = JobSpecification.query.filter_by(is_active=True).order_by(JobSpecification.order_index).all()

    return render_template("pos_multilayer.html", title="Build Quote", job_specs=job_specs, job=job)

@app.route("/pos/admin")
@login_required
def pos_admin():
    """POS Admin interface for managing categories and activities"""
    categories = POSCategory.query.filter_by(user_id=current_user.id).order_by(POSCategory.order_index).all()
    return render_template("pos_admin.html", title="POS Admin", categories=categories)

@app.route("/pos/admin/spec-mappings")
@login_required
def pos_spec_mappings():
    """Admin interface for mapping categories to job specifications"""
    categories = POSCategory.query.filter_by(user_id=current_user.id).order_by(POSCategory.order_index).all()
    job_specs = JobSpecification.query.filter_by(is_active=True).order_by(JobSpecification.order_index).all()

    # Get existing mappings
    mappings = {}
    for category in categories:
        category_mappings = POSCategorySpecMapping.query.filter_by(category_id=category.id).all()
        mappings[category.id] = [m.spec_id for m in category_mappings]

    return render_template("pos_spec_mappings.html", title="Specification Mappings",
                         categories=categories, job_specs=job_specs, mappings=mappings)

@app.route("/pos/quotes")
@login_required
def pos_quotes_list():
    """UNIFIED QUOTES PAGE - Shows both POS quotes and traditional estimates"""
    pos_quotes = POSQuote.query.filter_by(user_id=current_user.id).order_by(POSQuote.created_date.desc()).all()
    estimates = Estimate.query.filter_by(user_id=current_user.id).order_by(Estimate.created_date.desc()).all()
    return render_template("pos_quotes.html", title="All Quotes", pos_quotes=pos_quotes, estimates=estimates)

@app.route("/pos/quotes/<int:quote_id>")
@login_required
def pos_quote_detail(quote_id):
    """View a specific POS quote"""
    quote = POSQuote.query.filter_by(id=quote_id, user_id=current_user.id).first_or_404()

    # Parse JSON data
    import json
    selected_specs = json.loads(quote.selected_spec_ids) if quote.selected_spec_ids else []
    line_items = json.loads(quote.line_items) if quote.line_items else []

    # Get specification names
    specs = JobSpecification.query.filter(JobSpecification.id.in_(selected_specs)).all() if selected_specs else []

    return render_template("pos_quote_detail.html", title=f"Quote {quote.quote_number}",
                         quote=quote, specs=specs, line_items=line_items)

# POS API Endpoints

@app.route("/api/pos/job-specifications")
@login_required
def api_pos_job_specifications():
    """Get all active job specifications"""
    specs = JobSpecification.query.filter_by(is_active=True).order_by(JobSpecification.order_index).all()
    return jsonify([{
        'id': s.id,
        'name': s.name,
        'display_name': s.display_name,
        'description': s.description,
        'order_index': s.order_index
    } for s in specs])

@app.route("/api/pos/session/start", methods=['POST'])
@login_required
def api_pos_session_start():
    """Start a new POS session with selected job specifications"""
    import json

    data = request.get_json()
    selected_specs = data.get('selected_specs', [])
    project_description = data.get('project_description', '')
    job_id = data.get('job_id')

    # Create new session
    session_token = str(uuid.uuid4())

    session = POSSession(
        user_id=current_user.id,
        job_id=job_id,
        session_token=session_token,
        selected_spec_ids=json.dumps(selected_specs),
        current_layer=2,
        project_description=project_description,
        is_active=True
    )

    db.session.add(session)
    db.session.commit()

    return jsonify({
        'success': True,
        'session_token': session_token,
        'selected_specs': selected_specs,
        'next_layer': 2
    })

@app.route("/api/pos/session/<session_token>/categories")
@login_required
def api_pos_session_categories(session_token):
    """Get filtered categories based on session's job specification selections"""
    import json

    session = POSSession.query.filter_by(session_token=session_token, user_id=current_user.id, is_active=True).first_or_404()

    selected_specs = json.loads(session.selected_spec_ids) if session.selected_spec_ids else []

    # Get categories that have mappings to selected specs
    if selected_specs:
        # Get all mappings for selected specs
        mappings = POSCategorySpecMapping.query.filter(POSCategorySpecMapping.spec_id.in_(selected_specs)).all()
        category_ids = list(set([m.category_id for m in mappings]))

        # Get categories
        categories = POSCategory.query.filter(
            POSCategory.id.in_(category_ids),
            POSCategory.user_id == current_user.id,
            POSCategory.is_active == True
        ).order_by(POSCategory.order_index).all()
    else:
        # No specs selected, show all categories
        categories = POSCategory.query.filter_by(user_id=current_user.id, is_active=True).order_by(POSCategory.order_index).all()

    return jsonify({
        'session_token': session_token,
        'categories': [{
            'id': c.id,
            'name': c.name,
            'description': c.description,
            'icon': c.icon,
            'keywords': c.keywords
        } for c in categories],
        'count': len(categories)
    })

@app.route("/api/pos/session/<session_token>/category/<int:category_id>/activities")
@login_required
def api_pos_session_activities(session_token, category_id):
    """Get activities for a specific category"""
    session = POSSession.query.filter_by(session_token=session_token, user_id=current_user.id, is_active=True).first_or_404()
    category = POSCategory.query.filter_by(id=category_id, user_id=current_user.id).first_or_404()

    # Get all activities for this category
    activities = POSActivity.query.filter_by(category_id=category_id, is_active=True).order_by(POSActivity.order_index).all()

    return jsonify({
        'session_token': session_token,
        'category': {
            'id': category.id,
            'name': category.name,
            'description': category.description
        },
        'activities': [{
            'id': a.id,
            'name': a.name,
            'description': a.description,
            'base_cost': float(a.base_cost),
            'unit': a.unit,
            'has_subitems': a.has_subitems
        } for a in activities],
        'count': len(activities)
    })

@app.route("/api/pos/activity/<int:activity_id>/subitems")
@login_required
def api_pos_activity_subitems(activity_id):
    """Get subitems for an activity"""
    activity = POSActivity.query.get_or_404(activity_id)
    subitems = POSSubitem.query.filter_by(activity_id=activity_id).order_by(POSSubitem.order_index).all()

    return jsonify({
        'activity_id': activity_id,
        'activity': {
            'id': activity.id,
            'name': activity.name,
            'description': activity.description,
            'base_cost': float(activity.base_cost),
            'unit': activity.unit,
            'has_subitems': activity.has_subitems
        },
        'subitems': [{
            'id': s.id,
            'name': s.name,
            'description': s.description,
            'price_adjustment': float(s.price_adjustment),
            'is_default': s.is_default
        } for s in subitems]
    })

@app.route("/api/pos/session/<session_token>/save-quote", methods=['POST'])
@login_required
def api_pos_save_quote(session_token):
    """Save a POS quote from session cart"""
    import json

    session = POSSession.query.filter_by(session_token=session_token, user_id=current_user.id, is_active=True).first_or_404()
    data = request.get_json()

    # Generate quote number
    quote_count = POSQuote.query.filter_by(user_id=current_user.id).count()
    quote_number = f"POS-{current_user.id}-{quote_count + 1:04d}"

    # Calculate totals
    line_items = data.get('line_items', [])
    subtotal = Decimal(str(sum(item.get('total', 0) for item in line_items)))
    tax_rate = Decimal(str(data.get('tax_rate', 0)))
    tax_amount = subtotal * (tax_rate / 100)
    total_amount = subtotal + tax_amount

    # Create quote
    quote = POSQuote(
        user_id=current_user.id,
        job_id=session.job_id,
        quote_number=quote_number,
        client_name=data.get('client_name', ''),
        project_description=session.project_description,
        selected_spec_ids=session.selected_spec_ids,
        line_items=json.dumps(line_items),
        subtotal=subtotal,
        tax_rate=tax_rate,
        tax_amount=tax_amount,
        total_amount=total_amount,
        status='draft'
    )

    db.session.add(quote)

    # Mark session as inactive
    session.is_active = False

    db.session.commit()

    return jsonify({
        'success': True,
        'quote_id': quote.id,
        'quote_number': quote.quote_number,
        'total_amount': float(total_amount)
    })

@app.route("/api/pos/categories", methods=['POST'])
@login_required
def api_pos_create_category():
    """Create a new POS category"""
    data = request.get_json()

    category = POSCategory(
        user_id=current_user.id,
        name=data['name'],
        description=data.get('description', ''),
        icon=data.get('icon', ''),
        keywords=data.get('keywords', ''),
        order_index=data.get('order_index', 1)
    )

    db.session.add(category)
    db.session.commit()

    return jsonify({
        'success': True,
        'category_id': category.id,
        'message': f'Category "{category.name}" created successfully'
    })

@app.route("/api/pos/activities", methods=['POST'])
@login_required
def api_pos_create_activity():
    """Create a new POS activity"""
    data = request.get_json()

    # Verify category belongs to user
    category = POSCategory.query.filter_by(id=data['category_id'], user_id=current_user.id).first_or_404()

    activity = POSActivity(
        category_id=category.id,
        name=data['name'],
        description=data.get('description', ''),
        base_cost=Decimal(str(data['base_cost'])),
        unit=data.get('unit', 'each'),
        has_subitems=data.get('has_subitems', False),
        order_index=data.get('order_index', 1)
    )

    db.session.add(activity)
    db.session.commit()

    return jsonify({
        'success': True,
        'activity_id': activity.id,
        'message': f'Activity "{activity.name}" created successfully'
    })

@app.route("/api/pos/spec-mappings", methods=['GET', 'POST'])
@login_required
def api_pos_spec_mappings():
    """Get or save specification mappings"""
    import json

    if request.method == 'POST':
        data = request.get_json()
        category_id = data['category_id']
        spec_ids = data['spec_ids']

        # Verify category belongs to user
        category = POSCategory.query.filter_by(id=category_id, user_id=current_user.id).first_or_404()

        # Delete existing mappings
        POSCategorySpecMapping.query.filter_by(category_id=category_id).delete()

        # Create new mappings
        for spec_id in spec_ids:
            mapping = POSCategorySpecMapping(
                category_id=category_id,
                spec_id=spec_id
            )
            db.session.add(mapping)

        db.session.commit()

        return jsonify({
            'success': True,
            'message': f'Saved {len(spec_ids)} mappings for category {category.name}'
        })

    else:  # GET
        # Get all mappings for user's categories
        categories = POSCategory.query.filter_by(user_id=current_user.id).all()
        category_ids = [c.id for c in categories]

        mappings = POSCategorySpecMapping.query.filter(POSCategorySpecMapping.category_id.in_(category_ids)).all()

        return jsonify([{
            'id': m.id,
            'category_id': m.category_id,
            'spec_id': m.spec_id,
            'specific_activity_ids': m.specific_activity_ids
        } for m in mappings])

# ============================================================================
# POS Integration Routes - Connecting to Estimates, Jobs, Contracts
# ============================================================================

@app.route("/api/pos/quotes/<int:quote_id>/convert-to-estimate", methods=['POST'])
@login_required
def convert_pos_quote_to_estimate(quote_id):
    """Convert a POS Quote to a traditional Estimate"""
    import json

    pos_quote = POSQuote.query.filter_by(id=quote_id, user_id=current_user.id).first_or_404()

    # Generate estimate number
    estimate_count = Estimate.query.filter_by(user_id=current_user.id).count()
    estimate_number = f"EST-{current_user.id}-{estimate_count + 1:04d}"

    # Parse line items
    line_items = json.loads(pos_quote.line_items) if pos_quote.line_items else []

    # Calculate costs by category
    labor_cost = Decimal('0')
    material_cost = Decimal('0')
    equipment_cost = Decimal('0')

    # Create estimate
    estimate = Estimate(
        user_id=current_user.id,
        job_id=pos_quote.job_id,
        estimate_number=estimate_number,
        client_name=pos_quote.client_name,
        project_description=pos_quote.project_description,
        labor_cost=pos_quote.subtotal * Decimal('0.6'),  # 60% labor estimate
        material_cost=pos_quote.subtotal * Decimal('0.35'),  # 35% materials
        equipment_cost=pos_quote.subtotal * Decimal('0.05'),  # 5% equipment
        overhead_percentage=Decimal('10.0'),
        profit_percentage=Decimal('15.0'),
        status='draft'
    )
    estimate.calculate_total()
    db.session.add(estimate)

    # Commit estimate first to get the ID
    db.session.flush()

    # Add line items from POS quote
    for item in line_items:
        line_item = EstimateLineItem(
            estimate_id=estimate.id,
            description=item.get('name', ''),
            category='labor',  # Default to labor
            quantity=Decimal(str(item.get('quantity', 1))),
            unit=item.get('unit', 'each'),
            unit_cost=Decimal(str(item.get('unit_price', 0)))
        )
        line_item.calculate_total()
        db.session.add(line_item)

    # Update POS quote status
    pos_quote.status = 'converted'

    db.session.commit()

    return jsonify({
        'success': True,
        'estimate_id': estimate.id,
        'estimate_number': estimate_number,
        'message': f'POS Quote converted to Estimate {estimate_number}'
    })

@app.route("/api/pos/quotes/<int:quote_id>/send-to-client", methods=['POST'])
@login_required
def send_pos_quote_to_client(quote_id):
    """Send POS Quote to client via email"""
    import json

    pos_quote = POSQuote.query.filter_by(id=quote_id, user_id=current_user.id).first_or_404()

    # Get job for client email
    if not pos_quote.job_id:
        return jsonify({'success': False, 'message': 'Quote must be linked to a job to send'}), 400

    job = Job.query.get(pos_quote.job_id)
    if not job or not job.client_email:
        return jsonify({'success': False, 'message': 'Job must have client email'}), 400

    # Parse line items for email
    line_items = json.loads(pos_quote.line_items) if pos_quote.line_items else []

    # Build line items table
    line_items_html = ""
    for item in line_items:
        line_items_html += f"""
        <tr>
            <td style="padding: 8px; border-bottom: 1px solid #ddd;">{item.get('name', '')}</td>
            <td style="padding: 8px; border-bottom: 1px solid #ddd; text-align: center;">{item.get('quantity', 1)}</td>
            <td style="padding: 8px; border-bottom: 1px solid #ddd; text-align: center;">{item.get('unit', 'each')}</td>
            <td style="padding: 8px; border-bottom: 1px solid #ddd; text-align: right;">${item.get('unit_price', 0):,.2f}</td>
            <td style="padding: 8px; border-bottom: 1px solid #ddd; text-align: right;">${item.get('total', 0):,.2f}</td>
        </tr>
        """

    # Create email
    try:
        if current_app.config.get('MAIL_SUPPRESS_SEND'):
            # Simulated email for development
            email_content = f"""
            Dear {pos_quote.client_name},

            Please find your project quote for {pos_quote.project_description}.

            Quote Number: {pos_quote.quote_number}
            Total: ${pos_quote.total_amount:,.2f}

            Line Items:
            {line_items_html}

            Best regards,
            {current_user.company_name or current_user.username}
            """
            print(f"SIMULATED POS QUOTE EMAIL:\n{email_content}")

            # Log notification
            notification = EmailNotification(
                user_id=current_user.id,
                recipient_email=job.client_email,
                subject=f"Project Quote: {pos_quote.project_description}",
                body=email_content,
                notification_type='pos_quote_sent',
                related_id=pos_quote.id,
                status='sent',
                sent_date=datetime.utcnow()
            )
            db.session.add(notification)

            # Update quote status
            pos_quote.status = 'sent'
            db.session.commit()

            return jsonify({
                'success': True,
                'message': 'Quote sent to client (simulated in development mode)'
            })
        else:
            # Real email sending
            msg = Message(
                subject=f"Project Quote: {pos_quote.project_description}",
                recipients=[job.client_email],
                sender=current_app.config['MAIL_DEFAULT_SENDER']
            )

            msg.html = f"""
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <h2 style="color: #667eea;">Project Quote</h2>
                    <p>Dear {pos_quote.client_name},</p>
                    <p>Thank you for your interest. Please find your detailed project quote below.</p>

                    <div style="background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
                        <p><strong>Quote Number:</strong> {pos_quote.quote_number}</p>
                        <p><strong>Project:</strong> {pos_quote.project_description}</p>
                        <p><strong>Date:</strong> {pos_quote.created_date.strftime('%B %d, %Y')}</p>
                    </div>

                    <h3 style="color: #667eea;">Line Items</h3>
                    <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
                        <thead>
                            <tr style="background: #667eea; color: white;">
                                <th style="padding: 10px; text-align: left;">Item</th>
                                <th style="padding: 10px; text-align: center;">Qty</th>
                                <th style="padding: 10px; text-align: center;">Unit</th>
                                <th style="padding: 10px; text-align: right;">Unit Price</th>
                                <th style="padding: 10px; text-align: right;">Total</th>
                            </tr>
                        </thead>
                        <tbody>
                            {line_items_html}
                        </tbody>
                    </table>

                    <div style="background: #667eea; color: white; padding: 20px; border-radius: 5px; text-align: right;">
                        <p style="margin: 0; font-size: 1.2em;"><strong>Total: ${pos_quote.total_amount:,.2f}</strong></p>
                    </div>

                    <p style="margin-top: 30px;">If you have any questions or would like to proceed, please don't hesitate to contact us.</p>

                    <p>Best regards,<br>
                    {current_user.company_name or current_user.username}</p>
                </div>
            </body>
            </html>
            """

            mail.send(msg)

            # Log notification
            notification = EmailNotification(
                user_id=current_user.id,
                recipient_email=job.client_email,
                subject=msg.subject,
                body=msg.html,
                notification_type='pos_quote_sent',
                related_id=pos_quote.id,
                status='sent',
                sent_date=datetime.utcnow()
            )
            db.session.add(notification)

            # Update quote status
            pos_quote.status = 'sent'
            db.session.commit()

            return jsonify({
                'success': True,
                'message': f'Quote sent to {job.client_email}'
            })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Failed to send quote: {str(e)}'
        }), 500

@app.route("/api/pos/quotes/<int:quote_id>/accept", methods=['POST'])
@login_required
def accept_pos_quote(quote_id):
    """Accept a POS quote and update job accordingly"""
    pos_quote = POSQuote.query.filter_by(id=quote_id, user_id=current_user.id).first_or_404()

    # Update quote status
    pos_quote.status = 'accepted'

    # Update linked job if exists
    if pos_quote.job_id:
        job = Job.query.get(pos_quote.job_id)
        if job:
            # Update job budget with quote total
            job.budget = pos_quote.total_amount
            # Update job status to active
            if job.status == 'pending':
                job.status = 'active'

    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Quote accepted and job updated'
    })

@app.route("/api/pos/quotes/<int:quote_id>/accept-and-contract", methods=['POST'])
@login_required
def accept_quote_and_generate_contract(quote_id):
    """Accept POS quote and automatically generate contract"""
    pos_quote = POSQuote.query.filter_by(id=quote_id, user_id=current_user.id).first_or_404()

    if not pos_quote.job_id:
        return jsonify({
            'success': False,
            'message': 'Quote must be linked to a job to generate contract'
        }), 400

    try:
        job = Job.query.get(pos_quote.job_id)
        if not job or job.user_id != current_user.id:
            return jsonify({
                'success': False,
                'message': 'Job not found or access denied'
            }), 404

        # Accept the quote
        pos_quote.status = 'accepted'
        job.budget = pos_quote.total_amount
        if job.status == 'pending':
            job.status = 'active'

        # Generate contract with POS data
        if LLM_AVAILABLE and llm_service:
            # Build project data
            project_data = {
                'name': job.project_type or 'Renovation Project',
                'client_name': job.client_name,
                'budget_estimate': pos_quote.total_amount,
                'raw_scope': pos_quote.project_description or f"Complete {job.project_type} project as specified in POS quote {pos_quote.quote_number}"
            }

            # Analyze scope
            analysis = llm_service.analyze_scope(project_data['raw_scope'])

            # Get all quotes for this job (including this one)
            pos_quotes = POSQuote.query.filter_by(job_id=job.id, user_id=current_user.id).all()

            # Generate contract with POS integration
            contract_data = llm_service.generate_contract(project_data, analysis, pos_quotes)

            # Create or update contract
            contract = Contract.query.filter_by(job_id=job.id).first()
            if not contract:
                contract = Contract(
                    job_id=job.id,
                    contract_number=f"CON-{datetime.now().strftime('%Y%m%d')}-{job.id:04d}",
                    title=f"Construction Contract - {job.client_name}"
                )
                db.session.add(contract)

            contract.introduction_text = contract_data.get('introduction', '')
            contract.scope_of_work = contract_data.get('scope_section', '')
            contract.terms_and_conditions = contract_data.get('terms_conditions', '')
            contract.payment_terms = contract_data.get('payment_terms', '')
            contract.total_contract_value = pos_quote.total_amount
            contract.status = 'draft'

            # Generate tasks from scope analysis
            tasks_created = 0
            try:
                tasks_data = llm_service.generate_task_list(project_data, analysis)

                for task_info in tasks_data:
                    task = Task(
                        job_id=job.id,
                        task_name=task_info.get('name', 'Unnamed Task'),
                        task_description=task_info.get('description', ''),
                        estimated_days=task_info.get('duration_days', 1),
                        status='not_started',
                        is_critical_path=task_info.get('is_critical_path', False),
                        included_in_contract=True,
                        priority=task_info.get('priority', 3)
                    )
                    db.session.add(task)
                    tasks_created += 1

                print(f"[SUCCESS] Generated {tasks_created} tasks from AI analysis")
            except Exception as task_error:
                print(f"[WARNING] Failed to generate tasks: {task_error}")
                # Continue anyway - contract is still created

            db.session.commit()

            return jsonify({
                'success': True,
                'message': f'Quote accepted! Contract and {tasks_created} tasks generated successfully!',
                'contract_id': contract.id,
                'tasks_created': tasks_created,
                'redirect_url': url_for('unified_contract', job_id=job.id) + '?mode=view'
            })
        else:
            db.session.commit()
            return jsonify({
                'success': True,
                'message': 'Quote accepted! LLM service not available for contract generation.',
                'redirect_url': url_for('job_detail', job_id=job.id)
            })

    except Exception as e:
        db.session.rollback()
        print(f"Error accepting quote and generating contract: {e}")
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 500

@app.route("/api/pos/quotes/<int:quote_id>/reject", methods=['POST'])
@login_required
def reject_pos_quote(quote_id):
    """Reject a POS quote"""
    pos_quote = POSQuote.query.filter_by(id=quote_id, user_id=current_user.id).first_or_404()
    pos_quote.status = 'rejected'
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Quote rejected'
    })

@app.route("/api/jobs/<int:job_id>/pos-quotes")
@login_required
def get_job_pos_quotes(job_id):
    """Get all POS quotes for a job"""
    job = Job.query.filter_by(id=job_id, user_id=current_user.id).first_or_404()
    quotes = POSQuote.query.filter_by(job_id=job_id, user_id=current_user.id).order_by(POSQuote.created_date.desc()).all()

    return jsonify([{
        'id': q.id,
        'quote_number': q.quote_number,
        'project_description': q.project_description,
        'total_amount': float(q.total_amount),
        'status': q.status,
        'created_date': q.created_date.isoformat()
    } for q in quotes])

# ============================================
# AI-POWERED FEATURES
# ============================================

@app.route("/jobs/<int:job_id>/ai-contract-generator")
@login_required
def ai_contract_generator(job_id):
    """AI-powered contract generation from scope"""
    job = Job.query.filter_by(id=job_id, user_id=current_user.id).first_or_404()

    return render_template('ai_contract_generator.html',
                         job=job,
                         llm_available=LLM_AVAILABLE)

@app.route("/api/jobs/<int:job_id>/generate-ai-contract", methods=['POST'])
@login_required
def generate_ai_contract(job_id):
    """Generate contract using LLM service"""
    if not LLM_AVAILABLE or not llm_service:
        return jsonify({
            'success': False,
            'message': 'LLM service not available. Install with: pip install openai'
        }), 400

    job = Job.query.filter_by(id=job_id, user_id=current_user.id).first_or_404()
    data = request.get_json()

    raw_scope = data.get('raw_scope', '')
    if not raw_scope:
        return jsonify({
            'success': False,
            'message': 'Please provide a scope of work'
        }), 400

    try:
        # Analyze the scope
        analysis = llm_service.analyze_scope(raw_scope)

        # Build project data
        project_data = {
            'name': job.project_type or 'Renovation Project',
            'client_name': job.client_name,
            'budget_estimate': job.budget,
            'raw_scope': raw_scope
        }

        # Get POS quotes for this job to integrate into contract
        pos_quotes = POSQuote.query.filter_by(job_id=job_id, user_id=current_user.id).all()

        # Generate contract with POS data integration
        contract_data = llm_service.generate_contract(project_data, analysis, pos_quotes)

        # Create or update contract in database
        contract = Contract.query.filter_by(job_id=job_id).first()
        if not contract:
            contract = Contract(
                job_id=job_id,
                contract_number=f"CON-{datetime.now().strftime('%Y%m%d')}-{job_id:04d}"
            )
            db.session.add(contract)

        contract.title = f"Construction Contract - {job.client_name}"
        contract.introduction_text = contract_data.get('introduction', '')
        contract.scope_of_work = contract_data.get('scope_section', '')
        contract.terms_and_conditions = contract_data.get('terms_conditions', '')
        contract.payment_terms = contract_data.get('payment_terms', '')
        contract.total_contract_value = job.budget or Decimal('0.00')

        # Store full contract text in a new field or use existing
        if hasattr(contract, 'full_contract_text'):
            contract.full_contract_text = contract_data.get('contract_text', '')

        db.session.commit()

        # Optionally generate and save tasks
        if data.get('generate_tasks', False):
            tasks = llm_service.generate_task_list(project_data, analysis)

            for task_data in tasks:
                task = Task(
                    job_id=job_id,
                    task_name=task_data['name'],
                    task_description=f"AI-generated task - {task_data['category']}",
                    estimated_days=task_data.get('duration_days', 1),
                    status='not_started',
                    is_critical_path=task_data.get('is_critical_path', False),
                    included_in_contract=True
                )
                db.session.add(task)

            db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Contract generated successfully!',
            'contract_id': contract.id,
            'analysis': analysis,
            'tasks_generated': data.get('generate_tasks', False)
        })

    except Exception as e:
        print(f"Error generating contract: {e}")
        return jsonify({
            'success': False,
            'message': f'Error generating contract: {str(e)}'
        }), 500

@app.route("/api/jobs/<int:job_id>/ask", methods=['POST'])
@login_required
def ask_about_job(job_id):
    """Ask AI questions about a specific job"""
    if not LLM_AVAILABLE or not llm_service:
        return jsonify({
            'success': False,
            'answer': 'AI assistant not available. Install OpenAI with: pip install openai',
            'llm_available': False
        })

    job = Job.query.filter_by(id=job_id, user_id=current_user.id).first_or_404()
    data = request.get_json()
    question = data.get('question', '').strip()

    if not question:
        return jsonify({
            'success': False,
            'answer': 'Please ask a question'
        }), 400

    try:
        # Gather comprehensive job context
        tasks = Task.query.filter_by(job_id=job_id).all()
        locations = JobLocation.query.filter_by(job_id=job_id).all()
        photos = ProgressPhoto.query.filter_by(job_id=job_id).order_by(ProgressPhoto.uploaded_date.desc()).limit(10).all()
        estimates = Estimate.query.filter_by(user_id=current_user.id, job_id=job_id).all()
        pos_quotes = POSQuote.query.filter_by(job_id=job_id, user_id=current_user.id).order_by(POSQuote.created_date.desc()).all()
        contract = Contract.query.filter_by(job_id=job_id).first()

        # Calculate task statistics
        total_tasks = len(tasks)
        completed_tasks = sum(1 for t in tasks if t.status == 'completed')
        in_progress_tasks = sum(1 for t in tasks if t.status == 'in_progress')
        total_task_cost = sum(float(t.cost or 0) for t in tasks)
        critical_path_tasks = sum(1 for t in tasks if t.is_critical_path)

        # Build enhanced context for AI
        context = f"""
=== JOB OVERVIEW ===
Client: {job.client_name}
Project: {job.project_type or 'Not specified'}
Address: {job.address or 'Not specified'}
Status: {job.status.upper()}
Build Type: {job.build_type or 'Not specified'}

=== PROJECT DETAILS ===
Budget: ${job.budget or 0:,.2f}
Square Footage: {job.total_square_footage or 'Not specified'} sq ft
Stories: {job.stories or 'Not specified'}
Bedrooms: {job.bedrooms or 'Not specified'}
Bathrooms: {job.bathrooms or 'Not specified'}
Start Date: {job.start_date or 'Not set'}
Completion Target: {job.expected_end_date or 'Not set'}

=== TASK SUMMARY ===
Total Tasks: {total_tasks}
Completed: {completed_tasks} ({(completed_tasks/total_tasks*100) if total_tasks else 0:.1f}%)
In Progress: {in_progress_tasks}
Critical Path Tasks: {critical_path_tasks}
Total Task Budget: ${total_task_cost:,.2f}

=== LOCATIONS ===
"""
        if locations:
            for loc in locations:
                loc_tasks = [t for t in tasks if t.location_id == loc.id]
                context += f"- {loc.name}"
                if loc.square_footage:
                    context += f" ({loc.square_footage} sq ft)"
                context += f" - {len(loc_tasks)} tasks\n"
        else:
            context += "No locations defined\n"

        context += f"\n=== DETAILED TASKS ===\n"
        for i, task in enumerate(tasks[:20], 1):  # Show up to 20 tasks
            context += f"{i}. {task.task_name} - Status: {task.status.upper()}"
            if task.cost:
                context += f" - Cost: ${task.cost:,.2f}"
            if task.estimated_days:
                context += f" - Duration: {task.estimated_days} days"
            if task.scheduled_start_date and task.scheduled_end_date:
                context += f" - Scheduled: {task.scheduled_start_date.strftime('%m/%d')} to {task.scheduled_end_date.strftime('%m/%d')}"
            if task.is_critical_path:
                context += " [CRITICAL PATH]"
            if task.assigned_to:
                context += f" - Assigned: {task.assigned_to}"
            context += "\n"
            if task.task_description:
                context += f"   Description: {task.task_description[:150]}\n"

        if total_tasks > 20:
            context += f"... and {total_tasks - 20} more tasks\n"

        if photos:
            context += f"\n=== PROGRESS TRACKING ===\n"
            context += f"Photos Uploaded: {len(photos)}\n"
            recent_photo = photos[0]
            if recent_photo.milestone_percentage:
                context += f"Latest Progress: {recent_photo.milestone_percentage}% complete\n"
                context += f"Photo Date: {recent_photo.uploaded_date.strftime('%m/%d/%Y')}\n"
            if recent_photo.location:
                context += f"Latest Photo Location: {recent_photo.location}\n"

        if estimates:
            context += f"\n=== ESTIMATES ===\n"
            for est in estimates[:3]:
                context += f"- {est.estimate_number}: ${est.total_cost or 0:,.2f} ({est.status})\n"
                if est.description:
                    context += f"  Description: {est.description[:100]}\n"

        if pos_quotes:
            context += f"\n=== POS QUOTES ===\n"
            import json
            for quote in pos_quotes[:3]:
                context += f"- Quote #{quote.quote_number}: ${quote.total_amount:,.2f} ({quote.status})\n"
                if quote.project_description:
                    context += f"  Description: {quote.project_description[:100]}\n"

                # Include line item summary
                try:
                    line_items = json.loads(quote.line_items) if quote.line_items else []
                    if line_items:
                        context += f"  Items: {len(line_items)} line items\n"
                        for item in line_items[:3]:
                            activity = item.get('activity_name') or item.get('activity') or item.get('name') or 'Item'
                            total = item.get('total', 0)
                            category = item.get('category_name', '')
                            if category:
                                context += f"    - {category}: {activity} - ${total:,.2f}\n"
                            else:
                                context += f"    - {activity} - ${total:,.2f}\n"
                except Exception as e:
                    print(f"[WARNING] Error parsing POS line items: {e}")
                    pass

        if contract:
            context += f"\n=== CONTRACT ===\n"
            context += f"Contract Number: {contract.contract_number}\n"
            context += f"Contract Value: ${contract.total_contract_value or 0:,.2f}\n"
            if contract.signed_date:
                context += f"Signed: {contract.signed_date.strftime('%m/%d/%Y')}\n"
            context += f"Status: {contract.status}\n"

        # Use OpenAI if available
        print(f"[DEBUG] llm_service exists: {llm_service is not None}")
        if llm_service:
            print(f"[DEBUG] llm_service.use_openai: {llm_service.use_openai}")

        if hasattr(llm_service, 'use_openai') and llm_service.use_openai:
            print("[DEBUG] Attempting to use OpenAI API...")
            try:
                # Use modern OpenAI v1.0+ API
                from openai import OpenAI
                import os
                client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{
                        "role": "system",
                        "content": """You are an expert construction project manager and assistant with deep knowledge of:
- Project scheduling and critical path management
- Cost estimation and budget tracking
- Building codes and permit requirements
- Contractor coordination and subcontractor management
- Risk assessment and mitigation strategies

Based on the provided job context, answer questions with:
1. Specific, data-driven insights from the project data
2. Actionable recommendations when applicable
3. Industry best practices and standards
4. Realistic timelines and cost expectations
5. Risk flags and areas requiring attention

If the question requires information not in the context, clearly state that and suggest what additional information would be helpful. Always reference specific tasks, costs, or dates from the context when relevant."""
                    }, {
                        "role": "user",
                        "content": f"=== PROJECT CONTEXT ===\n{context}\n\n=== USER QUESTION ===\n{question}\n\nPlease provide a detailed, helpful answer based on the project context above."
                    }],
                    temperature=0.7,
                    max_tokens=800
                )

                answer = response.choices[0].message.content
                print(f"[DEBUG] OpenAI response received successfully!")

                return jsonify({
                    'success': True,
                    'answer': answer,
                    'llm_available': True,
                    'model_used': 'gpt-3.5-turbo'
                })
            except Exception as e:
                print(f"OpenAI error: {e}")
                # Fall through to rule-based response

        # Rule-based fallback responses
        question_lower = question.lower()

        if 'status' in question_lower or 'progress' in question_lower:
            completed_tasks = len([t for t in tasks if t.status == 'completed'])
            total_tasks = len(tasks)
            if total_tasks > 0:
                progress = (completed_tasks / total_tasks) * 100
                answer = f"The project is {progress:.1f}% complete based on tasks. {completed_tasks} of {total_tasks} tasks are completed. Current status: {job.status}."
            else:
                answer = f"No tasks have been created yet. Current job status: {job.status}."

        elif 'budget' in question_lower or 'cost' in question_lower:
            total_task_cost = sum(t.cost or 0 for t in tasks)
            answer = f"Job budget: ${job.budget or 0:,.2f}. Total task costs: ${total_task_cost:,.2f}. "
            if job.budget and total_task_cost > job.budget:
                answer += f"WARNING: Task costs exceed budget by ${total_task_cost - job.budget:,.2f}."
            elif job.budget:
                remaining = job.budget - total_task_cost
                answer += f"Remaining budget: ${remaining:,.2f}."

        elif 'task' in question_lower or 'to do' in question_lower or 'next' in question_lower:
            pending_tasks = [t for t in tasks if t.status in ['not_started', 'in_progress']]
            if pending_tasks:
                answer = f"You have {len(pending_tasks)} pending tasks:\n"
                for task in pending_tasks[:5]:
                    answer += f"- {task.task_name} ({task.status})\n"
            else:
                answer = "All tasks are completed! Great job."

        elif 'photo' in question_lower or 'picture' in question_lower:
            if photos:
                latest = photos[0]
                answer = f"There are {len(photos)} progress photos. Latest photo was uploaded on {latest.uploaded_date.strftime('%B %d, %Y')} "
                if latest.milestone_percentage:
                    answer += f"showing {latest.milestone_percentage}% completion."
            else:
                answer = "No progress photos have been uploaded yet."

        elif 'start' in question_lower or 'when' in question_lower:
            if job.start_date:
                answer = f"Project start date: {job.start_date.strftime('%B %d, %Y')}. "
                days_since = (date.today() - job.start_date).days
                if days_since > 0:
                    answer += f"Started {days_since} days ago."
                else:
                    answer += f"Starts in {abs(days_since)} days."
            else:
                answer = "No start date has been set for this project."

        elif 'quote' in question_lower or 'pos' in question_lower or 'estimate' in question_lower:
            if pos_quotes:
                answer = f"This job has {len(pos_quotes)} POS quote(s):\n\n"
                for quote in pos_quotes[:5]:
                    answer += f"Quote #{quote.quote_number}:\n"
                    answer += f"  Amount: ${quote.total_amount:,.2f}\n"
                    answer += f"  Status: {quote.status}\n"
                    answer += f"  Created: {quote.created_date.strftime('%B %d, %Y')}\n"
                    if quote.project_description:
                        answer += f"  Description: {quote.project_description[:150]}\n"
                    answer += "\n"

                # Add summary
                total_quote_value = sum(q.total_amount for q in pos_quotes)
                accepted_quotes = [q for q in pos_quotes if q.status == 'accepted']
                answer += f"Total Quote Value: ${total_quote_value:,.2f}\n"
                if accepted_quotes:
                    answer += f"Accepted Quotes: {len(accepted_quotes)}"
            elif estimates:
                answer = f"This job has {len(estimates)} estimate(s):\n\n"
                for est in estimates:
                    answer += f"Estimate {est.estimate_number}:\n"
                    answer += f"  Amount: ${est.total_cost or 0:,.2f}\n"
                    answer += f"  Status: {est.status}\n\n"
            else:
                answer = "No quotes or estimates have been created for this job yet."

        else:
            # Generic helpful response
            answer = f"""Here's what I know about this job:

Client: {job.client_name}
Project: {job.project_type or 'Renovation'}
Status: {job.status}
Budget: ${job.budget or 0:,.2f}
Tasks: {len(tasks)} total ({len([t for t in tasks if t.status == 'completed'])} completed)
POS Quotes: {len(pos_quotes)} quote(s)

You can ask me about:
- Project status and progress
- Budget and costs
- Pending tasks
- Progress photos
- Timeline and dates
- Quotes and estimates"""

        return jsonify({
            'success': True,
            'answer': answer,
            'llm_available': False,
            'model_used': 'rule-based'
        })

    except Exception as e:
        print(f"Error answering question: {e}")
        return jsonify({
            'success': False,
            'answer': f'Sorry, I encountered an error: {str(e)}'
        }), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)

