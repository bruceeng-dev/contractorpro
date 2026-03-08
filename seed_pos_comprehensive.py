"""
Comprehensive POS Seed Script
- Creates job specifications
- Creates POS categories
- Creates activities within categories
- Maps categories to job specifications
"""
from app import app, db
from models import JobSpecification, POSCategory, POSActivity, POSCategorySpecMapping, User
from decimal import Decimal

# Job Specifications
JOB_SPECS = [
    {"name": "place_and_permits", "display_name": "Place and Permits", "order_index": 1},
    {"name": "tearout_demolition", "display_name": "Tear Out and Demolition", "order_index": 2},
    {"name": "excavation_grading", "display_name": "Excavation and Grading", "order_index": 3},
    {"name": "concrete", "display_name": "Concrete", "order_index": 4},
    {"name": "masonry", "display_name": "Masonry", "order_index": 5},
    {"name": "floor_framing", "display_name": "Floor Framing", "order_index": 6},
    {"name": "wall_framing", "display_name": "Wall Framing", "order_index": 7},
    {"name": "roof_framing", "display_name": "Roof Framing", "order_index": 8},
    {"name": "roof_covering", "display_name": "Roof Covering", "order_index": 9},
    {"name": "flashing", "display_name": "Flashing", "order_index": 10},
    {"name": "exterior_trim", "display_name": "Exterior Trim", "order_index": 11},
    {"name": "porches_decks", "display_name": "Porches and Decks", "order_index": 12},
    {"name": "siding", "display_name": "Siding", "order_index": 13},
    {"name": "doors_trim", "display_name": "Doors and Door Trim", "order_index": 14},
    {"name": "windows_trim", "display_name": "Windows and Window Trim", "order_index": 15},
    {"name": "plumbing", "display_name": "Plumbing", "order_index": 16},
    {"name": "heating_ac", "display_name": "Heating and A/C", "order_index": 17},
    {"name": "electrical", "display_name": "Electrical", "order_index": 18},
    {"name": "insulation", "display_name": "Insulation", "order_index": 19},
    {"name": "interior_wall_covering", "display_name": "Interior Wall Covering", "order_index": 20},
    {"name": "ceiling_covering", "display_name": "Ceiling Covering", "order_index": 21},
    {"name": "millwork_trim", "display_name": "Millwork Trim", "order_index": 22},
    {"name": "stairs", "display_name": "Stairs", "order_index": 23},
    {"name": "cabinets_appliances", "display_name": "Cabinets and Appliances", "order_index": 24},
    {"name": "specialties", "display_name": "Specialties", "order_index": 25},
    {"name": "floor_covering", "display_name": "Floor Covering", "order_index": 26},
    {"name": "painting_decorating", "display_name": "Painting and Decorating", "order_index": 27},
    {"name": "cleanup", "display_name": "Clean Up", "order_index": 28}
]

