from app import app, db
from models import POSQuote, Job

app.app_context().push()

quote = POSQuote.query.get(1)
if quote:
    print(f"Quote #1:")
    print(f"  Job ID: {quote.job_id}")
    print(f"  Total: ${quote.total_amount}")
    print(f"  Items: {len(quote.items)}")
    print(f"  Status: {quote.status}")
    print(f"  Scope: {quote.scope_of_work[:100] if quote.scope_of_work else 'N/A'}")

    if quote.job_id:
        job = Job.query.get(quote.job_id)
        if job:
            print(f"\nLinked to Job #{job.id}:")
            print(f"  Client: {job.client_name}")
            print(f"  Address: {job.address}")
            print(f"  Type: {job.project_type}")
        else:
            print(f"\n⚠️ WARNING: Job #{quote.job_id} doesn't exist!")
    else:
        print("\n⚠️ WARNING: Quote is NOT linked to any job!")
else:
    print("Quote #1 not found!")
