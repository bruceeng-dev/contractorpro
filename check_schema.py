#!/usr/bin/env python3
from flask import Flask
from models import db
from config import config
from sqlalchemy import inspect

def check_schema():
    app = Flask(__name__)
    app.config.from_object(config['development'])
    db.init_app(app)
    
    with app.app_context():
        inspector = inspect(db.engine)
        
        # Check job table columns
        job_columns = [col['name'] for col in inspector.get_columns('job')]
        print("Job table columns:")
        for col in job_columns:
            print(f"  - {col}")
            
        # Check if our new columns exist
        new_columns = ['build_type', 'total_square_footage', 'permit_required']
        missing_columns = [col for col in new_columns if col not in job_columns]
        
        if missing_columns:
            print(f"\nMissing columns: {missing_columns}")
            return False
        else:
            print(f"\nAll new columns present: {new_columns}")
            return True

if __name__ == '__main__':
    check_schema()