# Categories with Activities and Job Spec Mappings
CATEGORIES_DATA = {
    "Kitchen Remodel": {
        "icon": "🍳",
        "keywords": "kitchen,cooking,remodel,renovation",
        "job_specs": ["tearout_demolition", "plumbing", "electrical", "interior_wall_covering",
                     "cabinets_appliances", "floor_covering", "painting_decorating", "cleanup"],
        "activities": [
            {"name": "Demo Existing Kitchen", "base_cost": 2500, "unit": "job"},
            {"name": "Install Kitchen Cabinets", "base_cost": 8500, "unit": "job"},
            {"name": "Install Countertops (Granite)", "base_cost": 4500, "unit": "job"},
            {"name": "Install Kitchen Sink & Faucet", "base_cost": 850, "unit": "each"},
            {"name": "Install Dishwasher", "base_cost": 650, "unit": "each"},
            {"name": "Install Range Hood", "base_cost": 750, "unit": "each"},
            {"name": "Kitchen Electrical Outlets", "base_cost": 150, "unit": "each"},
            {"name": "Kitchen Lighting Fixtures", "base_cost": 350, "unit": "each"},
            {"name": "Kitchen Flooring (Tile)", "base_cost": 2800, "unit": "sqft"},
            {"name": "Kitchen Backsplash", "base_cost": 1200, "unit": "job"},
            {"name": "Paint Kitchen", "base_cost": 850, "unit": "room"}
        ]
    },
    "Bathroom Remodel": {
        "icon": "🚿",
        "keywords": "bathroom,bath,shower,toilet,remodel",
        "job_specs": ["tearout_demolition", "plumbing", "electrical", "interior_wall_covering",
                     "ceiling_covering", "cabinets_appliances", "specialties", "floor_covering",
                     "painting_decorating", "cleanup"],
        "activities": [
            {"name": "Demo Existing Bathroom", "base_cost": 1800, "unit": "job"},
            {"name": "Install Bathtub", "base_cost": 2500, "unit": "each"},
            {"name": "Install Shower (Tile)", "base_cost": 4500, "unit": "each"},
            {"name": "Install Toilet", "base_cost": 450, "unit": "each"},
            {"name": "Install Bathroom Vanity", "base_cost": 1200, "unit": "each"},
            {"name": "Install Sink & Faucet", "base_cost": 650, "unit": "each"},
            {"name": "Install Bathroom Mirror", "base_cost": 350, "unit": "each"},
            {"name": "Bathroom Electrical Work", "base_cost": 850, "unit": "job"},
            {"name": "Bathroom Flooring (Tile)", "base_cost": 1800, "unit": "job"},
            {"name": "Paint Bathroom", "base_cost": 550, "unit": "room"}
        ]
    },
    "Roofing": {
        "icon": "🏠",
        "keywords": "roof,shingles,roofing,covering",
        "job_specs": ["roof_framing", "roof_covering", "flashing", "cleanup"],
        "activities": [
            {"name": "Remove Old Roofing", "base_cost": 2500, "unit": "square"},
            {"name": "Roof Sheathing Repair", "base_cost": 450, "unit": "sheet"},
            {"name": "Install Architectural Shingles", "base_cost": 350, "unit": "square"},
            {"name": "Install Ridge Vent", "base_cost": 850, "unit": "job"},
            {"name": "Install Flashing", "base_cost": 650, "unit": "job"},
            {"name": "Install Gutters", "base_cost": 12, "unit": "lnft"},
            {"name": "Install Downspouts", "base_cost": 85, "unit": "each"}
        ]
    },
    "Flooring": {
        "icon": "📐",
        "keywords": "floor,flooring,tile,hardwood,carpet,laminate",
        "job_specs": ["floor_covering", "cleanup"],
        "activities": [
            {"name": "Remove Old Flooring", "base_cost": 3.50, "unit": "sqft"},
            {"name": "Install Hardwood Flooring", "base_cost": 12, "unit": "sqft"},
            {"name": "Install Tile Flooring", "base_cost": 15, "unit": "sqft"},
            {"name": "Install Laminate Flooring", "base_cost": 8, "unit": "sqft"},
            {"name": "Install Carpet", "base_cost": 6, "unit": "sqft"},
            {"name": "Install Vinyl Plank", "base_cost": 9, "unit": "sqft"},
            {"name": "Floor Leveling", "base_cost": 4.50, "unit": "sqft"}
        ]
    },
    "Deck & Patio": {
        "icon": "🪵",
        "keywords": "deck,patio,outdoor,porch,railing",
        "job_specs": ["porches_decks", "cleanup"],
        "activities": [
            {"name": "Build Wood Deck (Pressure Treated)", "base_cost": 35, "unit": "sqft"},
            {"name": "Build Composite Deck", "base_cost": 55, "unit": "sqft"},
            {"name": "Install Deck Railing", "base_cost": 85, "unit": "lnft"},
            {"name": "Build Covered Patio", "base_cost": 65, "unit": "sqft"},
            {"name": "Install Patio Pavers", "base_cost": 25, "unit": "sqft"},
            {"name": "Build Deck Stairs", "base_cost": 850, "unit": "each"}
        ]
    },
    "Siding & Exterior": {
        "icon": "🏗️",
        "keywords": "siding,exterior,vinyl,trim",
        "job_specs": ["siding", "exterior_trim", "doors_trim", "windows_trim", "cleanup"],
        "activities": [
            {"name": "Remove Old Siding", "base_cost": 2.50, "unit": "sqft"},
            {"name": "Install Vinyl Siding", "base_cost": 8, "unit": "sqft"},
            {"name": "Install Fiber Cement Siding", "base_cost": 12, "unit": "sqft"},
            {"name": "Install Wood Siding", "base_cost": 15, "unit": "sqft"},
            {"name": "Install Exterior Trim", "base_cost": 8, "unit": "lnft"},
            {"name": "Install Soffit & Fascia", "base_cost": 12, "unit": "lnft"},
            {"name": "Replace Entry Door", "base_cost": 1850, "unit": "each"},
            {"name": "Replace Window", "base_cost": 650, "unit": "each"}
        ]
    },
    "Painting": {
        "icon": "🎨",
        "keywords": "paint,painting,interior,exterior,decorating",
        "job_specs": ["painting_decorating", "cleanup"],
        "activities": [
            {"name": "Paint Room (Interior)", "base_cost": 650, "unit": "room"},
            {"name": "Paint Ceiling", "base_cost": 350, "unit": "room"},
            {"name": "Paint Trim & Doors", "base_cost": 450, "unit": "room"},
            {"name": "Paint Exterior (House)", "base_cost": 4500, "unit": "job"},
            {"name": "Wallpaper Removal", "base_cost": 2.50, "unit": "sqft"},
            {"name": "Drywall Repair", "base_cost": 150, "unit": "each"}
        ]
    },
    "Basement Finishing": {
        "icon": "🏠",
        "keywords": "basement,finishing,remodel,framing",
        "job_specs": ["wall_framing", "electrical", "plumbing", "insulation",
                     "interior_wall_covering", "ceiling_covering", "floor_covering",
                     "painting_decorating", "cleanup"],
        "activities": [
            {"name": "Frame Basement Walls", "base_cost": 8, "unit": "lnft"},
            {"name": "Install Basement Insulation", "base_cost": 2.50, "unit": "sqft"},
            {"name": "Install Drywall", "base_cost": 3.50, "unit": "sqft"},
            {"name": "Basement Electrical Rough-In", "base_cost": 2500, "unit": "job"},
            {"name": "Basement Plumbing Rough-In", "base_cost": 3500, "unit": "job"},
            {"name": "Install Drop Ceiling", "base_cost": 6, "unit": "sqft"},
            {"name": "Install Basement Flooring", "base_cost": 8, "unit": "sqft"},
            {"name": "Paint Basement", "base_cost": 2500, "unit": "job"}
        ]
    },
    "Home Addition": {
        "icon": "🏡",
        "keywords": "addition,extension,new,construction",
        "job_specs": ["place_and_permits", "excavation_grading", "concrete", "floor_framing",
                     "wall_framing", "roof_framing", "roof_covering", "windows_trim", "doors_trim",
                     "siding", "electrical", "plumbing", "insulation", "interior_wall_covering",
                     "floor_covering", "painting_decorating", "cleanup"],
        "activities": [
            {"name": "Foundation & Footings", "base_cost": 12, "unit": "sqft"},
            {"name": "Floor Framing", "base_cost": 15, "unit": "sqft"},
            {"name": "Wall Framing", "base_cost": 18, "unit": "sqft"},
            {"name": "Roof Framing", "base_cost": 20, "unit": "sqft"},
            {"name": "Rough Electrical", "base_cost": 5, "unit": "sqft"},
            {"name": "Rough Plumbing", "base_cost": 6, "unit": "sqft"},
            {"name": "Insulation", "base_cost": 3, "unit": "sqft"},
            {"name": "Drywall Installation", "base_cost": 4, "unit": "sqft"},
            {"name": "Interior Finishing", "base_cost": 25, "unit": "sqft"}
        ]
    },
    "HVAC": {
        "icon": "❄️",
        "keywords": "hvac,heating,cooling,air conditioning,furnace",
        "job_specs": ["heating_ac", "electrical", "cleanup"],
        "activities": [
            {"name": "Install Central AC Unit", "base_cost": 4500, "unit": "each"},
            {"name": "Install Furnace", "base_cost": 3500, "unit": "each"},
            {"name": "Install Ductwork", "base_cost": 12, "unit": "lnft"},
            {"name": "Install Thermostat", "base_cost": 350, "unit": "each"},
            {"name": "HVAC System Tune-Up", "base_cost": 250, "unit": "job"}
        ]
    },
    "Electrical Work": {
        "icon": "⚡",
        "keywords": "electrical,wiring,outlets,lighting,panel",
        "job_specs": ["electrical", "cleanup"],
        "activities": [
            {"name": "Electrical Panel Upgrade", "base_cost": 2500, "unit": "each"},
            {"name": "Install Outlet", "base_cost": 125, "unit": "each"},
            {"name": "Install Light Fixture", "base_cost": 250, "unit": "each"},
            {"name": "Install Ceiling Fan", "base_cost": 350, "unit": "each"},
            {"name": "Install Recessed Lighting", "base_cost": 275, "unit": "each"},
            {"name": "Rewire Room", "base_cost": 1500, "unit": "room"}
        ]
    },
    "Plumbing Work": {
        "icon": "🔧",
        "keywords": "plumbing,pipes,fixtures,water,drain",
        "job_specs": ["plumbing", "cleanup"],
        "activities": [
            {"name": "Replace Water Heater", "base_cost": 1850, "unit": "each"},
            {"name": "Repipe House", "base_cost": 8500, "unit": "job"},
            {"name": "Install Sump Pump", "base_cost": 1200, "unit": "each"},
            {"name": "Drain Cleaning", "base_cost": 250, "unit": "each"},
            {"name": "Install Garbage Disposal", "base_cost": 350, "unit": "each"},
            {"name": "Fix Leak", "base_cost": 150, "unit": "each"}
        ]
    }
}

