from app import app
from models import db, Job

with app.app_context():
    with app.test_client() as client:
        # Login
        client.post('/login', data={
            'username': 'admin',
            'password': 'admin123'
        })

        # Test creating a new job
        print('Testing complete job creation flow...')
        print('=' * 50)

        job_count_before = Job.query.count()

        response = client.post('/jobs/new', data={
            'client_name': 'Complete Test Client',
            'project_type': 'Home Addition',
            'address': '1234 Working Ave',
            'start_date': '2026-03-01',
            'budget': '125000',
            'build_type': 'new_build',
            'stories': '2',
            'bedrooms': '3',
            'bathrooms': '2.5',
            'description': 'Two-story home addition'
        }, follow_redirects=True)

        job_count_after = Job.query.count()

        print(f'Jobs before: {job_count_before}')
        print(f'Jobs after: {job_count_after}')
        print(f'HTTP Status: {response.status_code}')

        if response.status_code == 200 and job_count_after > job_count_before:
            latest_job = Job.query.order_by(Job.id.desc()).first()
            print(f'')
            print('SUCCESS! Job created:')
            print(f'  ID: {latest_job.id}')
            print(f'  Client: {latest_job.client_name}')
            print(f'  Project: {latest_job.project_type}')
            print(f'  Budget: ${latest_job.budget:,.2f}')
            print(f'  Address: {latest_job.address}')
            print(f'')
            print('Job detail page loaded successfully!')
        else:
            print(f'ERROR: Job creation failed')
            print(f'Status: {response.status_code}')
