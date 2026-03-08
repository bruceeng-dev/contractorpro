"""
Setup script for Multi-Layer POS System
- Creates new database tables
- Seeds job specifications
- Provides setup instructions
"""
from app import app, db
from models import JobSpecification, POSCategorySpecMapping, POSSession

# Standard construction job specifications
JOB_SPECIFICATIONS = [
    {
        "name": "place_and_permits",
        "display_name": "Place and Permits",
        "description": "Site preparation, permits, and regulatory approvals",
        "order_index": 1
    },
    {
        "name": "tearout_demolition",
        "display_name": "Tear Out and Demolition",
        "description": "Removal of existing structures, fixtures, and materials",
        "order_index": 2
    },
    {
        "name": "excavation_grading",
        "display_name": "Excavation and Grading",
        "description": "Earth moving, grading, and site preparation",
        "order_index": 3
    },
    {
        "name": "concrete",
        "display_name": "Concrete",
        "description": "Foundation, slabs, footings, and concrete work",
        "order_index": 4
    },
    {
        "name": "masonry",
        "display_name": "Masonry",
        "description": "Brick, block, stone, and masonry work",
        "order_index": 5
    },
    {
        "name": "floor_framing",
        "display_name": "Floor Framing",
        "description": "Floor joists, subfloor, and structural floor systems",
        "order_index": 6
    },
    {
        "name": "wall_framing",
        "display_name": "Wall Framing",
        "description": "Wall studs, plates, headers, and wall structure",
        "order_index": 7
    },
    {
        "name": "roof_framing",
        "display_name": "Roof Framing",
        "description": "Rafters, trusses, roof decking, and structural roof",
        "order_index": 8
    },
    {
        "name": "roof_covering",
        "display_name": "Roof Covering",
        "description": "Shingles, tiles, metal roofing, and waterproofing",
        "order_index": 9
    },
    {
        "name": "flashing",
        "display_name": "Flashing",
        "description": "Roof flashing, drainage, and water management",
        "order_index": 10
    },
    {
        "name": "exterior_trim",
        "display_name": "Exterior Trim",
        "description": "Fascia, soffit, rake boards, and exterior trim work",
        "order_index": 11
    },
    {
        "name": "porches_decks",
        "display_name": "Porches and Decks",
        "description": "Decks, porches, railings, and outdoor structures",
        "order_index": 12
    },
    {
        "name": "siding",
        "display_name": "Siding",
        "description": "Exterior siding, cladding, and weather protection",
        "order_index": 13
    },
    {
        "name": "doors_trim",
        "display_name": "Doors and Door Trim",
        "description": "Interior and exterior doors, frames, and trim",
        "order_index": 14
    },
    {
        "name": "windows_trim",
        "display_name": "Windows and Window Trim",
        "description": "Windows, glazing, and window trim installation",
        "order_index": 15
    },
    {
        "name": "plumbing",
        "display_name": "Plumbing",
        "description": "Water supply, drainage, fixtures, and plumbing systems",
        "order_index": 16
    },
    {
        "name": "hvac",
        "display_name": "Heating and A/C",
        "description": "HVAC systems, ductwork, and climate control",
        "order_index": 17
    },
    {
        "name": "electrical",
        "display_name": "Electrical",
        "description": "Wiring, panels, outlets, switches, and electrical systems",
        "order_index": 18
    },
    {
        "name": "insulation",
        "display_name": "Insulation",
        "description": "Thermal and sound insulation for walls, ceilings, floors",
        "order_index": 19
    },
    {
        "name": "interior_wall_covering",
        "display_name": "Interior Wall Covering",
        "description": "Drywall, plaster, paneling, and wall finishes",
        "order_index": 20
    },
    {
        "name": "ceiling_covering",
        "display_name": "Ceiling Covering",
        "description": "Ceiling drywall, tiles, and ceiling finishes",
        "order_index": 21
    },
    {
        "name": "millwork_trim",
        "display_name": "Millwork Trim",
        "description": "Baseboards, crown molding, chair rail, and interior trim",
        "order_index": 22
    },
    {
        "name": "stairs",
        "display_name": "Stairs",
        "description": "Stairways, railings, treads, and risers",
        "order_index": 23
    },
    {
        "name": "cabinets_appliances",
        "display_name": "Cabinets and Appliances",
        "description": "Kitchen cabinets, bathroom vanities, and appliances",
        "order_index": 24
    },
    {
        "name": "specialties",
        "display_name": "Specialties",
        "description": "Mirrors, shelving, hardware, and specialty items",
        "order_index": 25
    },
    {
        "name": "floor_covering",
        "display_name": "Floor Covering",
        "description": "Flooring materials, tile, carpet, hardwood, vinyl",
        "order_index": 26
    },
    {
        "name": "painting_decorating",
        "display_name": "Painting and Decorating",
        "description": "Interior and exterior painting, staining, finishing",
        "order_index": 27
    },
    {
        "name": "cleanup",
        "display_name": "Clean Up",
        "description": "Final cleaning, debris removal, and site cleanup",
        "order_index": 28
    }
]

