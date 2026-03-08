"""
Migration script to add trade_category_id to Task table and seed trade categories
"""
from app import app, db
from models import TradeCategory
from sqlalchemy import text

def seed_trade_categories():
    """Create default trade categories if they don't exist"""
    trades = [
        {'name': 'Framing', 'color': '#8B4513', 'icon': '🏗️', 'order': 1},
        {'name': 'Electrical', 'color': '#FFD700', 'icon': '⚡', 'order': 2},
        {'name': 'Plumbing', 'color': '#4682B4', 'icon': '🚰', 'order': 3},
        {'name': 'HVAC', 'color': '#87CEEB', 'icon': '❄️', 'order': 4},
        {'name': 'Drywall', 'color': '#D3D3D3', 'icon': '🧱', 'order': 5},
        {'name': 'Flooring', 'color': '#CD853F', 'icon': '📏', 'order': 6},
        {'name': 'Painting', 'color': '#FF6347', 'icon': '🎨', 'order': 7},
        {'name': 'Roofing', 'color': '#696969', 'icon': '🏠', 'order': 8},
        {'name': 'Carpentry', 'color': '#8B7355', 'icon': '🪚', 'order': 9},
        {'name': 'Masonry', 'color': '#A9A9A9', 'icon': '🧱', 'order': 10},
        {'name': 'Landscaping', 'color': '#228B22', 'icon': '🌳', 'order': 11},
        {'name': 'General', 'color': '#808080', 'icon': '🔧', 'order': 99},
    ]

    created_count = 0
    for trade_data in trades:
        existing = TradeCategory.query.filter_by(name=trade_data['name']).first()
        if not existing:
            trade = TradeCategory(
                name=trade_data['name'],
                color=trade_data['color'],
                icon=trade_data['icon'],
                order_index=trade_data['order'],
                description=f"{trade_data['name']} trade category"
            )
            db.session.add(trade)
            created_count += 1
            print(f"[OK] Created trade category: {trade_data['name']} ({trade_data['color']})")
        else:
            print(f"[SKIP] Trade category already exists: {trade_data['name']}")

    if created_count > 0:
        db.session.commit()
        print(f"\n[SUCCESS] Created {created_count} new trade categories!")
    else:
        print(f"\n[INFO] All trade categories already exist")

def add_trade_field():
    """Add trade_category_id column to Task table"""
    with db.engine.connect() as conn:
        # Check if column already exists
        result = conn.execute(text("PRAGMA table_info(task)"))
        existing_columns = [row[1] for row in result]

        if 'trade_category_id' not in existing_columns:
            print("Adding trade_category_id column to task table...")
            conn.execute(text("ALTER TABLE task ADD COLUMN trade_category_id INTEGER REFERENCES trade_category(id)"))
            conn.commit()
            print("[OK] Added trade_category_id column")
        else:
            print("[OK] trade_category_id column already exists")

if __name__ == '__main__':
    with app.app_context():
        try:
            print("=" * 60)
            print("TRADE CATEGORY MIGRATION")
            print("=" * 60)
            print("\nStep 1: Adding trade_category_id field to tasks...")
            add_trade_field()

            print("\nStep 2: Seeding trade categories...")
            seed_trade_categories()

            print("\n" + "=" * 60)
            print("[SUCCESS] Migration completed successfully!")
            print("=" * 60)

        except Exception as e:
            print(f"\n[ERROR] Migration failed: {e}")
            import traceback
            traceback.print_exc()
