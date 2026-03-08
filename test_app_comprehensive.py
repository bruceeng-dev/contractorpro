#!/usr/bin/env python3
"""
Comprehensive Test Suite for ContractorPro
Tests all major functionality and identifies issues
"""

import sys
import os
from datetime import datetime, date, timedelta
from decimal import Decimal

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models import db, User, Job, Lead, Estimate, EstimateLineItem, ProgressPhoto, Document, Task, TaskTemplate, JobLocation, Contract, JobSpecification, POSCategory, POSActivity, POSSubitem, POSQuote, POSSession

class TestResults:
    def __init__(self):
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        self.issues = []

    def add_test(self, name, passed, error=None):
        self.total_tests += 1
        if passed:
            self.passed_tests += 1
            print(f"[PASS] {name}")
        else:
            self.failed_tests += 1
            print(f"[FAIL] {name}")
            if error:
                print(f"  Error: {error}")
                self.issues.append({
                    'test': name,
                    'error': str(error)
                })

    def print_summary(self):
        print("\n" + "="*70)
        print("TEST SUMMARY")
        print("="*70)
        print(f"Total Tests: {self.total_tests}")
        print(f"Passed: {self.passed_tests}")
        print(f"Failed: {self.failed_tests}")
        print(f"Success Rate: {(self.passed_tests/self.total_tests*100):.1f}%")

        if self.issues:
            print("\n" + "="*70)
            print("ISSUES FOUND:")
            print("="*70)
            for i, issue in enumerate(self.issues, 1):
                print(f"\n{i}. {issue['test']}")
                print(f"   {issue['error']}")

def test_database_models(results):
    """Test database model integrity"""
    print("\n" + "="*70)
    print("TESTING DATABASE MODELS")
    print("="*70)

    app, _, _ = create_app()

    with app.app_context():
        # Test User model
        try:
            user = User.query.first()
            if user:
                results.add_test("User model exists and queryable", True)
            else:
                results.add_test("User model - no users found", False, "No users in database")
        except Exception as e:
            results.add_test("User model", False, e)

        # Test Job model
        try:
            jobs = Job.query.all()
            results.add_test(f"Job model ({len(jobs)} jobs found)", True)
        except Exception as e:
            results.add_test("Job model", False, e)

        # Test Lead model
        try:
            leads = Lead.query.all()
            results.add_test(f"Lead model ({len(leads)} leads found)", True)
        except Exception as e:
            results.add_test("Lead model", False, e)

        # Test Estimate model
        try:
            estimates = Estimate.query.all()
            results.add_test(f"Estimate model ({len(estimates)} estimates found)", True)
        except Exception as e:
            results.add_test("Estimate model", False, e)

        # Test POS models
        try:
            categories = POSCategory.query.all()
            results.add_test(f"POSCategory model ({len(categories)} categories found)", True)
        except Exception as e:
            results.add_test("POSCategory model", False, e)

        try:
            specs = JobSpecification.query.all()
            results.add_test(f"JobSpecification model ({len(specs)} specs found)", True)
        except Exception as e:
            results.add_test("JobSpecification model", False, e)

def test_user_authentication(results):
    """Test user authentication"""
    print("\n" + "="*70)
    print("TESTING USER AUTHENTICATION")
    print("="*70)

    app, _, _ = create_app()

    with app.app_context():
        try:
            # Test password hashing
            test_user = User(
                username="test_auth_user",
                email="test@test.com",
                company_name="Test Co"
            )
            test_user.set_password("testpass123")

            # Verify password check works
            if test_user.check_password("testpass123"):
                results.add_test("Password hashing and verification", True)
            else:
                results.add_test("Password hashing and verification", False, "Password check failed")

            # Verify wrong password fails
            if not test_user.check_password("wrongpassword"):
                results.add_test("Wrong password rejection", True)
            else:
                results.add_test("Wrong password rejection", False, "Wrong password accepted")

        except Exception as e:
            results.add_test("User authentication", False, e)

def test_job_creation(results):
    """Test job creation and data integrity"""
    print("\n" + "="*70)
    print("TESTING JOB CREATION")
    print("="*70)

    app, _, _ = create_app()

    with app.app_context():
        try:
            user = User.query.first()
            if not user:
                results.add_test("Job creation - user check", False, "No user found")
                return

            # Test creating a job
            test_job = Job(
                user_id=user.id,
                client_name="Test Client",
                project_type="Test Project",
                address="123 Test St",
                start_date=date.today(),
                budget=Decimal('50000.00'),
                build_type='remodel',
                total_square_footage=Decimal('2000.00'),
                stories=2,
                bedrooms=3,
                bathrooms=Decimal('2.5'),
                permit_required=True
            )

            db.session.add(test_job)
            db.session.commit()

            # Verify it was created
            found_job = Job.query.filter_by(client_name="Test Client").first()
            if found_job:
                results.add_test("Job creation with full fields", True)

                # Clean up
                db.session.delete(found_job)
                db.session.commit()
            else:
                results.add_test("Job creation with full fields", False, "Job not found after creation")

        except Exception as e:
            results.add_test("Job creation", False, e)

