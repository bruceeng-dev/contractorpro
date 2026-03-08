#!/usr/bin/env python3
"""
Seed demo tasks with scheduled dates for calendar/gantt demo
"""
from datetime import datetime, timedelta
from flask import Flask
from models import db, User, Job, Task, JobLocation
from config import config
import os

def create_app():
    app = Flask(__name__)
    config_name = os.environ.get('FLASK_ENV', 'development')
    app.config.from_object(config[config_name])
    db.init_app(app)
    return app

def seed_demo_tasks():
    app = create_app()

    with app.app_context():
        # Get admin user
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            print("[ERROR] Admin user not found. Run 'python migrate.py init' first")
            return

        print("Seeding demo tasks for calendar/gantt...")
        print("-" * 60)

        # Create or get sample jobs
        job1 = Job.query.filter_by(client_name="Sarah Johnson", user_id=admin.id).first()
        if not job1:
            job1 = Job(
                user_id=admin.id,
                client_name="Sarah Johnson",
                client_email="sarah.johnson@email.com",
                client_phone="(555) 123-4567",
                project_type="Kitchen Remodel",
                address="123 Oak Street, Springfield, IL 62701",
                description="Complete kitchen renovation with new cabinets, countertops, and appliances",
                budget=45000,
                status="active"
            )
            db.session.add(job1)
            db.session.flush()
            print(f"[OK] Created job: {job1.client_name} - {job1.project_type}")
        else:
            print(f"[OK] Using existing job: {job1.client_name} - {job1.project_type}")

        job2 = Job.query.filter_by(client_name="Michael Davis", user_id=admin.id).first()
        if not job2:
            job2 = Job(
                user_id=admin.id,
                client_name="Michael Davis",
                client_email="michael.davis@email.com",
                client_phone="(555) 987-6543",
                project_type="Bathroom Addition",
                address="456 Maple Avenue, Springfield, IL 62702",
                description="Master bathroom addition with walk-in shower and dual vanity",
                budget=32000,
                status="active"
            )
            db.session.add(job2)
            db.session.flush()
            print(f"[OK] Created job: {job2.client_name} - {job2.project_type}")
        else:
            print(f"[OK] Using existing job: {job2.client_name} - {job2.project_type}")

        # Create location for job1
        location1 = JobLocation.query.filter_by(job_id=job1.id, name="Kitchen").first()
        if not location1:
            location1 = JobLocation(job_id=job1.id, name="Kitchen", description="Main kitchen area")
            db.session.add(location1)
            db.session.flush()

        # Create location for job2
        location2 = JobLocation.query.filter_by(job_id=job2.id, name="Master Bathroom").first()
        if not location2:
            location2 = JobLocation(job_id=job2.id, name="Master Bathroom", description="New master bathroom")
            db.session.add(location2)
            db.session.flush()

        # Clear existing tasks for clean demo
        Task.query.filter_by(job_id=job1.id).delete()
        Task.query.filter_by(job_id=job2.id).delete()
        db.session.commit()

        print("\nCreating scheduled tasks...")

        # Get today's date and calculate start dates
        today = datetime.now().date()

        # Job 1: Kitchen Remodel (Starting in 3 days, spanning 3 weeks)
        start_date = today + timedelta(days=3)

        kitchen_tasks = [
            {
                'name': 'Demolition & Removal',
                'days': 2,
                'critical': True,
                'description': 'Remove old cabinets, countertops, and appliances',
                'order': 1
            },
            {
                'name': 'Electrical Rough-in',
                'days': 2,
                'critical': True,
                'description': 'Install new electrical wiring and outlets',
                'order': 2
            },
            {
                'name': 'Plumbing Rough-in',
                'days': 2,
                'critical': True,
                'description': 'Install new plumbing lines for sink and dishwasher',
                'order': 3
            },
            {
                'name': 'Drywall Repair',
                'days': 1,
                'critical': False,
                'description': 'Patch and repair drywall from demolition',
                'order': 4
            },
            {
                'name': 'Cabinet Installation',
                'days': 3,
                'critical': True,
                'description': 'Install new custom cabinets',
                'order': 5
            },
            {
                'name': 'Countertop Installation',
                'days': 1,
                'critical': True,
                'description': 'Install granite countertops',
                'order': 6
            },
            {
                'name': 'Backsplash Tile',
                'days': 2,
                'critical': False,
                'description': 'Install ceramic tile backsplash',
                'order': 7
            },
            {
                'name': 'Painting',
                'days': 2,
                'critical': False,
                'description': 'Paint walls and trim',
                'order': 8
            },
            {
                'name': 'Appliance Installation',
                'days': 1,
                'critical': True,
                'description': 'Install refrigerator, stove, and dishwasher',
                'order': 9
            },
            {
                'name': 'Final Inspection',
                'days': 1,
                'critical': True,
                'description': 'Final walkthrough and punch list',
                'order': 10
            }
        ]

        current_date = start_date
        for task_data in kitchen_tasks:
            task = Task(
                job_id=job1.id,
                location_id=location1.id,
                task_name=task_data['name'],
                task_description=task_data['description'],
                estimated_days=task_data['days'],
                scheduled_start_date=current_date,
                scheduled_end_date=current_date + timedelta(days=task_data['days'] - 1),
                is_critical_path=task_data['critical'],
                status='not_started',
                order_index=task_data['order']
            )
            db.session.add(task)
            print(f"  [OK] {task_data['name']}: {current_date.strftime('%m/%d')} - {(current_date + timedelta(days=task_data['days'] - 1)).strftime('%m/%d')}")
            current_date += timedelta(days=task_data['days'])

        # Job 2: Bathroom Addition (Starting in 1 week, spanning 4 weeks)
        start_date2 = today + timedelta(days=7)

        bathroom_tasks = [
            {
                'name': 'Framing',
                'days': 3,
                'critical': True,
                'description': 'Frame new bathroom addition',
                'order': 1
            },
            {
                'name': 'Roofing',
                'days': 2,
                'critical': True,
                'description': 'Install roof structure and shingles',
                'order': 2
            },
            {
                'name': 'Electrical Installation',
                'days': 2,
                'critical': True,
                'description': 'Run electrical wiring for lighting and outlets',
                'order': 3
            },
            {
                'name': 'Plumbing Installation',
                'days': 3,
                'critical': True,
                'description': 'Install plumbing for shower, toilet, and vanity',
                'order': 4
            },
            {
                'name': 'HVAC Ductwork',
                'days': 1,
                'critical': False,
                'description': 'Extend HVAC ductwork to new bathroom',
                'order': 5
            },
            {
                'name': 'Insulation',
                'days': 1,
                'critical': False,
                'description': 'Install insulation in walls and ceiling',
                'order': 6
            },
            {
                'name': 'Drywall Installation',
                'days': 2,
                'critical': True,
                'description': 'Hang and finish drywall',
                'order': 7
            },
            {
                'name': 'Tile Work',
                'days': 4,
                'critical': True,
                'description': 'Install floor and shower tile',
                'order': 8
            },
            {
                'name': 'Vanity & Fixtures',
                'days': 2,
                'critical': True,
                'description': 'Install vanity, toilet, and fixtures',
                'order': 9
            },
            {
                'name': 'Painting',
                'days': 2,
                'critical': False,
                'description': 'Paint walls and ceiling',
                'order': 10
            },
            {
                'name': 'Final Fixtures & Inspection',
                'days': 1,
                'critical': True,
                'description': 'Install accessories and final inspection',
                'order': 11
            }
        ]

        current_date2 = start_date2
        print("\n  Bathroom Addition Tasks:")
        for task_data in bathroom_tasks:
            task = Task(
                job_id=job2.id,
                location_id=location2.id,
                task_name=task_data['name'],
                task_description=task_data['description'],
                estimated_days=task_data['days'],
                scheduled_start_date=current_date2,
                scheduled_end_date=current_date2 + timedelta(days=task_data['days'] - 1),
                is_critical_path=task_data['critical'],
                status='not_started',
                order_index=task_data['order']
            )
            db.session.add(task)
            print(f"  [OK] {task_data['name']}: {current_date2.strftime('%m/%d')} - {(current_date2 + timedelta(days=task_data['days'] - 1)).strftime('%m/%d')}")
            current_date2 += timedelta(days=task_data['days'])

        # Add some unscheduled tasks
        print("\nCreating unscheduled tasks...")
        unscheduled = [
            Task(
                job_id=job1.id,
                location_id=location1.id,
                task_name="Hardware Installation",
                task_description="Install cabinet pulls and knobs",
                estimated_days=1,
                status='not_started',
                order_index=11
            ),
            Task(
                job_id=job2.id,
                location_id=location2.id,
                task_name="Mirror & Accessories",
                task_description="Install mirror and bathroom accessories",
                estimated_days=1,
                status='not_started',
                order_index=12
            )
        ]

        for task in unscheduled:
            db.session.add(task)
            print(f"  [OK] {task.task_name} (unscheduled)")

        db.session.commit()

        print("\n" + "=" * 60)
        print("DEMO TASKS SEEDED SUCCESSFULLY!")
        print("=" * 60)
        print("\nYou can now test:")
        print("  - Calendar view: http://localhost:5000/calendar")
        print("  - Gantt chart: http://localhost:5000/gantt")
        print("  - Task list: http://localhost:5000/tasks")
        print("\nJobs span the next 4-5 weeks with realistic task scheduling")
        print("Critical path tasks are marked for priority")

if __name__ == '__main__':
    seed_demo_tasks()
