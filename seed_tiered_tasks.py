"""
Create sample jobs and tasks with tiered trade assignments for testing.
"""

from sqlalchemy import create_engine, text
from config import Config
from datetime import datetime, timedelta

def seed_tasks():
    """Create sample jobs and tasks with trade assignments"""

    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)

    with engine.connect() as conn:
        # Get user ID
        result = conn.execute(text("SELECT id FROM user WHERE username = 'admin'"))
        user_id = result.fetchone()[0]

        # Get trade categories
        result = conn.execute(text("SELECT id, name, tier FROM trade_category ORDER BY tier, order_index"))
        trades = {row[1]: {'id': row[0], 'tier': row[2]} for row in result}

        # Create a sample job
        conn.execute(text("""
            INSERT INTO job (user_id, client_name, client_email, client_phone, project_type,
                           address, start_date, status, budget, created_date)
            VALUES (:user_id, :client_name, :client_email, :client_phone, :project_type,
                   :address, :start_date, :status, :budget, :created_date)
        """), {
            'user_id': user_id,
            'client_name': 'Johnson Residence',
            'client_email': 'johnson@example.com',
            'client_phone': '555-0123',
            'project_type': 'Full Home Renovation',
            'address': '123 Main St, Anytown, USA',
            'start_date': datetime.now(),
            'status': 'active',
            'budget': 250000.00,
            'created_date': datetime.now()
        })

        # Get the job ID
        result = conn.execute(text("SELECT id FROM job WHERE client_name = 'Johnson Residence'"))
        job_id = result.fetchone()[0]

        print(f"\nCreated job: Johnson Residence (ID: {job_id})")
        print(f"\nCreating tasks organized by tier...\n")

        # Define tasks by tier
        tasks_by_tier = {
            1: [  # Critical Path / Schedule Killers
                ('Site Preparation & Excavation', 'Sitework & Foundation', 5, True),
                ('Foundation Pour', 'Sitework & Foundation', 3, True),
                ('Electrical Panel Upgrade', 'Electrical', 2, True),
                ('Main Electrical Rough-In', 'Electrical', 4, False),
                ('Plumbing Rough-In', 'Plumbing', 4, True),
                ('Water Supply Line Installation', 'Plumbing', 2, False),
                ('Roof Tear-Off & Preparation', 'Roofing', 3, True),
                ('New Roof Installation', 'Roofing', 4, False),
            ],
            2: [  # High Risk / Delay Amplifiers
                ('Wall Framing', 'Framing', 6, True),
                ('Floor Framing & Joists', 'Framing', 4, False),
                ('HVAC Ductwork Installation', 'HVAC', 5, True),
                ('HVAC Unit Installation', 'HVAC', 2, False),
                ('Brick Veneer Installation', 'Masonry', 8, False),
                ('Stone Fireplace Construction', 'Masonry', 5, False),
            ],
            3: [  # Compressible / Stackable
                ('Wall & Ceiling Insulation', 'Insulation', 3, False),
                ('Drywall Hanging', 'Drywall', 4, False),
                ('Drywall Taping & Mudding', 'Drywall', 5, False),
                ('Interior Door Installation', 'Carpentry', 2, False),
                ('Custom Cabinet Installation', 'Carpentry', 3, False),
                ('Crown Molding & Trim', 'Carpentry', 4, False),
                ('Tile Backsplash Installation', 'Interior Finishes', 2, False),
                ('Countertop Installation', 'Interior Finishes', 1, False),
            ],
            4: [  # Low Criticality / End-Game
                ('Hardwood Flooring Installation', 'Flooring', 4, False),
                ('Carpet Installation', 'Flooring', 2, False),
                ('Interior Painting', 'Painting', 6, False),
                ('Exterior Painting', 'Painting', 4, False),
                ('Final Walkthrough & Punchlist', 'Final & Cleanup', 1, False),
                ('Deep Cleaning', 'Final & Cleanup', 2, False),
                ('Landscaping & Lawn Installation', 'Landscaping', 5, False),
                ('Driveway Sealing', 'Landscaping', 1, False),
            ]
        }

        tier_emoji = {1: '[T1]', 2: '[T2]', 3: '[T3]', 4: '[T4]'}
        task_count = 0

        # Insert tasks
        start_date = datetime.now() + timedelta(days=7)

        for tier in [1, 2, 3, 4]:
            print(f"\n{tier_emoji[tier]} Tier {tier} Tasks:")
            print("-" * 70)

            for task_name, trade_name, duration, is_critical in tasks_by_tier[tier]:
                trade_id = trades[trade_name]['id']

                conn.execute(text("""
                    INSERT INTO task (job_id, task_name, task_description, estimated_days,
                                    is_critical_path, status, trade_category_id,
                                    estimated_labor_hours, number_of_workers, labor_cost_per_hour,
                                    scheduled_start_date, scheduled_end_date)
                    VALUES (:job_id, :task_name, :description, :estimated_days,
                           :is_critical, :status, :trade_id,
                           :labor_hours, :workers, :hourly_rate,
                           :start_date, :end_date)
                """), {
                    'job_id': job_id,
                    'task_name': task_name,
                    'description': f'{trade_name} work for {task_name}',
                    'estimated_days': duration,
                    'is_critical': is_critical,
                    'status': 'not_started',
                    'trade_id': trade_id,
                    'labor_hours': duration * 8,
                    'workers': 2 if tier == 1 else 1,
                    'hourly_rate': 75.00,
                    'start_date': start_date,
                    'end_date': start_date + timedelta(days=duration-1)
                })

                critical_flag = " [CRITICAL]" if is_critical else ""
                print(f"  {task_name[:45]:45} | {trade_name[:20]:20} | {duration}d{critical_flag}")
                task_count += 1
                start_date += timedelta(days=duration)

        conn.commit()

        print(f"\n{'='*70}")
        print(f"[OK] Created {task_count} tasks across 4 tiers!")
        print(f"{'='*70}\n")

        # Show summary
        print("Summary by Tier:")
        print(f"  Tier 1 (Critical Path): {len(tasks_by_tier[1])} tasks")
        print(f"  Tier 2 (High Risk): {len(tasks_by_tier[2])} tasks")
        print(f"  Tier 3 (Compressible): {len(tasks_by_tier[3])} tasks")
        print(f"  Tier 4 (Low Priority): {len(tasks_by_tier[4])} tasks")
        print(f"\nView the calendar at: http://localhost:5000/calendar")
        print(f"View the Gantt chart at: http://localhost:5000/gantt-chart")

if __name__ == '__main__':
    seed_tasks()
