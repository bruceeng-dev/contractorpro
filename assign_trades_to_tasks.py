"""
Assign trade categories to existing tasks based on task names
"""
from app import app, db
from models import Task, TradeCategory

def assign_trades():
    """Assign trade categories to tasks based on keywords in task names"""
    with app.app_context():
        try:
            # Get all trade categories
            trades = {trade.name.lower(): trade for trade in TradeCategory.query.all()}

            # Keyword mapping to trades
            trade_keywords = {
                'framing': ['framing', 'frame'],
                'electrical': ['electrical', 'electric', 'wiring', 'outlet', 'fixture'],
                'plumbing': ['plumbing', 'plumb', 'pipe', 'drain', 'water'],
                'hvac': ['hvac', 'heating', 'cooling', 'vent', 'air conditioning'],
                'drywall': ['drywall', 'sheetrock', 'gypsum'],
                'flooring': ['flooring', 'floor', 'carpet', 'tile', 'hardwood', 'laminate'],
                'painting': ['paint', 'stain', 'finish'],
                'roofing': ['roof', 'shingle', 'gutter'],
                'carpentry': ['door', 'cabinet', 'trim', 'molding', 'woodwork', 'deck'],
                'masonry': ['brick', 'stone', 'concrete', 'mason', 'patio', 'paver'],
                'landscaping': ['landscape', 'lawn', 'tree', 'garden', 'irrigation'],
            }

            # Get all tasks
            tasks = Task.query.all()
            updated_count = 0

            for task in tasks:
                if task.trade_category_id:
                    continue  # Skip if already assigned

                task_lower = task.task_name.lower()

                # Find matching trade
                assigned_trade = None
                for trade_name, keywords in trade_keywords.items():
                    for keyword in keywords:
                        if keyword in task_lower:
                            assigned_trade = trade_name
                            break
                    if assigned_trade:
                        break

                if assigned_trade and assigned_trade in trades:
                    task.trade_category_id = trades[assigned_trade].id
                    updated_count += 1
                    print(f"[OK] {task.task_name} -> {trades[assigned_trade].name}")
                else:
                    # Assign to General if no match
                    if 'general' in trades:
                        task.trade_category_id = trades['general'].id
                        updated_count += 1
                        print(f"[OK] {task.task_name} -> General")

            db.session.commit()
            print(f"\n[SUCCESS] Updated {updated_count} tasks with trade categories!")

        except Exception as e:
            print(f"[ERROR] Failed to assign trades: {e}")
            import traceback
            traceback.print_exc()
            db.session.rollback()

if __name__ == '__main__':
    print("=" * 60)
    print("ASSIGN TRADE CATEGORIES TO TASKS")
    print("=" * 60)
    assign_trades()
