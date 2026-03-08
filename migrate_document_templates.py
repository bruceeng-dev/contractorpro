"""
Migration script to add DocumentTemplate table to database
"""
from app import app, db
from models import DocumentTemplate

def migrate():
    with app.app_context():
        print("Creating DocumentTemplate table...")
        try:
            # Create the table
            db.create_all()
            print("DocumentTemplate table created successfully!")

            # Verify table exists
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()

            if 'document_template' in tables:
                print("✓ Verified: document_template table exists")

                # Show columns
                columns = inspector.get_columns('document_template')
                print("\nColumns in document_template:")
                for col in columns:
                    print(f"  - {col['name']}: {col['type']}")
            else:
                print("✗ Error: document_template table not found!")

        except Exception as e:
            print(f"Error during migration: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    migrate()