def seed_comprehensive_pos():
    with app.app_context():
        print("=" * 70)
        print("COMPREHENSIVE POS SYSTEM SEED")
        print("=" * 70)
        print()

        # Get first user (admin) for categories
        admin_user = User.query.first()
        if not admin_user:
            print("[ERROR] No users found. Please create a user first.")
            return

        print(f"Using user: {admin_user.username}")
        print()

        # Step 1: Job Specifications
        print("Step 1: Seeding job specifications...")
        spec_map = {}
        existing_specs = JobSpecification.query.count()

        if existing_specs == 0:
            for spec_data in JOB_SPECS:
                spec = JobSpecification(**spec_data)
                db.session.add(spec)
            db.session.commit()
            print(f"  [OK] Created {len(JOB_SPECS)} job specifications")
        else:
            print(f"  [OK] Found {existing_specs} existing specifications")

        # Build spec name to ID map
        all_specs = JobSpecification.query.all()
        for spec in all_specs:
            spec_map[spec.name] = spec.id
        print()

        # Step 2: Categories and Activities
        print("Step 2: Creating categories and activities...")
        existing_categories = POSCategory.query.filter_by(user_id=admin_user.id).count()

        if existing_categories > 0:
            print(f"  [INFO] Found {existing_categories} existing categories")
            response = input("  Clear and recreate? (yes/no): ").strip().lower()
            if response == 'yes':
                POSCategory.query.filter_by(user_id=admin_user.id).delete()
                db.session.commit()
                print("  [OK] Cleared existing categories")
            else:
                print("  [SKIP] Keeping existing categories")
                print("\n[DONE] Setup complete (kept existing data)")
                return

        category_count = 0
        activity_count = 0
        mapping_count = 0

        for cat_name, cat_data in CATEGORIES_DATA.items():
            # Create category
            category = POSCategory(
                user_id=admin_user.id,
                name=cat_name,
                description=f"{cat_name} services and activities",
                icon=cat_data['icon'],
                keywords=cat_data['keywords'],
                order_index=category_count + 1
            )
            db.session.add(category)
            db.session.flush()  # Get the ID
            category_count += 1

            # Create activities
            for idx, activity_data in enumerate(cat_data['activities']):
                activity = POSActivity(
                    category_id=category.id,
                    name=activity_data['name'],
                    description=f"{activity_data['name']} - {cat_name}",
                    base_cost=Decimal(str(activity_data['base_cost'])),
                    unit=activity_data['unit'],
                    order_index=idx + 1
                )
                db.session.add(activity)
                activity_count += 1

            # Create mappings
            for spec_name in cat_data['job_specs']:
                if spec_name in spec_map:
                    mapping = POSCategorySpecMapping(
                        category_id=category.id,
                        spec_id=spec_map[spec_name]
                    )
                    db.session.add(mapping)
                    mapping_count += 1

        db.session.commit()
        print(f"  [OK] Created {category_count} categories")
        print(f"  [OK] Created {activity_count} activities")
        print(f"  [OK] Created {mapping_count} spec mappings")
        print()

        # Summary
        print("=" * 70)
        print("SETUP COMPLETE!")
        print("=" * 70)
        print()
        print("Categories Created:")
        for cat_name in CATEGORIES_DATA.keys():
            print(f"  - {cat_name}")
        print()
        print("Ready to Use!")
        print("  1. Go to http://localhost:5000/pos/multilayer")
        print("  2. Or click 'Quote Builder' in sidebar")
        print("  3. Or click 'Build Quote' from any job")
        print()

if __name__ == "__main__":
    seed_comprehensive_pos()
