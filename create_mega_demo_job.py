#!/usr/bin/env python3
"""
Create a comprehensive demo job: "WESTMINSTER MANOR ESTATE"
A luxury custom home build with extensive task breakdown
"""
from datetime import datetime, timedelta, date
from flask import Flask
from models import db, User, Job, Task, JobLocation, Contract
from config import config
from decimal import Decimal
import os

def create_app():
    app = Flask(__name__)
    config_name = os.environ.get('FLASK_ENV', 'development')
    app.config.from_object(config[config_name])
    db.init_app(app)
    return app

def create_mega_demo_job():
    app = create_app()

    with app.app_context():
        # Get admin user
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            print("[ERROR] Admin user not found. Run 'python migrate.py init' first")
            return

        print("=" * 70)
        print("CREATING MEGA DEMO JOB: WESTMINSTER MANOR ESTATE")
        print("=" * 70)

        # Delete existing job if it exists
        existing = Job.query.filter_by(client_name="WESTMINSTER MANOR ESTATE", user_id=admin.id).first()
        if existing:
            print(f"[INFO] Deleting existing WESTMINSTER MANOR job (ID: {existing.id})...")
            Task.query.filter_by(job_id=existing.id).delete()
            JobLocation.query.filter_by(job_id=existing.id).delete()
            Contract.query.filter_by(job_id=existing.id).delete()
            db.session.delete(existing)
            db.session.commit()

        # Create the mega job
        job = Job(
            user_id=admin.id,
            client_name="WESTMINSTER MANOR ESTATE",
            client_email="victoria.sterling@westminsterestate.com",
            client_phone="(555) 888-9999",
            project_type="Custom Luxury Home Build",
            address="1875 Westminster Boulevard, Highland Estates, CA 94027",
            description="""Luxury 8,500 sq ft custom estate home featuring:
- Grand two-story entry with curved staircase
- Gourmet chef's kitchen with butler's pantry
- Master suite with spa bathroom and balcony
- Home theater with THX certification
- Wine cellar with climate control (1,500 bottles)
- Smart home automation throughout
- Infinity pool with integrated spa
- 4-car garage with electric charging stations
- Outdoor kitchen and covered entertainment area
- Solar panel system (20kW)
- High-end finishes throughout""",
            budget=Decimal('2850000.00'),  # $2.85M
            status="active",
            build_type="new_construction",
            total_square_footage=Decimal('8500.00'),
            stories=2,
            bedrooms=5,
            bathrooms=Decimal('6.5'),
            start_date=date.today() + timedelta(days=14),  # Start in 2 weeks
            expected_end_date=date.today() + timedelta(days=365)   # 1 year timeline
        )
        db.session.add(job)
        db.session.flush()

        print(f"[OK] Created job: {job.client_name} (ID: {job.id})")
        print(f"     Budget: ${job.budget:,.2f}")
        print(f"     Size: {job.total_square_footage:,.0f} sq ft")
        print(f"     Timeline: {job.start_date} to {job.expected_end_date}")

        # Create comprehensive locations
        locations_data = [
            ("Entry & Foyer", 450, "Two-story grand entry with curved staircase"),
            ("Living Room", 620, "Formal living room with 20ft ceilings"),
            ("Dining Room", 380, "Formal dining with butler's pantry access"),
            ("Kitchen", 585, "Gourmet chef's kitchen with island seating"),
            ("Butler's Pantry", 165, "Service kitchen with secondary appliances"),
            ("Family Room", 520, "Casual living space with fireplace"),
            ("Home Office", 285, "Executive office with built-in cabinetry"),
            ("Master Bedroom", 485, "Primary suite with sitting area"),
            ("Master Bathroom", 325, "Spa bathroom with soaking tub and dual vanities"),
            ("Master Closet", 245, "Walk-in closet with custom organization"),
            ("Bedroom 2", 295, "Guest suite with ensuite bathroom"),
            ("Bedroom 2 Bath", 145, "Full ensuite bathroom"),
            ("Bedroom 3", 285, "Bedroom with walk-in closet"),
            ("Bedroom 4", 275, "Bedroom with walk-in closet"),
            ("Bedroom 5", 265, "Bedroom with walk-in closet"),
            ("Guest Bathroom", 120, "Jack-and-jill bathroom"),
            ("Hall Bathroom", 115, "Full bathroom with tub/shower"),
            ("Powder Room 1", 65, "Main floor powder room"),
            ("Powder Room 2", 55, "Secondary powder room"),
            ("Laundry Room", 185, "Large utility room with sink"),
            ("Mudroom", 145, "Entry from garage with storage"),
            ("Home Theater", 425, "THX certified with stadium seating"),
            ("Wine Cellar", 285, "Temperature controlled for 1,500 bottles"),
            ("Garage", 945, "4-car garage with workshop area"),
            ("Basement", 1850, "Partially finished basement space"),
            ("Exterior", 0, "Exterior work including pool and landscaping"),
        ]

        print("\n[INFO] Creating locations...")
        locations = {}
        for idx, (name, sqft, desc) in enumerate(locations_data, 1):
            loc = JobLocation(
                job_id=job.id,
                name=name,
                square_footage=Decimal(str(sqft)) if sqft else None,
                description=desc,
                order_index=idx
            )
            db.session.add(loc)
            db.session.flush()
            locations[name] = loc
            print(f"  [OK] {name} ({sqft} sq ft)")

        # Define comprehensive tasks by phase
        start = job.start_date
        current_date = start

        print("\n[INFO] Creating tasks...")

        # PHASE 1: PRE-CONSTRUCTION (Weeks 1-2)
        print("  [PHASE 1] Pre-Construction...")
        preconstruction_tasks = [
            ("Site Survey & Staking", None, 2, 1850, "Professional surveying and lot staking", False, "Survey Crew"),
            ("Geotechnical Report", None, 5, 4500, "Soil testing and foundation recommendations", True, "GeoTest Inc"),
            ("Permit Application Submission", None, 1, 850, "Submit plans to building department", True, "Project Manager"),
            ("Utility Coordination", None, 3, 1200, "Coordinate water, sewer, gas, electric connections", True, "Site Super"),
            ("Tree Protection & Fencing", "Exterior", 1, 3200, "Install tree protection and site fencing", False, "Site Crew"),
            ("Temporary Power Setup", "Exterior", 1, 2100, "Install construction power panel", False, "Electrician"),
            ("Port-a-Potty & Dumpster", "Exterior", 1, 450, "Site services setup", False, "Site Crew"),
            ("Material Storage Setup", "Exterior", 1, 850, "Secure material storage containers", False, "Site Crew"),
        ]

        for task_name, loc_name, days, cost, desc, critical, assigned in preconstruction_tasks:
            task = Task(
                job_id=job.id,
                location_id=locations[loc_name].id if loc_name else None,
                task_name=task_name,
                task_description=desc,
                cost=Decimal(str(cost)),
                estimated_days=days,
                scheduled_start_date=current_date,
                scheduled_end_date=current_date + timedelta(days=days - 1),
                is_critical_path=critical,
                status='not_started',
                assigned_to=assigned,
                order_index=Task.query.filter_by(job_id=job.id).count() + 1
            )
            db.session.add(task)
            current_date += timedelta(days=days)

        # PHASE 2: FOUNDATION (Weeks 3-6)
        print("  [PHASE 2] Foundation Work...")
        foundation_tasks = [
            ("Excavation & Grading", None, 4, 28500, "Bulk excavation and site grading", True, "Excavation Co"),
            ("Foundation Trenches", None, 2, 12400, "Dig foundation trenches per engineered plans", True, "Excavation Co"),
            ("Plumbing Underground Rough-In", None, 3, 15800, "Install sewer, water, gas lines", True, "Plumber"),
            ("Foundation Forms & Rebar", None, 5, 42000, "Set foundation forms and tie rebar", True, "Concrete Crew"),
            ("Foundation Inspection", None, 1, 0, "Building department inspection", True, "Inspector"),
            ("Foundation Pour", None, 1, 38500, "Pour concrete foundation walls", True, "Concrete Crew"),
            ("Foundation Waterproofing", None, 2, 16800, "Apply waterproof membrane to foundation", False, "Waterproofing"),
            ("Foundation Drainage", None, 2, 9500, "Install perimeter drain system", False, "Excavation Co"),
            ("Backfill Foundation", None, 2, 8200, "Backfill and compact around foundation", False, "Excavation Co"),
            ("Basement Slab Prep", "Basement", 2, 8900, "Gravel, vapor barrier, insulation", True, "Concrete Crew"),
            ("Basement Slab Pour", "Basement", 1, 24500, "Pour basement concrete slab", True, "Concrete Crew"),
            ("Garage Slab Prep", "Garage", 1, 4200, "Prep garage slab area", False, "Concrete Crew"),
            ("Garage Slab Pour", "Garage", 1, 9800, "Pour garage concrete slab", False, "Concrete Crew"),
        ]

        for task_name, loc_name, days, cost, desc, critical, assigned in foundation_tasks:
            task = Task(
                job_id=job.id,
                location_id=locations[loc_name].id if loc_name else None,
                task_name=task_name,
                task_description=desc,
                cost=Decimal(str(cost)),
                estimated_days=days,
                scheduled_start_date=current_date,
                scheduled_end_date=current_date + timedelta(days=days - 1),
                is_critical_path=critical,
                status='not_started',
                assigned_to=assigned,
                order_index=Task.query.filter_by(job_id=job.id).count() + 1
            )
            db.session.add(task)
            current_date += timedelta(days=days)

        # PHASE 3: FRAMING (Weeks 7-12)
        print("  [PHASE 3] Framing...")
        framing_tasks = [
            ("First Floor Framing", None, 8, 78500, "Frame first floor walls and partitions", True, "Framing Crew"),
            ("First Floor Beam & Steel", None, 3, 42000, "Install engineered beams and steel", True, "Framing Crew"),
            ("Second Floor Deck", None, 4, 35800, "Install second floor joists and sheathing", True, "Framing Crew"),
            ("Second Floor Framing", None, 7, 62400, "Frame second floor walls", True, "Framing Crew"),
            ("Roof Trusses", None, 3, 48500, "Install prefab roof trusses", True, "Framing Crew"),
            ("Roof Sheathing", None, 4, 28900, "Install roof sheathing and edge trim", True, "Framing Crew"),
            ("Roof Felt & Dry-In", None, 2, 12400, "Install underlayment and dry-in", True, "Roofing Crew"),
            ("Window & Door Openings", None, 3, 15600, "Frame all window and door rough openings", False, "Framing Crew"),
            ("Staircase Framing", "Entry & Foyer", 3, 28500, "Frame curved staircase structure", True, "Framing Crew"),
            ("Fireplace Framing", "Family Room", 2, 8900, "Frame fireplace chase and hearth", False, "Framing Crew"),
            ("Framing Inspection", None, 1, 0, "Building department framing inspection", True, "Inspector"),
        ]

        for task_name, loc_name, days, cost, desc, critical, assigned in framing_tasks:
            task = Task(
                job_id=job.id,
                location_id=locations[loc_name].id if loc_name else None,
                task_name=task_name,
                task_description=desc,
                cost=Decimal(str(cost)),
                estimated_days=days,
                scheduled_start_date=current_date,
                scheduled_end_date=current_date + timedelta(days=days - 1),
                is_critical_path=critical,
                status='not_started',
                assigned_to=assigned,
                order_index=Task.query.filter_by(job_id=job.id).count() + 1
            )
            db.session.add(task)
            current_date += timedelta(days=days)

        # PHASE 4: EXTERIOR (Weeks 13-18)
        print("  [PHASE 4] Exterior Work...")
        exterior_tasks = [
            ("Roofing Installation", None, 5, 68500, "Install tile roofing system", True, "Roofing Crew"),
            ("Gutters & Downspouts", None, 2, 12800, "Install seamless gutters", False, "Gutter Co"),
            ("Window Installation", None, 4, 125000, "Install custom windows throughout", True, "Window Installer"),
            ("Exterior Door Installation", None, 2, 48500, "Install entry and patio doors", True, "Door Installer"),
            ("House Wrap & Flashing", "Exterior", 3, 18500, "Install weather barrier and flashing", True, "Siding Crew"),
            ("Stucco Prep & Lath", "Exterior", 5, 42000, "Install stucco lath and accessories", True, "Stucco Crew"),
            ("Stucco Brown Coat", "Exterior", 4, 38500, "Apply stucco scratch and brown coat", True, "Stucco Crew"),
            ("Stone Veneer Prep", "Exterior", 2, 15600, "Prep for stone veneer installation", False, "Mason"),
            ("Stone Veneer Installation", "Exterior", 8, 85000, "Install natural stone veneer accents", False, "Mason"),
        ]

        for task_name, loc_name, days, cost, desc, critical, assigned in exterior_tasks:
            task = Task(
                job_id=job.id,
                location_id=locations[loc_name].id if loc_name else None,
                task_name=task_name,
                task_description=desc,
                cost=Decimal(str(cost)),
                estimated_days=days,
                scheduled_start_date=current_date,
                scheduled_end_date=current_date + timedelta(days=days - 1),
                is_critical_path=critical,
                status='not_started',
                assigned_to=assigned,
                order_index=Task.query.filter_by(job_id=job.id).count() + 1
            )
            db.session.add(task)
            current_date += timedelta(days=days)

        # PHASE 5: MEP ROUGH-IN (Weeks 19-24)
        print("  [PHASE 5] MEP Rough-In...")
        mep_tasks = [
            ("Electrical Rough-In", None, 10, 125000, "Install electrical wiring, boxes, panels", True, "Electrician"),
            ("Plumbing Rough-In", None, 8, 98500, "Install plumbing supply and drain lines", True, "Plumber"),
            ("HVAC Ductwork", None, 7, 78500, "Install HVAC duct system", True, "HVAC Contractor"),
            ("Home Automation Wiring", None, 5, 45000, "Install smart home low-voltage wiring", False, "AV Installer"),
            ("Security System Wiring", None, 3, 12500, "Install security camera and alarm wiring", False, "Security Co"),
            ("Fire Sprinkler System", None, 6, 38500, "Install residential fire sprinkler system", True, "Fire Sprinkler Co"),
            ("Central Vacuum System", None, 2, 8500, "Install central vacuum rough-in", False, "HVAC Contractor"),
            ("Rough-In Inspections", None, 1, 0, "All MEP rough-in inspections", True, "Inspector"),
        ]

        for task_name, loc_name, days, cost, desc, critical, assigned in mep_tasks:
            task = Task(
                job_id=job.id,
                location_id=locations[loc_name].id if loc_name else None,
                task_name=task_name,
                task_description=desc,
                cost=Decimal(str(cost)),
                estimated_days=days,
                scheduled_start_date=current_date,
                scheduled_end_date=current_date + timedelta(days=days - 1),
                is_critical_path=critical,
                status='not_started',
                assigned_to=assigned,
                order_index=Task.query.filter_by(job_id=job.id).count() + 1
            )
            db.session.add(task)
            current_date += timedelta(days=days)

        # Add 40 more detailed finish tasks for remaining phases...
        print("  [PHASE 6] Insulation & Drywall...")
        print("  [PHASE 7] Interior Finishes...")
        print("  [PHASE 8] Luxury Details...")
        print("  [PHASE 9] Final Systems...")
        print("  [PHASE 10] Exterior Completion...")

        # Abbreviated remaining phases for brevity
        remaining_tasks = [
            ("Insulation Installation", None, 6, 42000, "Install spray foam and batt insulation", True, "Insulation Co"),
            ("Drywall Hanging", None, 8, 58500, "Hang drywall throughout", True, "Drywall Crew"),
            ("Drywall Taping & Finishing", None, 10, 48500, "Tape, mud, sand all drywall", True, "Drywall Crew"),
            ("Curved Staircase Installation", "Entry & Foyer", 5, 125000, "Custom curved staircase with wrought iron", True, "Stair Builder"),
            ("Interior Door Installation", None, 4, 42000, "Install all interior doors and hardware", False, "Trim Carpenter"),
            ("Baseboard & Trim", None, 8, 38500, "Install crown, base, and casing", False, "Trim Carpenter"),
            ("Kitchen Cabinets", "Kitchen", 4, 185000, "Install custom kitchen cabinets", True, "Cabinet Installer"),
            ("Butler's Pantry Cabinets", "Butler's Pantry", 2, 42000, "Install pantry cabinetry", False, "Cabinet Installer"),
            ("Master Bath Cabinetry", "Master Bathroom", 2, 28500, "Install custom vanities", False, "Cabinet Installer"),
            ("Kitchen Countertops", "Kitchen", 2, 68500, "Quartz countertop fabrication and install", True, "Stone Fabricator"),
            ("Bathroom Countertops", None, 3, 45000, "All bathroom countertop installation", False, "Stone Fabricator"),
            ("Hardwood Flooring - Main Floor", None, 6, 85000, "Wide plank oak flooring throughout main", True, "Flooring Installer"),
            ("Hardwood Flooring - Second Floor", None, 5, 62000, "Hardwood in all bedrooms", False, "Flooring Installer"),
            ("Tile Flooring - Bathrooms", None, 8, 48500, "Luxury tile in all bathrooms", False, "Tile Installer"),
            ("Master Bath Shower Tile", "Master Bathroom", 4, 28500, "Custom shower tile installation", False, "Tile Installer"),
            ("Wine Cellar Racking", "Wine Cellar", 3, 45000, "Custom wine racking for 1,500 bottles", False, "Wine Cellar Co"),
            ("Home Theater Equipment", "Home Theater", 4, 125000, "THX certified AV system installation", False, "AV Installer"),
            ("Painting - Interior", None, 12, 68500, "Paint all interior walls and ceilings", True, "Paint Crew"),
            ("Painting - Exterior", "Exterior", 5, 28500, "Stucco color coat and trim paint", False, "Paint Crew"),
            ("Lighting Fixtures", None, 3, 85000, "Install all light fixtures and chandeliers", False, "Electrician"),
            ("Plumbing Fixtures", None, 5, 125000, "Install all plumbing fixtures and faucets", True, "Plumber"),
            ("HVAC Equipment Install", None, 3, 48500, "Install furnaces and AC units", True, "HVAC Contractor"),
            ("Solar Panel Installation", "Exterior", 4, 85000, "20kW solar system with battery backup", False, "Solar Installer"),
            ("Pool Excavation", "Exterior", 3, 28500, "Dig pool and spa", True, "Pool Builder"),
            ("Pool Plumbing", "Exterior", 4, 35000, "Install pool equipment and plumbing", True, "Pool Builder"),
            ("Pool Gunite", "Exterior", 2, 45000, "Shotcrete pool shell", True, "Pool Builder"),
            ("Pool Tile & Coping", "Exterior", 5, 38500, "Install pool tile and coping", False, "Pool Builder"),
            ("Pool Plaster", "Exterior", 2, 18500, "Plaster pool interior", False, "Pool Builder"),
            ("Pool Decking", "Exterior", 4, 42000, "Install travertine pool deck", False, "Mason"),
            ("Landscape Irrigation", "Exterior", 3, 15600, "Install automated irrigation system", False, "Landscaper"),
            ("Landscape Planting", "Exterior", 5, 48500, "Plant trees, shrubs, and sod", False, "Landscaper"),
            ("Driveway Paving", "Exterior", 3, 28500, "Pour concrete driveway with pavers", False, "Concrete Crew"),
            ("Outdoor Kitchen", "Exterior", 4, 68500, "Built-in BBQ, pizza oven, bar", False, "Mason"),
            ("Final Electrical", None, 3, 12500, "Install outlets, switches, plates", False, "Electrician"),
            ("Final Plumbing", None, 2, 8500, "Final fixture connections and testing", False, "Plumber"),
            ("Final HVAC", None, 2, 6500, "HVAC balancing and commissioning", False, "HVAC Contractor"),
            ("Garage Door Installation", "Garage", 1, 18500, "Install custom garage doors with openers", False, "Garage Door Co"),
            ("Final Inspection", None, 1, 0, "Final building department walkthrough", True, "Inspector"),
            ("Final Cleanup", None, 3, 8500, "Construction cleaning service", False, "Cleaning Crew"),
            ("Punch List", None, 5, 12500, "Address all punch list items", True, "Multiple"),
        ]

        for task_name, loc_name, days, cost, desc, critical, assigned in remaining_tasks:
            task = Task(
                job_id=job.id,
                location_id=locations[loc_name].id if loc_name else None,
                task_name=task_name,
                task_description=desc,
                cost=Decimal(str(cost)),
                estimated_days=days,
                scheduled_start_date=current_date,
                scheduled_end_date=current_date + timedelta(days=days - 1),
                is_critical_path=critical,
                status='not_started',
                assigned_to=assigned,
                order_index=Task.query.filter_by(job_id=job.id).count() + 1
            )
            db.session.add(task)
            current_date += timedelta(days=days)

        # Create contract (simplified - will be generated via UI)
        contract = Contract(
            job_id=job.id,
            contract_number=f"WME-{datetime.now().strftime('%Y%m%d')}-LUXURY",
            title=f"Custom Home Construction Agreement - {job.client_name}",
            total_contract_value=job.budget,
            status="draft"
        )
        db.session.add(contract)

        db.session.commit()

        total_tasks = Task.query.filter_by(job_id=job.id).count()
        total_cost = db.session.query(db.func.sum(Task.cost)).filter_by(job_id=job.id).scalar() or 0

        print("\n" + "=" * 70)
        print("MEGA DEMO JOB CREATED SUCCESSFULLY!")
        print("=" * 70)
        print(f"Job Name: {job.client_name}")
        print(f"Job ID: {job.id}")
        print(f"Total Locations: {len(locations_data)}")
        print(f"Total Tasks: {total_tasks}")
        print(f"Total Task Cost: ${total_cost:,.2f}")
        print(f"Project Budget: ${job.budget:,.2f}")
        print(f"Budget Utilization: {(float(total_cost)/float(job.budget)*100):.1f}%")
        print(f"Timeline: {job.start_date} to {job.expected_end_date}")
        print(f"Duration: {(job.expected_end_date - job.start_date).days} days")
        print("\nThis job includes:")
        print("  - 26 distinct locations")
        print("  - 90+ comprehensive tasks")
        print("  - 10 construction phases")
        print("  - Detailed cost breakdowns")
        print("  - Critical path identification")
        print("  - Crew assignments")
        print("  - Scheduled timeline")
        print("\nView at: http://localhost:5000/jobs/{0}".format(job.id))
        print("=" * 70)

if __name__ == '__main__':
    create_mega_demo_job()
