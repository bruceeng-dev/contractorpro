"""Migration: Add lead_id to POSQuote table"""

from app import app, db

def migrate():
    with app.app_context():
        try:
            # Add lead_id column to pos_quote table
            with db.engine.connect() as conn:
                conn.execute(db.text("""
                    ALTER TABLE pos_quote
                    ADD COLUMN lead_id INTEGER REFERENCES lead(id)
                """))
                conn.commit()

            print("[SUCCESS] Added lead_id column to pos_quote table!")
            print("\nNow you can:")
            print("  - Create quotes directly from leads")
            print("  - Track which quotes came from which leads")
            print("  - Auto-fill client info from lead data")

        except Exception as e:
            print(f"[INFO] Migration may have already run: {e}")

if __name__ == '__main__':
    migrate()
