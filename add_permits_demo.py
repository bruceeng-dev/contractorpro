"""
Add Permits and Demolition categories to POS system
"""
from app import app, db
from models import POSCategory, POSActivity, User
import json

def add_permits_demo_categories():
    """Add permits and demo categories with activities"""

    with app.app_context():
        print("="*70)
        print("ADDING PERMITS & DEMOLITION TO POS")
        print("="*70)
        print()

        # Get first user (or you can specify)
        user = User.query.first()
        if not user:
            print("ERROR: No users found. Please create a user first.")
            return

        print(f"Adding categories for user: {user.username}")
        print()

        # 1. PERMITS & INSPECTIONS Category
        permits_cat = POSCategory.query.filter_by(name="Permits & Inspections", user_id=user.id).first()
        if not permits_cat:
            permits_cat = POSCategory(
                user_id=user.id,
                name="Permits & Inspections",
                description="Building permits, inspections, and regulatory requirements",
                icon="📋",
                keywords="permit,inspection,approval,building,regulatory,code",
                is_active=True
            )
            db.session.add(permits_cat)
            db.session.flush()
            print("[NEW] Permits & Inspections category created")

            # Add permit activities
            permit_activities = [
                {"name": "Building Permit Application", "cost": 500, "specs": ["place_and_permits"]},
                {"name": "Electrical Permit", "cost": 150, "specs": ["place_and_permits", "electrical"]},
                {"name": "Plumbing Permit", "cost": 150, "specs": ["place_and_permits", "plumbing"]},
                {"name": "Mechanical/HVAC Permit", "cost": 150, "specs": ["place_and_permits", "hvac"]},
                {"name": "Roofing Permit", "cost": 100, "specs": ["place_and_permits", "roof_covering"]},
                {"name": "Demolition Permit", "cost": 200, "specs": ["place_and_permits", "tearout_demolition"]},
                {"name": "Structural Engineering Review", "cost": 1000, "specs": ["place_and_permits", "floor_framing", "wall_framing"]},
                {"name": "Site Plan Review", "cost": 750, "specs": ["place_and_permits"]},
                {"name": "HOA Approval", "cost": 250, "specs": ["place_and_permits"]},
                {"name": "Rough Inspection - Framing", "cost": 0, "specs": ["place_and_permits", "floor_framing", "wall_framing", "roof_framing"]},
                {"name": "Rough Inspection - Electrical", "cost": 0, "specs": ["place_and_permits", "electrical"]},
                {"name": "Rough Inspection - Plumbing", "cost": 0, "specs": ["place_and_permits", "plumbing"]},
                {"name": "Rough Inspection - HVAC", "cost": 0, "specs": ["place_and_permits", "hvac"]},
                {"name": "Insulation Inspection", "cost": 0, "specs": ["place_and_permits", "insulation"]},
                {"name": "Final Inspection", "cost": 0, "specs": ["place_and_permits"]},
                {"name": "Certificate of Occupancy", "cost": 200, "specs": ["place_and_permits"]},
            ]

            for idx, act_data in enumerate(permit_activities, 1):
                activity = POSActivity(
                    category_id=permits_cat.id,
                    name=act_data["name"],
                    description=f"Required for compliance",
                    base_cost=act_data["cost"],
                    unit="each",
                    job_spec_tags=json.dumps(act_data["specs"]),
                    is_active=True,
                    order_index=idx
                )
                db.session.add(activity)
                print(f"  + {act_data['name']} - ${act_data['cost']}")

        else:
            print("[EXISTS] Permits & Inspections category already exists")

        print()

        # 2. DEMOLITION & SITE PREP Category
        demo_cat = POSCategory.query.filter_by(name="Demolition & Site Prep", user_id=user.id).first()
        if not demo_cat:
            demo_cat = POSCategory(
                user_id=user.id,
                name="Demolition & Site Prep",
                description="Demolition, debris removal, and site preparation",
                icon="🔨",
                keywords="demolition,demo,removal,tearout,debris,dumpster,site",
                is_active=True
            )
            db.session.add(demo_cat)
            db.session.flush()
            print("[NEW] Demolition & Site Prep category created")

            # Add demo activities
            demo_activities = [
                {"name": "Full House Demolition", "cost": 15000, "specs": ["tearout_demolition"]},
                {"name": "Interior Demolition - Per Room", "cost": 1500, "specs": ["tearout_demolition"]},
                {"name": "Kitchen Demolition", "cost": 2500, "specs": ["tearout_demolition", "cabinets_appliances"]},
                {"name": "Bathroom Demolition", "cost": 2000, "specs": ["tearout_demolition", "plumbing"]},
                {"name": "Wall Removal (Non-Load Bearing)", "cost": 800, "specs": ["tearout_demolition", "wall_framing"]},
                {"name": "Wall Removal (Load Bearing)", "cost": 3000, "specs": ["tearout_demolition", "wall_framing"]},
                {"name": "Cabinet Removal", "cost": 500, "specs": ["tearout_demolition", "cabinets_appliances"]},
                {"name": "Countertop Removal", "cost": 300, "specs": ["tearout_demolition"]},
                {"name": "Flooring Removal - Carpet", "cost": 200, "specs": ["tearout_demolition", "floor_covering"]},
                {"name": "Flooring Removal - Tile", "cost": 500, "specs": ["tearout_demolition", "floor_covering"]},
                {"name": "Flooring Removal - Hardwood", "cost": 400, "specs": ["tearout_demolition", "floor_covering"]},
                {"name": "Ceiling Removal", "cost": 600, "specs": ["tearout_demolition", "ceiling_covering"]},
                {"name": "Drywall Removal", "cost": 400, "specs": ["tearout_demolition", "interior_wall_covering"]},
                {"name": "Window Removal", "cost": 150, "specs": ["tearout_demolition", "windows_trim"]},
                {"name": "Door Removal", "cost": 100, "specs": ["tearout_demolition", "doors_trim"]},
                {"name": "Appliance Removal & Disposal", "cost": 150, "specs": ["tearout_demolition", "cabinets_appliances"]},
                {"name": "Fixture Removal (Toilet/Sink/Tub)", "cost": 200, "specs": ["tearout_demolition", "plumbing"]},
                {"name": "10-Yard Dumpster Rental", "cost": 400, "specs": ["tearout_demolition", "cleanup"]},
                {"name": "20-Yard Dumpster Rental", "cost": 550, "specs": ["tearout_demolition", "cleanup"]},
                {"name": "30-Yard Dumpster Rental", "cost": 700, "specs": ["tearout_demolition", "cleanup"]},
                {"name": "Debris Haul-Away (Per Load)", "cost": 300, "specs": ["tearout_demolition", "cleanup"]},
                {"name": "Hazardous Material Removal - Asbestos", "cost": 5000, "specs": ["tearout_demolition"]},
                {"name": "Hazardous Material Removal - Lead Paint", "cost": 3000, "specs": ["tearout_demolition"]},
                {"name": "Mold Remediation", "cost": 2500, "specs": ["tearout_demolition"]},
                {"name": "Site Protection & Barriers", "cost": 500, "specs": ["place_and_permits", "tearout_demolition"]},
                {"name": "Temporary Power & Water", "cost": 300, "specs": ["place_and_permits", "electrical", "plumbing"]},
                {"name": "Temporary Toilet Rental", "cost": 200, "specs": ["place_and_permits"]},
            ]

            for idx, act_data in enumerate(demo_activities, 1):
                activity = POSActivity(
                    category_id=demo_cat.id,
                    name=act_data["name"],
                    description=f"Demolition and removal service",
                    base_cost=act_data["cost"],
                    unit="each",
                    job_spec_tags=json.dumps(act_data["specs"]),
                    is_active=True,
                    order_index=idx
                )
                db.session.add(activity)
                print(f"  + {act_data['name']} - ${act_data['cost']}")

        else:
            print("[EXISTS] Demolition & Site Prep category already exists")

        db.session.commit()

        print()
        print("="*70)
        print("SUCCESS! Permits & Demo categories added to POS")
        print("="*70)
        print()
        print("Next steps:")
        print("1. Go to http://localhost:5000/pos/multilayer")
        print("2. Select 'Place and Permits' and 'Tear Out and Demolition'")
        print("3. See the new Permits & Demolition categories!")
        print()

if __name__ == '__main__':
    add_permits_demo_categories()
