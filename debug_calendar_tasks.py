from app import app, db
from models import Task, Job
from datetime import datetime

app.app_context().push()

# Get all jobs
all_jobs = Job.query.all()
print("=" * 60)
print("ALL JOBS IN DATABASE:")
print("=" * 60)
for job in all_jobs:
    print(f"\nJob #{job.id}: {job.client_name} - {job.project_type}")

    # Get tasks for this job
    scheduled = Task.query.filter(Task.job_id == job.id, Task.scheduled_start_date != None).all()
    unscheduled = Task.query.filter(Task.job_id == job.id, Task.scheduled_start_date == None).all()

    print(f"  Scheduled tasks: {len(scheduled)}")
    for task in scheduled:
        print(f"    - {task.task_name} ({task.scheduled_start_date} to {task.scheduled_end_date})")

    print(f"  Unscheduled tasks: {len(unscheduled)}")
    for task in unscheduled:
        print(f"    - {task.task_name}")

print("\n" + "=" * 60)
print("SUMMARY:")
print("=" * 60)
total_scheduled = Task.query.filter(Task.scheduled_start_date != None).count()
total_unscheduled = Task.query.filter(Task.scheduled_start_date == None).count()
print(f"Total scheduled tasks across all jobs: {total_scheduled}")
print(f"Total unscheduled tasks across all jobs: {total_unscheduled}")
