from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from decimal import Decimal
from sqlalchemy import DECIMAL
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    company_name = db.Column(db.String(200))
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    jobs = db.relationship('Job', backref='user', lazy=True)
    leads = db.relationship('Lead', backref='user', lazy=True)
    estimates = db.relationship('Estimate', backref='user', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    client_name = db.Column(db.String(200), nullable=False)
    client_email = db.Column(db.String(120))
    client_phone = db.Column(db.String(20))
    project_type = db.Column(db.String(100), nullable=False)
    address = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.Date)
    expected_end_date = db.Column(db.Date)
    budget = db.Column(DECIMAL(12, 2))
    actual_cost = db.Column(DECIMAL(12, 2))
    status = db.Column(db.String(20), default='pending')
    priority = db.Column(db.Integer, default=1)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # New Build vs Remodel Classification
    build_type = db.Column(db.String(20), default='remodel')  # 'new_build' or 'remodel'
    
    # Dimensional Information
    total_square_footage = db.Column(DECIMAL(10, 2))
    lot_square_footage = db.Column(DECIMAL(10, 2))
    linear_footage = db.Column(DECIMAL(10, 2))
    stories = db.Column(db.Integer, default=1)
    bedrooms = db.Column(db.Integer)
    bathrooms = db.Column(DECIMAL(3, 1))  # Allow half baths like 2.5
    
    # Additional Project Details
    permit_required = db.Column(db.Boolean, default=False)
    permit_number = db.Column(db.String(50))
    permit_status = db.Column(db.String(20), default='pending')  # pending, submitted, approved, expired
    
    # Relationships
    progress_photos = db.relationship('ProgressPhoto', backref='job', lazy=True, cascade='all, delete-orphan')
    documents = db.relationship('Document', backref='job', lazy=True, cascade='all, delete-orphan')
    estimates = db.relationship('Estimate', backref='job', lazy=True)
    locations = db.relationship('JobLocation', backref='job', lazy=True, cascade='all, delete-orphan')
    tasks = db.relationship('Task', backref='job', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Job {self.client_name} - {self.project_type}>'

class Lead(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    project_type = db.Column(db.String(100))
    address = db.Column(db.Text)
    budget_range = db.Column(db.String(50))
    timeline = db.Column(db.String(100))
    lead_source = db.Column(db.String(100))
    status = db.Column(db.String(20), default='new')
    priority = db.Column(db.Integer, default=1)
    notes = db.Column(db.Text)
    follow_up_date = db.Column(db.Date)
    converted_job_id = db.Column(db.Integer, db.ForeignKey('job.id'))
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Lead {self.name} - {self.project_type}>'

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    file_size = db.Column(db.Integer)
    mime_type = db.Column(db.String(100))
    document_type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    uploaded_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Document {self.filename}>'

class ProgressPhoto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    photo_type = db.Column(db.String(50))  # before, progress, after, issue
    caption = db.Column(db.Text)
    taken_date = db.Column(db.Date)
    location = db.Column(db.String(200))
    is_milestone = db.Column(db.Boolean, default=False)
    milestone_percentage = db.Column(db.Integer)
    uploaded_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ProgressPhoto {self.filename}>'

class Estimate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'))
    estimate_number = db.Column(db.String(50), unique=True, nullable=False)
    client_name = db.Column(db.String(200), nullable=False)
    project_description = db.Column(db.Text)
    labor_cost = db.Column(DECIMAL(12, 2), default=0)
    material_cost = db.Column(DECIMAL(12, 2), default=0)
    equipment_cost = db.Column(DECIMAL(12, 2), default=0)
    overhead_percentage = db.Column(DECIMAL(5, 2), default=10.0)
    profit_percentage = db.Column(DECIMAL(5, 2), default=15.0)
    total_cost = db.Column(DECIMAL(12, 2))
    status = db.Column(db.String(20), default='draft')  # draft, sent, accepted, rejected
    valid_until = db.Column(db.Date)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    line_items = db.relationship('EstimateLineItem', backref='estimate', lazy=True, cascade='all, delete-orphan')
    
    def calculate_total(self):
        subtotal = self.labor_cost + self.material_cost + self.equipment_cost
        overhead = subtotal * (self.overhead_percentage / 100)
        profit = (subtotal + overhead) * (self.profit_percentage / 100)
        self.total_cost = subtotal + overhead + profit
        return self.total_cost
    
    def __repr__(self):
        return f'<Estimate {self.estimate_number}>'

class EstimateLineItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    estimate_id = db.Column(db.Integer, db.ForeignKey('estimate.id'), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    category = db.Column(db.String(100))  # labor, material, equipment, other
    quantity = db.Column(DECIMAL(10, 2), default=1)
    unit = db.Column(db.String(20))  # sqft, hour, each, etc.
    unit_cost = db.Column(DECIMAL(10, 2), nullable=False)
    total_cost = db.Column(DECIMAL(12, 2))
    notes = db.Column(db.Text)
    
    def calculate_total(self):
        self.total_cost = self.quantity * self.unit_cost
        return self.total_cost
    
    def __repr__(self):
        return f'<EstimateLineItem {self.description}>'

class EmailNotification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipient_email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    body = db.Column(db.Text)
    notification_type = db.Column(db.String(50))  # job_update, estimate_sent, etc.
    related_id = db.Column(db.Integer)  # ID of related job, estimate, etc.
    status = db.Column(db.String(20), default='pending')  # pending, sent, failed
    sent_date = db.Column(db.DateTime)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<EmailNotification {self.subject}>'

class JobLocation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)  # Main Level, Lower Level, Bathroom, Kitchen, Roof
    description = db.Column(db.Text)
    square_footage = db.Column(DECIMAL(10, 2))
    order_index = db.Column(db.Integer, default=1)  # For ordering locations in contract
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    tasks = db.relationship('Task', backref='location', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<JobLocation {self.name}>'

class TaskTemplate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    location_type = db.Column(db.String(100), nullable=False)  # Kitchen, Bathroom, Roof, etc.
    task_name = db.Column(db.String(200), nullable=False)
    task_description = db.Column(db.Text, nullable=False)  # Pre-written verbiage
    default_cost = db.Column(DECIMAL(12, 2))
    estimated_days = db.Column(db.Integer)
    category = db.Column(db.String(50))  # demolition, installation, finishing, etc.
    is_active = db.Column(db.Boolean, default=True)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<TaskTemplate {self.task_name}>'

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('job_location.id'))
    task_name = db.Column(db.String(200), nullable=False)
    task_description = db.Column(db.Text)
    cost = db.Column(DECIMAL(12, 2))

    # Task Management Fields
    assigned_to = db.Column(db.String(100))  # Worker or subcontractor name
    priority = db.Column(db.Integer, default=1)  # 1-5 scale
    estimated_days = db.Column(db.Integer)
    actual_days = db.Column(db.Integer)
    is_critical_path = db.Column(db.Boolean, default=False)

    # Status and Scheduling
    status = db.Column(db.String(20), default='not_started')  # not_started, in_progress, completed, on_hold
    scheduled_start_date = db.Column(db.Date)
    scheduled_end_date = db.Column(db.Date)
    actual_start_date = db.Column(db.Date)
    actual_end_date = db.Column(db.Date)

    # Contract Integration
    included_in_contract = db.Column(db.Boolean, default=False)
    order_index = db.Column(db.Integer, default=1)  # Order within location

    # POS Quote Integration
    pos_quote_id = db.Column(db.Integer, db.ForeignKey('pos_quote.id'))
    pos_line_item_data = db.Column(db.Text)  # JSON data for the specific line item from POS quote

    # Metadata
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Task {self.task_name}>'
    
    def get_duration_days(self):
        """Calculate actual or estimated duration"""
        if self.actual_start_date and self.actual_end_date:
            return (self.actual_end_date - self.actual_start_date).days + 1
        elif self.scheduled_start_date and self.scheduled_end_date:
            return (self.scheduled_end_date - self.scheduled_start_date).days + 1
        return self.estimated_days or 1

    def get_pos_line_item(self):
        """Parse and return POS line item data as dict"""
        if self.pos_line_item_data:
            import json
            try:
                return json.loads(self.pos_line_item_data)
            except:
                return None
        return None

class Contract(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    contract_number = db.Column(db.String(50), unique=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)

    # Contract Content
    introduction_text = db.Column(db.Text)
    scope_of_work = db.Column(db.Text)
    terms_and_conditions = db.Column(db.Text)
    payment_terms = db.Column(db.Text)
    warranty_info = db.Column(db.Text)

    # Financial Summary
    total_contract_value = db.Column(DECIMAL(12, 2))

    # Status
    status = db.Column(db.String(20), default='draft')  # draft, sent, signed, executed
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    signed_date = db.Column(db.DateTime)

    # Relationships
    job = db.relationship('Job', backref='contracts')

    def __repr__(self):
        return f'<Contract {self.contract_number}>'

    def calculate_total_value(self):
        """Calculate total from included tasks"""
        total = Decimal('0.00')
        tasks = Task.query.filter_by(job_id=self.job_id, included_in_contract=True).all()
        for task in tasks:
            if task.cost:
                total += task.cost
        self.total_contract_value = total
        return total

# ============================================================================
# POS (Point of Sale) Multi-Layer System Models
# ============================================================================

class JobSpecification(db.Model):
    """28 standard construction job specifications for filtering POS categories"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    display_name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    order_index = db.Column(db.Integer, default=1)
    is_active = db.Column(db.Boolean, default=True)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<JobSpecification {self.display_name}>'

class POSCategory(db.Model):
    """Categories for organizing POS activities (Kitchen, Bathroom, etc.)"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    icon = db.Column(db.String(50))  # Emoji or icon class
    keywords = db.Column(db.Text)  # Comma-separated for search
    is_active = db.Column(db.Boolean, default=True)
    order_index = db.Column(db.Integer, default=1)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    activities = db.relationship('POSActivity', backref='category', lazy=True, cascade='all, delete-orphan')
    spec_mappings = db.relationship('POSCategorySpecMapping', backref='category', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<POSCategory {self.name}>'

class POSActivity(db.Model):
    """Individual activities/line items within a category"""
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('pos_category.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    base_cost = db.Column(DECIMAL(12, 2), nullable=False)
    unit = db.Column(db.String(20), default='each')  # each, sqft, lnft, hour, etc.
    has_subitems = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    order_index = db.Column(db.Integer, default=1)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    subitems = db.relationship('POSSubitem', backref='activity', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<POSActivity {self.name}>'

class POSSubitem(db.Model):
    """Sub-options for activities (e.g., different cabinet styles)"""
    id = db.Column(db.Integer, primary_key=True)
    activity_id = db.Column(db.Integer, db.ForeignKey('pos_activity.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    price_adjustment = db.Column(DECIMAL(12, 2), default=0)  # +/- from base cost
    is_default = db.Column(db.Boolean, default=False)
    order_index = db.Column(db.Integer, default=1)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<POSSubitem {self.name}>'

class POSCategorySpecMapping(db.Model):
    """Maps categories to job specifications for filtering"""
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('pos_category.id'), nullable=False)
    spec_id = db.Column(db.Integer, db.ForeignKey('job_specification.id'), nullable=False)
    specific_activity_ids = db.Column(db.Text)  # JSON array (optional fine-grained filtering)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    specification = db.relationship('JobSpecification', backref='category_mappings')

    def __repr__(self):
        return f'<POSCategorySpecMapping Cat:{self.category_id} Spec:{self.spec_id}>'

class POSSession(db.Model):
    """Tracks user's POS session and job spec selections"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'))  # Optional link to job
    session_token = db.Column(db.String(100), unique=True, nullable=False)
    selected_spec_ids = db.Column(db.Text)  # JSON array of spec IDs
    current_layer = db.Column(db.Integer, default=1)  # 1 = specs, 2 = categories/activities
    current_category_id = db.Column(db.Integer, db.ForeignKey('pos_category.id'))
    project_description = db.Column(db.Text)
    cart_data = db.Column(db.Text)  # JSON array of cart items
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    # Relationships
    user = db.relationship('User', backref='pos_sessions')
    job = db.relationship('Job', backref='pos_sessions')
    current_category = db.relationship('POSCategory', foreign_keys=[current_category_id])

    def __repr__(self):
        return f'<POSSession {self.session_token}>'

class POSQuote(db.Model):
    """Saved quotes from POS system"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'))
    quote_number = db.Column(db.String(50), unique=True, nullable=False)
    client_name = db.Column(db.String(200), nullable=False)
    project_description = db.Column(db.Text)
    selected_spec_ids = db.Column(db.Text)  # JSON array of job spec IDs
    line_items = db.Column(db.Text)  # JSON array of selected activities/quantities
    subtotal = db.Column(DECIMAL(12, 2))
    tax_rate = db.Column(DECIMAL(5, 2), default=0)
    tax_amount = db.Column(DECIMAL(12, 2))
    total_amount = db.Column(DECIMAL(12, 2))
    status = db.Column(db.String(20), default='draft')  # draft, sent, accepted, rejected
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = db.relationship('User', backref='pos_quotes')
    job = db.relationship('Job', backref='pos_quotes')
    tasks = db.relationship('Task', backref='pos_quote', lazy=True)

    def __repr__(self):
        return f'<POSQuote {self.quote_number}>'