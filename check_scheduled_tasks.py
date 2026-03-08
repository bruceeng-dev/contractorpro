from app import app, db
from models import Task, Job
from datetime import datetime

app.app_context().push()

# Check all scheduled tasks
scheduled = Task.query.filter(Task.scheduled_start_date != None).all()
print(f"Total scheduled tasks: {len(scheduled)}\n")

for task in scheduled:
    job = Job.query.get(task.job_id)
    print(f"Task #{task.id}: {task.task_name}")
    print(f"  Job: {job.client_name if job else 'N/A'}")
    print(f"  Start: {task.scheduled_start_date}")
    print(f"  End: {task.scheduled_end_date}")
    print(f"  Duration: {task.estimated_days} days")
    print()

# Check unscheduled tasks
unscheduled = Task.query.filter(Task.scheduled_start_date == None).all()
print(f"\nUnscheduled tasks: {len(unscheduled)}")
for task in unscheduled:
    job = Job.query.get(task.job_id)
    print(f"  - {task.task_name} (Job: {job.client_name if job else 'N/A'})")