def test_estimate_calculations(results):
    """Test estimate calculations"""
    print("\n" + "="*70)
    print("TESTING ESTIMATE CALCULATIONS")
    print("="*70)

    app, _, _ = create_app()

    with app.app_context():
        try:
            user = User.query.first()
            if not user:
                results.add_test("Estimate calculation - user check", False, "No user found")
                return

            # Create test estimate
            test_estimate = Estimate(
                user_id=user.id,
                estimate_number="TEST-EST-001",
                client_name="Test Client",
                project_description="Test Project",
                labor_cost=Decimal('10000.00'),
                material_cost=Decimal('5000.00'),
                equipment_cost=Decimal('1000.00'),
                overhead_percentage=Decimal('10.0'),
                profit_percentage=Decimal('15.0')
            )

            # Calculate total
            test_estimate.calculate_total()

            # Verify calculation
            expected_subtotal = Decimal('16000.00')  # 10k + 5k + 1k
            expected_overhead = expected_subtotal * Decimal('0.10')  # 1600
            expected_profit = (expected_subtotal + expected_overhead) * Decimal('0.15')  # 2640
            expected_total = expected_subtotal + expected_overhead + expected_profit  # 20240

            if abs(test_estimate.total_cost - expected_total) < Decimal('0.01'):
                results.add_test(f"Estimate total calculation (${test_estimate.total_cost})", True)
            else:
                results.add_test("Estimate total calculation", False,
                               f"Expected ${expected_total}, got ${test_estimate.total_cost}")

            # Test line item
            line_item = EstimateLineItem(
                estimate_id=test_estimate.id,
                description="Test Item",
                category="labor",
                quantity=Decimal('10.0'),
                unit="hour",
                unit_cost=Decimal('50.00')
            )
            line_item.calculate_total()

            if line_item.total_cost == Decimal('500.00'):
                results.add_test("Line item calculation", True)
            else:
                results.add_test("Line item calculation", False,
                               f"Expected $500.00, got ${line_item.total_cost}")

        except Exception as e:
            results.add_test("Estimate calculations", False, e)

def test_task_management(results):
    """Test task management features"""
    print("\n" + "="*70)
    print("TESTING TASK MANAGEMENT")
    print("="*70)

    app, _, _ = create_app()

    with app.app_context():
        try:
            user = User.query.first()
            job = Job.query.filter_by(user_id=user.id).first()

            if not job:
                results.add_test("Task management - job check", False, "No job found")
                return

            # Create job location
            location = JobLocation(
                job_id=job.id,
                name="Kitchen",
                description="Main kitchen area",
                square_footage=Decimal('300.00'),
                order_index=1
            )
            db.session.add(location)
            db.session.commit()

            # Create task
            task = Task(
                job_id=job.id,
                location_id=location.id,
                task_name="Install Cabinets",
                task_description="Install new kitchen cabinets",
                cost=Decimal('5000.00'),
                estimated_days=5,
                priority=1,
                is_critical_path=True,
                included_in_contract=True,
                status='not_started'
            )
            db.session.add(task)
            db.session.commit()

            results.add_test("Task creation with location", True)

            # Test task duration calculation
            task.scheduled_start_date = date.today()
            task.scheduled_end_date = date.today() + timedelta(days=4)
            duration = task.get_duration_days()

            if duration == 5:
                results.add_test("Task duration calculation", True)
            else:
                results.add_test("Task duration calculation", False,
                               f"Expected 5 days, got {duration}")

            # Clean up
            db.session.delete(task)
            db.session.delete(location)
            db.session.commit()

        except Exception as e:
            results.add_test("Task management", False, e)

def test_contract_generation(results):
    """Test contract generation"""
    print("\n" + "="*70)
    print("TESTING CONTRACT GENERATION")
    print("="*70)

    app, _, _ = create_app()

    with app.app_context():
        try:
            user = User.query.first()
            job = Job.query.filter_by(user_id=user.id).first()

            if not job:
                results.add_test("Contract generation - job check", False, "No job found")
                return

            # Create contract
            contract = Contract(
                job_id=job.id,
                contract_number="TEST-CON-001",
                title=f"Construction Contract - {job.client_name}",
                introduction_text="This contract outlines the terms...",
                terms_and_conditions="Standard terms apply...",
                payment_terms="50% deposit, 50% on completion",
                warranty_info="1 year warranty on workmanship",
                status='draft'
            )
            db.session.add(contract)
            db.session.commit()

            results.add_test("Contract creation", True)

            # Test contract value calculation
            total_value = contract.calculate_total_value()
            results.add_test(f"Contract value calculation (${total_value})", True)

            # Clean up
            db.session.delete(contract)
            db.session.commit()

        except Exception as e:
            results.add_test("Contract generation", False, e)

