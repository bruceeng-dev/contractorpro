"""
Migration script to reorganize trade categories into 4 tiers based on criticality.

Tier 1: Critical Path / Schedule Killers
Tier 2: High Risk / Delay Amplifiers
Tier 3: Compressible / Stackable
Tier 4: Low Criticality / End-Game
"""

from sqlalchemy import create_engine, text
from config import Config

def migrate_trade_tiers():
    """Add tier fields and reorganize trade categories"""

    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)

    with engine.connect() as conn:
        # Check if trade_category table exists
        result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='trade_category'"))
        table_exists = result.fetchone() is not None

        if not table_exists:
            print("Creating trade_category table...")
            conn.execute(text("""
                CREATE TABLE trade_category (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR(100) NOT NULL,
                    description TEXT,
                    icon VARCHAR(50),
                    color VARCHAR(20),
                    tier INTEGER DEFAULT 4,
                    tier_label VARCHAR(50),
                    order_index INTEGER DEFAULT 1,
                    is_active BOOLEAN DEFAULT 1,
                    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            conn.commit()
            existing_columns = []
        else:
            # Check if tier column exists
            result = conn.execute(text("PRAGMA table_info(trade_category)"))
            existing_columns = [row[1] for row in result]

        # Add tier and tier_label columns if they don't exist
        if 'tier' not in existing_columns and table_exists:
            print("Adding tier column...")
            conn.execute(text("ALTER TABLE trade_category ADD COLUMN tier INTEGER DEFAULT 4"))
            conn.commit()
        else:
            print("[OK] tier column already exists")

        if 'tier_label' not in existing_columns and table_exists:
            print("Adding tier_label column...")
            conn.execute(text("ALTER TABLE trade_category ADD COLUMN tier_label VARCHAR(50)"))
            conn.commit()
        else:
            print("[OK] tier_label column already exists")

        # Clear existing trade categories (this will also clear task assignments due to foreign key)
        print("\nClearing existing trade categories...")
        conn.execute(text("DELETE FROM trade_category"))
        conn.commit()

        # Define trades organized by tier
        trades = [
            # Tier 1 - Critical Path / Schedule Killers (Red)
            {'name': 'Sitework & Foundation', 'color': '#8B0000', 'icon': '🏗️', 'tier': 1, 'tier_label': 'Critical Path / Schedule Killers', 'order': 1},
            {'name': 'Electrical', 'color': '#DC143C', 'icon': '⚡', 'tier': 1, 'tier_label': 'Critical Path / Schedule Killers', 'order': 2},
            {'name': 'Plumbing', 'color': '#B22222', 'icon': '🚰', 'tier': 1, 'tier_label': 'Critical Path / Schedule Killers', 'order': 3},
            {'name': 'Roofing', 'color': '#8B1A1A', 'icon': '🏠', 'tier': 1, 'tier_label': 'Critical Path / Schedule Killers', 'order': 4},

            # Tier 2 - High Risk / Delay Amplifiers (Orange)
            {'name': 'Framing', 'color': '#FF8C00', 'icon': '🏗️', 'tier': 2, 'tier_label': 'High Risk / Delay Amplifiers', 'order': 5},
            {'name': 'HVAC', 'color': '#FF6347', 'icon': '❄️', 'tier': 2, 'tier_label': 'High Risk / Delay Amplifiers', 'order': 6},
            {'name': 'Masonry', 'color': '#D2691E', 'icon': '🧱', 'tier': 2, 'tier_label': 'High Risk / Delay Amplifiers', 'order': 7},

            # Tier 3 - Compressible / Stackable (Yellow)
            {'name': 'Insulation', 'color': '#FFD700', 'icon': '🧊', 'tier': 3, 'tier_label': 'Compressible / Stackable', 'order': 8},
            {'name': 'Drywall', 'color': '#DAA520', 'icon': '🧱', 'tier': 3, 'tier_label': 'Compressible / Stackable', 'order': 9},
            {'name': 'Carpentry', 'color': '#B8860B', 'icon': '🪚', 'tier': 3, 'tier_label': 'Compressible / Stackable', 'order': 10},
            {'name': 'Interior Finishes', 'color': '#F0E68C', 'icon': '🎨', 'tier': 3, 'tier_label': 'Compressible / Stackable', 'order': 11},

            # Tier 4 - Low Criticality / End-Game (Green)
            {'name': 'Flooring', 'color': '#90EE90', 'icon': '📏', 'tier': 4, 'tier_label': 'Low Criticality / End-Game', 'order': 12},
            {'name': 'Painting', 'color': '#98FB98', 'icon': '🎨', 'tier': 4, 'tier_label': 'Low Criticality / End-Game', 'order': 13},
            {'name': 'Final & Cleanup', 'color': '#8FBC8F', 'icon': '✨', 'tier': 4, 'tier_label': 'Low Criticality / End-Game', 'order': 14},
            {'name': 'Landscaping', 'color': '#228B22', 'icon': '🌳', 'tier': 4, 'tier_label': 'Low Criticality / End-Game', 'order': 15},
            {'name': 'General', 'color': '#A9A9A9', 'icon': '🔧', 'tier': 4, 'tier_label': 'Low Criticality / End-Game', 'order': 99},
        ]

        # Insert new trade categories
        print("\nCreating tiered trade categories...")
        for trade in trades:
            conn.execute(text("""
                INSERT INTO trade_category (name, color, icon, tier, tier_label, order_index, is_active)
                VALUES (:name, :color, :icon, :tier, :tier_label, :order, 1)
            """), {
                'name': trade['name'],
                'color': trade['color'],
                'icon': trade['icon'],
                'tier': trade['tier'],
                'tier_label': trade['tier_label'],
                'order': trade['order']
            })
            print(f"  [Tier {trade['tier']}] {trade['name']}")

        conn.commit()

        print("\n" + "="*60)
        print("[OK] Trade categories reorganized into 4 tiers!")
        print("="*60)
        print("\nTier 1 (Critical Path): 4 trades")
        print("Tier 2 (High Risk): 3 trades")
        print("Tier 3 (Compressible): 4 trades")
        print("Tier 4 (Low Criticality): 5 trades")
        print("\nNOTE: Existing tasks have been unassigned from trades.")
        print("      You may need to reassign trades to tasks.")

if __name__ == '__main__':
    migrate_trade_tiers()
