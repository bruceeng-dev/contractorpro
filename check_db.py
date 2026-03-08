from app import app, db
from models import POSQuote, Job, Task, Estimate

app.app_context().push()

quotes = POSQuote.query.order_by(POSQuote.id.desc()).limit(5).all()
print('Recent Quotes:')
for q in quotes:
    print(f'  Quote #{q.id}: Job ID={q.job_id}, Total=${q.total_amount}, Items={len(q.items)}, Status={q.status}')

jobs = Job.query.order_by(Job.id.desc()).limit(3).all()
print('\nRecent Jobs:')
for j in jobs:
    print(f'  Job #{j.id}: {j.client_name}, Tasks={len(j.tasks)}')

tasks = Task.query.order_by(Task.id.desc()).limit(10).all()
print(f'\nRecent Tasks (Total: {Task.query.count()}):')
for t in tasks:
    print(f'  Task #{t.id}: {t.task_name} (Job #{t.job_id})')

estimates = Estimate.query.order_by(Estimate.id.desc()).limit(5).all()
print(f'\nRecent Estimates:')
for e in estimates:
    print(f'  Estimate #{e.id}: {e.estimate_number} - {e.client_name}, Job ID={e.job_id}')
