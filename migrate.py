#!/usr/bin/env python3
"""
Database migration script for ContractorPro
Run this to initialize or update the database schema
"""

import os
from flask import Flask
from models import db, User, Job, Lead, Document, ProgressPhoto, Estimate, EstimateLineItem, EmailNotification, JobLocation, TaskTemplate, Task, Contract
from config import config

def create_app():
    app = Flask(__name__)
    config_name = os.environ.get('FLASK_ENV', 'development')
    app.config.from_object(config[config_name])
    db.init_app(app)
    return app

def init_db():
    """Initialize the database with all tables"""
    app = create_app()
    
    with app.app_context():
        print("Creating database tables...")
        
        # Create all tables
        db.create_all()
        
        print("Database initialized successfully!")
        print("\nCreated tables:")
        print("- users")
        print("- jobs") 
        print("- leads")
        print("- documents")
        print("- progress_photos")
        print("- estimates")
        print("- estimate_line_items")
        print("- email_notifications")
        print("- job_locations")
        print("- task_templates")
        print("- tasks")
        print("- contracts")
        
        # Create a default admin user for testing
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            admin_user = User(
                username='admin',
                email='admin@contractorpro.com',
                company_name='Demo Construction Co.'
            )
            admin_user.set_password('admin123')
            db.session.add(admin_user)
            db.session.commit()
            print(f"\nCreated default admin user:")
            print(f"Username: admin")
            print(f"Password: admin123")
            print(f"Email: admin@contractorpro.com")
        else:
            print(f"\nAdmin user already exists: {admin_user.username}")
        
        print("\n✅ Database setup complete!")

def reset_db():
    """Reset the database (DROP ALL TABLES and recreate)"""
    app = create_app()
    
    with app.app_context():
        print("⚠️  WARNING: This will DELETE ALL DATA!")
        response = input("Are you sure you want to reset the database? (yes/no): ")
        
        if response.lower() != 'yes':
            print("Database reset cancelled.")
            return
        
        print("Dropping all tables...")
        db.drop_all()
        
        print("Recreating tables...")
        db.create_all()
        
        print("Database reset complete!")

def seed_sample_data():
    """Add sample data for development/testing"""
    app = create_app()
    
    with app.app_context():
        # Check if admin user exists
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            print("Please run 'python migrate.py init' first to create the admin user.")
            return
        
        print("Adding sample data...")
        
        # Sample jobs
        if Job.query.count() == 0:
            sample_jobs = [
                Job(
                    user_id=admin_user.id,
                    client_name="John Smith",
                    client_email="john@email.com",
                    client_phone="(555) 123-4567",
                    project_type="Kitchen Remodel",
                    address="123 Main St, Anytown, ST 12345",
                    description="Complete kitchen renovation with new cabinets and countertops",
                    budget=25000,
                    status="active"
                ),
                Job(
                    user_id=admin_user.id,
                    client_name="Sarah Johnson",
                    client_email="sarah@email.com",
                    client_phone="(555) 987-6543",
                    project_type="Bathroom Renovation",
                    address="456 Oak Ave, Somewhere, ST 67890",
                    description="Master bathroom renovation with tile work",
                    budget=15000,
                    status="pending"
                )
            ]
            
            for job in sample_jobs:
                db.session.add(job)
        
        # Sample leads
        if Lead.query.count() == 0:
            sample_leads = [
                Lead(
                    user_id=admin_user.id,
                    name="Mike Davis",
                    email="mike@email.com",
                    phone="(555) 555-1234",
                    project_type="Home Addition",
                    budget_range="$50k-$100k",
                    notes="Interested in adding a second story",
                    status="new"
                ),
                Lead(
                    user_id=admin_user.id,
                    name="Lisa Brown",
                    email="lisa@email.com",
                    phone="(555) 555-5678",
                    project_type="Roofing",
                    budget_range="$10k-$25k",
                    notes="Roof replacement needed due to storm damage",
                    status="contacted"
                )
            ]
            
            for lead in sample_leads:
                db.session.add(lead)
        
        # Sample estimate
        if Estimate.query.count() == 0:
            sample_estimate = Estimate(
                user_id=admin_user.id,
                estimate_number="EST-20250101-ABC123",
                client_name="John Smith",
                project_description="Kitchen Remodel - Complete renovation",
                labor_cost=8000,
                material_cost=12000,
                equipment_cost=2000,
                overhead_percentage=10.0,
                profit_percentage=15.0
            )
            sample_estimate.calculate_total()
            db.session.add(sample_estimate)
        
        db.session.commit()
        print("✅ Sample data added successfully!")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python migrate.py init       - Initialize database")
        print("  python migrate.py reset      - Reset database (deletes all data)")
        print("  python migrate.py seed       - Add sample data")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'init':
        init_db()
    elif command == 'reset':
        reset_db()
    elif command == 'seed':
        seed_sample_data()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)