#!/usr/bin/env python3
"""
Quick script to initialize the ContractTemplate table
Run this in the same environment where your Flask app runs
"""

from app import app, db
from models import ContractTemplate

def init_contract_templates():
    """Create the ContractTemplate table if it doesn't exist"""
    with app.app_context():
        # Create all tables (including ContractTemplate)
        db.create_all()
        print("✅ ContractTemplate table created successfully!")
        print("\nYou can now:")
        print("1. Restart your Flask app: python app.py")
        print("2. Generate a contract and edit sections")
        print("3. Your custom terminology will persist!")

if __name__ == '__main__':
    init_contract_templates()
