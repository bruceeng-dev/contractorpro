from app import app, db
from models import Task, Job
from datetime import datetime
import calendar as cal

app.app_context().push()

# Simulate viewing Job #8's calendar for December 2025
job_id = 8
month = 12
year = 2025

print("=" * 60)
print(f"SIMULATING CALENDAR VIEW FOR JOB #{job_id}")
print(f"Month: {cal.month_name[month]} {year}")
print("=" * 60)

# Get the job
job = Job.query.get(job_id)
if job:
    print(f"\nJob: {job.client_name} - {job.project_type}")
else:
    print(f"\n⚠️ Job #{job_id} not found!")
    exit()

# Get tasks for this job (matching the calendar_view route logic)
scheduled_tasks = Task.query.filter(
    Task.job_id == job_id,
    Task.scheduled_start_date != None
).all()

unscheduled_tasks = Task.query.filter(
    Task.job_id == job_id,
    Task.scheduled_start_date == None
).all()

print(f"\nScheduled tasks: {len(scheduled_tasks)}")
print(f"Unscheduled tasks: {len(unscheduled_tasks)}")

# Check which days should show tasks
print(f"\n" + "=" * 60)
print("CALENDAR GRID - DECEMBER 2025")
print("=" * 60)

_, num_days = cal.monthrange(year, month)

for day in range(1, num_days + 1):
    current_day_date = f'{year:04d}-{month:02d}-{day:02d}'
    day_tasks = []

    for task in scheduled_tasks:
        if task.scheduled_start_date and task.scheduled_end_date:
            task_start = task.scheduled_start_date.strftime('%Y-%m-%d')
            task_end = task.scheduled_end_date.strftime('%Y-%m-%d')

            if current_day_date >= task_start and current_day_date <= task_end:
                day_tasks.append(task)

    if day_tasks:
        print(f"\nDay {day} ({current_day_date}):")
        for task in day_tasks:
            is_start = task.scheduled_start_date.strftime('%Y-%m-%d') == current_day_date
            marker = "START" if is_start else "CONT"
            print(f"  [{marker}] {task.task_name}")

print("\n" + "=" * 60)
print("UNSCHEDULED TASKS (Should appear in sidebar):")
print("=" * 60)
for task in unscheduled_tasks:
    print(f"  - {task.task_name}")
