"""
Reassign trade categories to existing tasks based on task names.
Uses the new tiered trade system.
"""

from sqlalchemy import create_engine, text
from config import Config

def reassign_trades():
    """Assign trade categories to tasks based on keywords in task names"""

    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)

    with engine.connect() as conn:
        # Get all trade categories
        result = conn.execute(text("SELECT id, name, tier FROM trade_category"))
        trades = {row[1]: {'id': row[0], 'tier': row[2]} for row in result}

        # Keyword mappings for trade assignment
        keyword_mapping = {
            'Sitework & Foundation': ['foundation', 'excavation', 'grading', 'sitework', 'concrete slab', 'footing'],
            'Electrical': ['electrical', 'wiring', 'outlet', 'panel', 'lighting', 'electric'],
            'Plumbing': ['plumbing', 'pipe', 'drain', 'water', 'sewer', 'fixture'],
            'Roofing': ['roof', 'shingle', 'gutter', 'flashing'],
            'Framing': ['framing', 'frame', 'stud', 'joist', 'beam', 'structural'],
            'HVAC': ['hvac', 'heating', 'cooling', 'air conditioning', 'furnace', 'ductwork'],
            'Masonry': ['masonry', 'brick', 'stone', 'block', 'concrete wall'],
            'Insulation': ['insulation', 'insulate'],
            'Drywall': ['drywall', 'sheetrock', 'gypsum'],
            'Carpentry': ['door', 'window', 'trim', 'cabinet', 'carpentry', 'molding', 'baseboard'],
            'Interior Finishes': ['finish', 'tile', 'backsplash', 'countertop'],
            'Flooring': ['floor', 'flooring', 'hardwood', 'laminate', 'carpet', 'vinyl'],
            'Painting': ['paint', 'primer', 'stain'],
            'Final & Cleanup': ['cleanup', 'final inspection', 'punchlist', 'clean'],
            'Landscaping': ['landscape', 'landscaping', 'lawn', 'sod', 'plants', 'yard'],
        }

        # Get all tasks
        result = conn.execute(text("SELECT id, task_name FROM task"))
        tasks = list(result)

        print(f"\nProcessing {len(tasks)} tasks...\n")

        assigned_count = 0
        for task_id, task_name in tasks:
            task_name_lower = task_name.lower()
            assigned_trade = None

            # Try to match keywords
            for trade_name, keywords in keyword_mapping.items():
                if any(keyword in task_name_lower for keyword in keywords):
                    assigned_trade = trade_name
                    break

            # Default to General if no match
            if not assigned_trade:
                assigned_trade = 'General'

            # Assign the trade
            if assigned_trade in trades:
                trade_id = trades[assigned_trade]['id']
                tier = trades[assigned_trade]['tier']

                conn.execute(text(
                    "UPDATE task SET trade_category_id = :trade_id WHERE id = :task_id"
                ), {'trade_id': trade_id, 'task_id': task_id})

                tier_emoji = {1: '[T1]', 2: '[T2]', 3: '[T3]', 4: '[T4]'}
                print(f"{tier_emoji[tier]} {task_name[:50]:50} -> {assigned_trade}")
                assigned_count += 1

        conn.commit()

        print(f"\n{'='*70}")
        print(f"[OK] Assigned trades to {assigned_count} tasks!")
        print(f"{'='*70}\n")

        # Show summary by tier
        result = conn.execute(text("""
            SELECT tc.tier, COUNT(*) as count
            FROM task t
            JOIN trade_category tc ON t.trade_category_id = tc.id
            GROUP BY tc.tier
            ORDER BY tc.tier
        """))

        tier_counts = {1: 0, 2: 0, 3: 0, 4: 0}
        for tier, count in result:
            tier_counts[tier] = count

        print("Tasks by Tier:")
        print(f"  Tier 1 (Critical Path): {tier_counts[1]} tasks")
        print(f"  Tier 2 (High Risk): {tier_counts[2]} tasks")
        print(f"  Tier 3 (Compressible): {tier_counts[3]} tasks")
        print(f"  Tier 4 (Low Priority): {tier_counts[4]} tasks")

if __name__ == '__main__':
    reassign_trades()
