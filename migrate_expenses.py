"""
Migration script to add Expense table for job costing
"""

from app import app, db
from models import Expense

def migrate():
    with app.app_context():
        print("Creating Expense table...")
        db.create_all()
        print("[SUCCESS] Expense table created successfully!")
        print("\nYou can now track:")
        print("  - Labor costs")
        print("  - Material costs")
        print("  - Equipment costs")
        print("  - Subcontractor costs")
        print("  - Permits and fees")
        print("  - Other job expenses")

if __name__ == '__main__':
    migrate()
