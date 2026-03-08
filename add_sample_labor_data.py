"""
Add sample labor estimation data to existing tasks
"""
from app import app, db
from models import Task, Job
from decimal import Decimal

def add_sample_labor_data():
    """Add sample labor estimates to tasks"""
    with app.app_context():
        try:
            # Get all scheduled tasks
            tasks = Task.query.filter(Task.scheduled_start_date != None).all()

            if not tasks:
                print("No scheduled tasks found!")
                return

            print(f"Found {len(tasks)} scheduled tasks")
            print("Adding sample labor data...\n")

            # Labor estimates based on common construction tasks
            labor_estimates = {
                'carpet': {'hours': 16, 'workers': 2, 'rate': 35},
                'door': {'hours': 4, 'workers': 1, 'rate': 45},
                'paint': {'hours': 24, 'workers': 2, 'rate': 30},
                'drywall': {'hours': 32, 'workers': 2, 'rate': 40},
                'deck': {'hours': 40, 'workers': 3, 'rate': 35},
                'patio': {'hours': 48, 'workers': 3, 'rate': 35},
                'rail': {'hours': 16, 'workers': 2, 'rate': 35},
                'fixture': {'hours': 2, 'workers': 1, 'rate': 45},
                'shower': {'hours': 8, 'workers': 1, 'rate': 50},
                'ceiling': {'hours': 12, 'workers': 2, 'rate': 30},
            }

            updated_count = 0
            for task in tasks:
                task_lower = task.task_name.lower()

                # Find matching labor estimate
                matching_estimate = None
                for key, estimate in labor_estimates.items():
                    if key in task_lower:
                        matching_estimate = estimate
                        break

                if matching_estimate:
                    task.estimated_labor_hours = Decimal(str(matching_estimate['hours']))
                    task.number_of_workers = matching_estimate['workers']
                    task.labor_cost_per_hour = Decimal(str(matching_estimate['rate']))

                    total_cost = task.get_total_labor_cost()
                    labor_days = task.get_labor_days()

                    print(f"[OK] {task.task_name}")
                    print(f"     Labor: {task.estimated_labor_hours}hrs x ${task.labor_cost_per_hour}/hr = ${total_cost:.2f}")
                    days_str = f"{labor_days:.1f}" if labor_days else "N/A"
                    print(f"     Workers: {task.number_of_workers} | Days: {days_str}")
                    print()

                    updated_count += 1

            db.session.commit()
            print(f"\n[SUCCESS] Updated {updated_count} out of {len(tasks)} tasks with labor data!")

        except Exception as e:
            print(f"[ERROR] Failed to add labor data: {e}")
            import traceback
            traceback.print_exc()
            db.session.rollback()

if __name__ == '__main__':
    print("=" * 60)
    print("ADD SAMPLE LABOR ESTIMATION DATA")
    print("=" * 60)
    add_sample_labor_data()