def setup_multilayer_pos():
    """Setup multi-layer POS system"""

    with app.app_context():
        print("="*70)
        print("MULTI-LAYER POS SYSTEM SETUP")
        print("="*70)
        print()

        # Step 1: Create tables
        print("Step 1: Creating database tables...")
        try:
            db.create_all()
            print("  ✓ Tables created successfully")
        except Exception as e:
            print(f"  ✗ Error creating tables: {e}")
            return

        # Step 2: Seed job specifications
        print("\nStep 2: Seeding job specifications...")
        existing_count = JobSpecification.query.count()

        if existing_count > 0:
            print(f"  Found {existing_count} existing job specifications")
            response = input("  Clear and re-seed? (yes/no): ")
            if response.lower() == 'yes':
                JobSpecification.query.delete()
                db.session.commit()
                print("  Cleared existing specifications")
            else:
                print("  Keeping existing specifications")
                print()
                display_summary()
                return

        added_count = 0
        for spec_data in JOB_SPECIFICATIONS:
            spec = JobSpecification(
                name=spec_data['name'],
                display_name=spec_data['display_name'],
                description=spec_data['description'],
                order_index=spec_data['order_index'],
                is_active=True
            )
            db.session.add(spec)
            added_count += 1

        db.session.commit()
        print(f"  ✓ Added {added_count} job specifications")

        # Display summary
        print()
        display_summary()

def display_summary():
    """Display setup summary and next steps"""
    with app.app_context():
        print("="*70)
        print("SETUP COMPLETE!")
        print("="*70)
        print()

        # Display specifications
        all_specs = JobSpecification.query.order_by(JobSpecification.order_index).all()
        print(f"Job Specifications ({len(all_specs)} total):")
        print("-"*70)
        for spec in all_specs:
            print(f"  {spec.order_index:2d}. {spec.display_name:<30s}")
        print()

        # Display next steps
        print("="*70)
        print("NEXT STEPS:")
        print("="*70)
        print()
        print("1. START THE APPLICATION:")
        print("   python app.py")
        print()
        print("2. CREATE POS CATEGORIES:")
        print("   Navigate to: http://localhost:5000/pos/admin")
        print("   Create categories like Kitchen, Bathroom, Roofing, etc.")
        print()
        print("3. ADD ACTIVITIES TO CATEGORIES:")
        print("   In POS Admin, add activities to each category")
        print("   Example: For 'Kitchen' category, add activities like:")
        print("   - New Cabinets ($5000)")
        print("   - Countertop Installation ($2500)")
        print("   - Sink and Faucet ($800)")
        print()
        print("4. MAP CATEGORIES TO JOB SPECIFICATIONS:")
        print("   Navigate to: http://localhost:5000/pos/admin/spec-mappings")
        print("   For each category, check which job specs apply")
        print("   Example: 'Kitchen' category might map to:")
        print("   - Plumbing")
        print("   - Electrical")
        print("   - Cabinets and Appliances")
        print("   - Floor Covering")
        print("   - Painting and Decorating")
        print()
        print("5. USE THE MULTI-LAYER POS SYSTEM:")
        print("   Navigate to: http://localhost:5000/pos/multilayer")
        print("   - Layer 1: Select job specifications (e.g., Plumbing, Electrical)")
        print("   - Layer 2: See only filtered categories/activities")
        print("   - Build quote with curated options")
        print()
        print("="*70)
        print("SYSTEM ARCHITECTURE:")
        print("="*70)
        print()
        print("Database Models:")
        print("  • JobSpecification - 28 standard construction specifications")
        print("  • POSCategorySpecMapping - Links categories to specifications")
        print("  • POSSession - Tracks user selections across layers")
        print()
        print("Routes:")
        print("  • GET  /pos/multilayer - Multi-layer interface")
        print("  • GET  /api/pos/job-specifications - Get all specifications")
        print("  • POST /api/pos/session/start - Start new session")
        print("  • GET  /api/pos/session/{token}/categories - Filtered categories")
        print("  • GET  /pos/admin/spec-mappings - Admin mapping interface")
        print("  • POST /api/pos/spec-mappings - Save category mappings")
        print()
        print("="*70)
        print()

if __name__ == '__main__':
    setup_multilayer_pos()
