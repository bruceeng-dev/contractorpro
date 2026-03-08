from app import app
from models import db, Job

with app.app_context():
    with app.test_client() as client:
        print('=' * 60)
        print('CONTRACTORPRO - COMPLETE JOB CREATION WORKFLOW TEST')
        print('=' * 60)

        # Step 1: Login
        print('\n[1/4] Logging in...')
        response = client.post('/login', data={
            'username': 'admin',
            'password': 'admin123'
        }, follow_redirects=True)
        if response.status_code == 200:
            print('  [OK] Login successful')
        else:
            print(f'  [ERROR] Login failed: {response.status_code}')
            exit(1)

        # Step 2: Create a new job
        print('\n[2/4] Creating new job...')
        job_count_before = Job.query.count()

        response = client.post('/jobs/new', data={
            'client_name': 'Workflow Test Client',
            'project_type': 'Kitchen Remodel',
            'address': '5555 Test Workflow Street',
            'start_date': '2026-04-01',
            'budget': '45000',
            'build_type': 'remodel',
            'stories': '1',
            'bedrooms': '3',
            'bathrooms': '2',
            'description': 'Complete kitchen remodel with new cabinets and appliances'
        }, follow_redirects=False)

        if response.status_code == 302:
            print('  [OK] Job created, redirecting...')
        else:
            print(f'  [ERROR] Job creation failed: {response.status_code}')
            exit(1)

        # Step 3: Verify job was created
        print('\n[3/4] Verifying job in database...')
        job_count_after = Job.query.count()
        latest_job = Job.query.order_by(Job.id.desc()).first()

        if job_count_after > job_count_before and latest_job:
            print(f'  [OK] Job #{latest_job.id} created successfully')
            print(f'    Client: {latest_job.client_name}')
            print(f'    Project: {latest_job.project_type}')
            print(f'    Budget: ${latest_job.budget:,.2f}')
            print(f'    Address: {latest_job.address}')
        else:
            print('  [ERROR] Job not found in database')
            exit(1)

        # Step 4: Test viewing job detail
        print('\n[4/4] Testing job detail page...')
        response = client.get(f'/jobs/{latest_job.id}')

        if response.status_code == 200:
            print('  [OK] Job detail page loads correctly')
        else:
            print(f'  [ERROR] Job detail page failed: {response.status_code}')
            exit(1)

        # Final summary
        print('\n' + '=' * 60)
        print('[SUCCESS] ALL TESTS PASSED!')
        print('=' * 60)
        print(f'\nTotal jobs in system: {job_count_after}')
        print('\nJob creation workflow is fully functional!')
        print('You can now:')
        print('  1. Visit http://localhost:5000')
        print('  2. Login with admin/admin123')
        print('  3. Create new jobs successfully')
        print('  4. View job details without errors')
        print('=' * 60)
