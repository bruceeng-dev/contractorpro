#!/usr/bin/env python3
"""
Clean database creation script
Forces complete recreation with all new models
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

def create_fresh_db():
    """Create a completely fresh database"""
    app = create_app()
    
    with app.app_context():
        print("Creating fresh database with all tables...")
        
        # Drop all existing tables first
        db.drop_all()
        print("Dropped all existing tables")
        
        # Create all tables from current models
        db.create_all()
        print("Created all tables from current models")
        
        # Verify tables were created by checking inspector
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"\nCreated tables: {tables}")
        
        # Create admin user
        admin_user = User(
            username='admin',
            email='admin@contractorpro.com',
            company_name='Demo Construction Co.'
        )
        admin_user.set_password('admin123')
        db.session.add(admin_user)
        db.session.commit()
        
        print(f"\nCreated admin user:")
        print(f"Username: admin")
        print(f"Password: admin123")
        
        print("\nDatabase setup complete!")

if __name__ == '__main__':
    create_fresh_db()