def test_pos_system(results):
    """Test POS multi-layer system"""
    print("\n" + "="*70)
    print("TESTING POS SYSTEM")
    print("="*70)

    app, _, _ = create_app()

    with app.app_context():
        try:
            user = User.query.first()

            # Test POS Category creation
            category = POSCategory(
                user_id=user.id,
                name="Test Category",
                description="Testing category",
                icon="icon",
                keywords="test,category",
                order_index=1
            )
            db.session.add(category)
            db.session.commit()

            results.add_test("POS Category creation", True)

            # Test POS Activity creation
            activity = POSActivity(
                category_id=category.id,
                name="Test Activity",
                description="Test activity description",
                base_cost=Decimal('1000.00'),
                unit='each',
                has_subitems=True,
                order_index=1
            )
            db.session.add(activity)
            db.session.commit()

            results.add_test("POS Activity creation", True)

            # Test POS Subitem creation
            subitem = POSSubitem(
                activity_id=activity.id,
                name="Premium Option",
                description="Premium upgrade",
                price_adjustment=Decimal('250.00'),
                is_default=False,
                order_index=1
            )
            db.session.add(subitem)
            db.session.commit()

            results.add_test("POS Subitem creation", True)

            # Clean up
            db.session.delete(subitem)
            db.session.delete(activity)
            db.session.delete(category)
            db.session.commit()

        except Exception as e:
            results.add_test("POS system", False, e)

def test_relationships(results):
    """Test database relationships"""
    print("\n" + "="*70)
    print("TESTING DATABASE RELATIONSHIPS")
    print("="*70)

    app, _, _ = create_app()

    with app.app_context():
        try:
            user = User.query.first()

            # Test User -> Jobs relationship
            user_jobs = user.jobs
            results.add_test(f"User -> Jobs relationship ({len(user_jobs)} jobs)", True)

            # Test User -> Leads relationship
            user_leads = user.leads
            results.add_test(f"User -> Leads relationship ({len(user_leads)} leads)", True)

            # Test User -> Estimates relationship
            user_estimates = user.estimates
            results.add_test(f"User -> Estimates relationship ({len(user_estimates)} estimates)", True)

            # Test Job -> Tasks relationship
            if user_jobs:
                job = user_jobs[0]
                job_tasks = job.tasks
                results.add_test(f"Job -> Tasks relationship ({len(job_tasks)} tasks)", True)

                # Test Job -> Locations relationship
                job_locations = job.locations
                results.add_test(f"Job -> Locations relationship ({len(job_locations)} locations)", True)

        except Exception as e:
            results.add_test("Database relationships", False, e)

def test_data_validation(results):
    """Test data validation and constraints"""
    print("\n" + "="*70)
    print("TESTING DATA VALIDATION")
    print("="*70)

    app, _, _ = create_app()

    with app.app_context():
        try:
            # Test unique constraint on username
            try:
                user1 = User(username="duplicate_test", email="test1@test.com")
                user1.set_password("pass123")
                db.session.add(user1)
                db.session.commit()

                user2 = User(username="duplicate_test", email="test2@test.com")
                user2.set_password("pass123")
                db.session.add(user2)
                db.session.commit()

                results.add_test("Unique username constraint", False,
                               "Duplicate username was allowed")

                # Clean up
                db.session.rollback()
            except Exception:
                db.session.rollback()
                results.add_test("Unique username constraint", True)

            # Test decimal precision
            user = User.query.first()
            job = Job(
                user_id=user.id,
                client_name="Decimal Test",
                project_type="Test",
                address="123 Test",
                budget=Decimal('12345.67')
            )
            db.session.add(job)
            db.session.commit()

            if job.budget == Decimal('12345.67'):
                results.add_test("Decimal precision for currency", True)
            else:
                results.add_test("Decimal precision for currency", False,
                               f"Expected 12345.67, got {job.budget}")

            # Clean up
            db.session.delete(job)
            db.session.commit()

        except Exception as e:
            results.add_test("Data validation", False, e)

def test_file_structure(results):
    """Test file structure and required files"""
    print("\n" + "="*70)
    print("TESTING FILE STRUCTURE")
    print("="*70)

    required_files = [
        'app.py',
        'models.py',
        'config.py',
        'migrate.py',
        'requirements.txt',
        '.env',
        'templates/base.html',
        'templates/login.html',
        'templates/dashboard.html',
        'templates/jobs.html',
        'static/css/styles.css'
    ]

    for file_path in required_files:
        if os.path.exists(file_path):
            results.add_test(f"File exists: {file_path}", True)
        else:
            results.add_test(f"File exists: {file_path}", False, "File not found")

    # Test upload directories
    upload_dirs = ['uploads', 'uploads/photos', 'uploads/documents']
    for dir_path in upload_dirs:
        if os.path.exists(dir_path):
            results.add_test(f"Directory exists: {dir_path}", True)
        else:
            results.add_test(f"Directory exists: {dir_path}", False, "Directory not found")

def main():
    print("="*70)
    print("CONTRACTORPRO COMPREHENSIVE TEST SUITE")
    print("="*70)
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    results = TestResults()

    # Run all tests
    test_file_structure(results)
    test_database_models(results)
    test_user_authentication(results)
    test_job_creation(results)
    test_estimate_calculations(results)
    test_task_management(results)
    test_contract_generation(results)
    test_pos_system(results)
    test_relationships(results)
    test_data_validation(results)

    # Print summary
    results.print_summary()

    print(f"\nTest completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    return results.failed_tests == 0

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
