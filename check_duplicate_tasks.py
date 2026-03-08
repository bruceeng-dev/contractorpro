from app import app, db
from models import Task, Job

app.app_context().push()

# Get Job #8
job_id = 8
job = Job.query.get(job_id)

if not job:
    print(f"Job #{job_id} not found!")
    exit()

print(f"Checking tasks for Job #{job_id}: {job.client_name}")
print("=" * 80)

# Get ALL tasks for this job
all_tasks = Task.query.filter_by(job_id=job_id).all()

print(f"\nTotal tasks: {len(all_tasks)}\n")

# Group by task name to find duplicates
from collections import defaultdict
tasks_by_name = defaultdict(list)

for task in all_tasks:
    tasks_by_name[task.task_name].append(task)

# Show all tasks with their IDs and schedule status
print("TASK DETAILS:")
print("-" * 80)
for task_name, tasks in sorted(tasks_by_name.items()):
    if len(tasks) > 1:
        print(f"\n[!] DUPLICATE: '{task_name}' ({len(tasks)} instances)")
    else:
        print(f"\n[ ] '{task_name}'")

    for task in tasks:
        status = "SCHEDULED" if task.scheduled_start_date else "UNSCHEDULED"
        dates = ""
        if task.scheduled_start_date:
            dates = f" | {task.scheduled_start_date} to {task.scheduled_end_date}"
        print(f"    ID: {task.id:3d} | {status:12s}{dates}")
