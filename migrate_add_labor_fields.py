"""
Migration script to add labor estimation fields to Task table
"""
from app import app, db
from sqlalchemy import text

def add_labor_fields():
    """Add labor estimation fields to Task table"""
    with app.app_context():
        try:
            # Add the new columns
            with db.engine.connect() as conn:
                # Check if columns already exist
                result = conn.execute(text("PRAGMA table_info(task)"))
                existing_columns = [row[1] for row in result]

                if 'estimated_labor_hours' not in existing_columns:
                    print("Adding estimated_labor_hours column...")
                    conn.execute(text("ALTER TABLE task ADD COLUMN estimated_labor_hours DECIMAL(8, 2)"))
                    conn.commit()
                    print("[OK] Added estimated_labor_hours")
                else:
                    print("[OK] estimated_labor_hours already exists")

                if 'number_of_workers' not in existing_columns:
                    print("Adding number_of_workers column...")
                    conn.execute(text("ALTER TABLE task ADD COLUMN number_of_workers INTEGER DEFAULT 1"))
                    conn.commit()
                    print("[OK] Added number_of_workers")
                else:
                    print("[OK] number_of_workers already exists")

                if 'labor_cost_per_hour' not in existing_columns:
                    print("Adding labor_cost_per_hour column...")
                    conn.execute(text("ALTER TABLE task ADD COLUMN labor_cost_per_hour DECIMAL(8, 2)"))
                    conn.commit()
                    print("[OK] Added labor_cost_per_hour")
                else:
                    print("[OK] labor_cost_per_hour already exists")

            print("\n[SUCCESS] Migration completed successfully!")
            print("\nNew fields added to Task table:")
            print("  - estimated_labor_hours: Total person-hours needed")
            print("  - number_of_workers: Number of workers needed")
            print("  - labor_cost_per_hour: Hourly rate for labor cost calculation")

        except Exception as e:
            print(f"\n[ERROR] Migration failed: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    print("=" * 60)
    print("LABOR ESTIMATION FIELDS MIGRATION")
    print("=" * 60)
    add_labor_fields()
