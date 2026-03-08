"""
Clear all jobs, tasks, contracts, estimates, quotes, and leads from the database
Keeps POS categories/activities and user accounts intact
"""
from app import app
from models import db, Job, ProgressPhoto, Document, Estimate, EstimateLineItem, Task, Contract, JobLocation, POSQuote, POSQuoteItem, Lead, EmailNotification, ContractTemplate

def clear_all_jobs():
    """Delete all jobs and related data"""
    with app.app_context():
        try:
            print("=" * 60)
            print("CLEARING ALL JOBS, TASKS, CONTRACTS & QUOTES")
            print("=" * 60)

            # Count records before deletion
            jobs_count = Job.query.count()
            tasks_count = Task.query.count()
            contracts_count = Contract.query.count()
            estimates_count = Estimate.query.count()
            quotes_count = POSQuote.query.count()
            leads_count = Lead.query.count()
            templates_count = ContractTemplate.query.count()

            print(f"\nFound:")
            print(f"  - {jobs_count} jobs")
            print(f"  - {tasks_count} tasks")
            print(f"  - {contracts_count} contracts")
            print(f"  - {estimates_count} estimates")
            print(f"  - {quotes_count} POS quotes")
            print(f"  - {leads_count} leads")
            print(f"  - {templates_count} contract templates")

            # Delete child records first
            print("\nDeleting email notifications...")
            EmailNotification.query.delete()

            print("Deleting progress photos...")
            ProgressPhoto.query.delete()

            print("Deleting documents...")
            Document.query.delete()

            print("Deleting estimate line items...")
            EstimateLineItem.query.delete()

            print("Deleting POS quote items...")
            POSQuoteItem.query.delete()

            print("Deleting tasks...")
            Task.query.delete()

            print("Deleting contracts...")
            Contract.query.delete()

            print("Deleting estimates...")
            Estimate.query.delete()

            print("Deleting POS quotes...")
            POSQuote.query.delete()

            print("Deleting leads...")
            Lead.query.delete()

            print("Deleting contract templates (custom terminology)...")
            ContractTemplate.query.delete()

            print("Deleting job locations...")
            JobLocation.query.delete()

            print("Deleting jobs...")
            Job.query.delete()

            db.session.commit()

            print("\n" + "=" * 60)
            print("DELETION COMPLETE!")
            print("=" * 60)
            print(f"\nDeleted:")
            print(f"  - {jobs_count} jobs")
            print(f"  - {tasks_count} tasks")
            print(f"  - {contracts_count} contracts")
            print(f"  - {estimates_count} estimates")
            print(f"  - {quotes_count} POS quotes")
            print(f"  - {leads_count} leads")
            print(f"  - {templates_count} contract templates")
            print("\nKEPT INTACT:")
            print("  [OK] User accounts")
            print("  [OK] POS categories and activities")
            print("  [OK] POS sub-items")
            print("\nYou can now create fresh quotes to test the intelligent task system!")
            print("=" * 60)

        except Exception as e:
            db.session.rollback()
            print(f"Error deleting records: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    print("This will delete ALL jobs, tasks, contracts, estimates, quotes, and leads.")
    print("Your POS categories/activities and user account will be preserved.")
    confirm = input("\nAre you sure? (yes/no): ")
    if confirm.lower() == 'yes':
        clear_all_jobs()
    else:
        print("Operation cancelled")
