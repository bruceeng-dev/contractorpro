"""
Migration script to add Smart Forms tables (ChangeOrder, LienWaiver, WorkAuthorization)
"""
from app import app
from models import db

def migrate():
    with app.app_context():
        print("Adding Smart Forms tables...")

        try:
            # Create the new tables
            db.create_all()

            print("\nSuccessfully created tables:")
            print("  - change_order (Change Orders)")
            print("  - lien_waiver (Lien Waivers)")
            print("  - work_authorization (Work Authorizations)")
            print("\nSmart Forms migration complete!")

        except Exception as e:
            print(f"Error during migration: {e}")
            raise

if __name__ == '__main__':
    migrate()
