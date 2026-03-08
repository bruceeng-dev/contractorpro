from app import app, db
from models import Task, Job
from datetime import datetime

app.app_context().push()

# Check all tasks
all_tasks = Task.query.all()
print(f"Total tasks in database: {len(all_tasks)}")

# Check scheduled vs unscheduled
scheduled = Task.query.filter(Task.scheduled_start_date != None).all()
unscheduled = Task.query.filter(Task.scheduled_start_date == None).all()

print(f"\nScheduled tasks: {len(scheduled)}")
for task in scheduled:
    print(f"  - {task.task_name}: {task.scheduled_start_date} to {task.scheduled_end_date}")

print(f"\nUnscheduled tasks: {len(unscheduled)}")
for task in unscheduled:
    print(f"  - {task.task_name} (Job #{task.job_id}, Est: {task.estimated_days} days)")
