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

from models import db, User, Job, Lead, Document, ProgressPhoto, Estimate, EstimateLineItem, EmailNotification, JobLocation, TaskTemplate, Task, Contract
from config import config

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
    
    return render_template("dashboard.html", title="Dashboard", 
                         total_jobs=total_jobs, 
                         total_leads=total_leads,
                         active_jobs=active_jobs,
                         recent_jobs=recent_jobs,
                         recent_leads=recent_leads)

@app.route("/jobs")
@login_required
def jobs_list():
    jobs = Job.query.filter_by(user_id=current_user.id).order_by(Job.created_date.desc()).all()
    return render_template("jobs.html", title="Job Management", jobs=jobs)

@app.route("/jobs/new", methods=['GET', 'POST'])
@login_required
def new_job():
    if request.method == 'POST':
        job = Job(
            user_id=current_user.id,
            client_name=request.form['client_name'],
            project_type=request.form['project_type'],
            address=request.form['address'],
            start_date=datetime.strptime(request.form['start_date'], '%Y-%m-%d').date() if request.form['start_date'] else None,
            budget=Decimal(request.form['budget']) if request.form['budget'] else None,
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
        flash('New job created successfully!', 'success')
        return redirect(url_for('job_detail', job_id=job.id))
    return render_template("new_job.html", title="New Job")

@app.route("/jobs/<int:job_id>")
@login_required
def job_detail(job_id):
    job = Job.query.filter_by(id=job_id, user_id=current_user.id).first_or_404()
    progress_photos = ProgressPhoto.query.filter_by(job_id=job_id).order_by(ProgressPhoto.uploaded_date.desc()).all()
    documents = Document.query.filter_by(job_id=job_id).order_by(Document.uploaded_date.desc()).all()
    return render_template("job_detail.html", title=f"Job: {job.client_name}", 
                         job=job, progress_photos=progress_photos, documents=documents, date=date)

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
    return render_template("estimates.html", title="Estimates", estimates=estimates)

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

# Contract Generator Routes
@app.route("/jobs/<int:job_id>/contract")
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
                         overdue_tasks=overdue_tasks)

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
    
    # Get all scheduled tasks for the user
    scheduled_tasks = Task.query.join(Job).filter(
        Job.user_id == current_user.id,
        Task.scheduled_start_date != None
    ).all()
    
    # Get all jobs for drag-and-drop
    jobs = Job.query.filter_by(user_id=current_user.id).all()
    unscheduled_tasks = Task.query.join(Job).filter(
        Job.user_id == current_user.id,
        Task.scheduled_start_date == None
    ).all()
    
    # Generate calendar data
    _, num_days = monthrange(year, month)
    month_name = cal.month_name[month]
    
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
    # Get all jobs with their tasks for current user
    jobs_with_tasks = Job.query.filter_by(user_id=current_user.id).join(Task).distinct().all()
    
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
    
    return render_template("gantt_chart.html", title="Project Gantt Chart", project_data=project_data)

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

if __name__ == "__main__":
    app.run(debug=True)

