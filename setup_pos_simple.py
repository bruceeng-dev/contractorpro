"""
Simple POS Setup Script - Initializes database tables and seeds job specifications
"""
from app import app, db
from models import JobSpecification

# Standard construction job specifications
JOB_SPECIFICATIONS = [
    {"name": "place_and_permits", "display_name": "Place and Permits", "description": "Site preparation, permits, and regulatory approvals", "order_index": 1},
    {"name": "tearout_demolition", "display_name": "Tear Out and Demolition", "description": "Removal of existing structures, fixtures, and materials", "order_index": 2},
    {"name": "excavation_grading", "display_name": "Excavation and Grading", "description": "Earth moving, grading, and site preparation", "order_index": 3},
    {"name": "concrete", "display_name": "Concrete", "description": "Foundation, slabs, footings, and concrete work", "order_index": 4},
    {"name": "masonry", "display_name": "Masonry", "description": "Brick, block, stone, and masonry work", "order_index": 5},
    {"name": "floor_framing", "display_name": "Floor Framing", "description": "Floor joists, subfloor, and structural floor systems", "order_index": 6},
    {"name": "wall_framing", "display_name": "Wall Framing", "description": "Wall studs, plates, headers, and wall structure", "order_index": 7},
    {"name": "roof_framing", "display_name": "Roof Framing", "description": "Rafters, trusses, roof decking, and structural roof", "order_index": 8},
    {"name": "roof_covering", "display_name": "Roof Covering", "description": "Shingles, tiles, metal roofing, and waterproofing", "order_index": 9},
    {"name": "flashing", "display_name": "Flashing", "description": "Roof flashing, drainage, and water management", "order_index": 10},
    {"name": "exterior_trim", "display_name": "Exterior Trim", "description": "Fascia, soffit, rake boards, and exterior trim work", "order_index": 11},
    {"name": "porches_decks", "display_name": "Porches and Decks", "description": "Decks, porches, railings, and outdoor structures", "order_index": 12},
    {"name": "siding", "display_name": "Siding", "description": "Exterior siding, cladding, and weather protection", "order_index": 13},
    {"name": "doors_trim", "display_name": "Doors and Door Trim", "description": "Interior and exterior doors, frames, and trim", "order_index": 14},
    {"name": "windows_trim", "display_name": "Windows and Window Trim", "description": "Windows, glazing, and window trim installation", "order_index": 15},
    {"name": "plumbing", "display_name": "Plumbing", "description": "Water supply, drainage, fixtures, and plumbing systems", "order_index": 16},
    {"name": "heating_ac", "display_name": "Heating and A/C", "description": "HVAC systems, ductwork, and climate control", "order_index": 17},
    {"name": "electrical", "display_name": "Electrical", "description": "Wiring, panels, outlets, and electrical systems", "order_index": 18},
    {"name": "insulation", "display_name": "Insulation", "description": "Thermal and sound insulation systems", "order_index": 19},
    {"name": "interior_wall_covering", "display_name": "Interior Wall Covering", "description": "Drywall, plaster, paneling, and wall finishes", "order_index": 20},
    {"name": "ceiling_covering", "display_name": "Ceiling Covering", "description": "Ceiling finishes and treatments", "order_index": 21},
    {"name": "millwork_trim", "display_name": "Millwork Trim", "description": "Baseboards, crown molding, and interior trim", "order_index": 22},
    {"name": "stairs", "display_name": "Stairs", "description": "Stairways, railings, and stair systems", "order_index": 23},
    {"name": "cabinets_appliances", "display_name": "Cabinets and Appliances", "description": "Kitchen and bathroom cabinetry and appliances", "order_index": 24},
    {"name": "specialties", "display_name": "Specialties", "description": "Mirrors, shelving, hardware, and specialty items", "order_index": 25},
    {"name": "floor_covering", "display_name": "Floor Covering", "description": "Tile, carpet, hardwood, and floor finishes", "order_index": 26},
    {"name": "painting_decorating", "display_name": "Painting and Decorating", "description": "Interior and exterior painting and finishing", "order_index": 27},
    {"name": "cleanup", "display_name": "Clean Up", "description": "Final cleaning, debris removal, and site cleanup", "order_index": 28}
]

def setup_pos():
    with app.app_context():
        print("=" * 70)
        print("MULTI-LAYER POS SYSTEM SETUP")
        print("=" * 70)
        print()

        # Create tables
        print("Step 1: Creating database tables...")
        try:
            db.create_all()
            print("  [OK] Tables created successfully")
        except Exception as e:
            print(f"  [ERROR] Error creating tables: {e}")
            return

        # Seed job specifications
        print("\nStep 2: Seeding job specifications...")
        existing_count = JobSpecification.query.count()

        if existing_count > 0:
            print(f"  Found {existing_count} existing job specifications")
            print("  Skipping seed (already populated)")
        else:
            try:
                for spec_data in JOB_SPECIFICATIONS:
                    spec = JobSpecification(**spec_data)
                    db.session.add(spec)

                db.session.commit()
                print(f"  [OK] Seeded {len(JOB_SPECIFICATIONS)} job specifications")
            except Exception as e:
                db.session.rollback()
                print(f"  [ERROR] Error seeding specifications: {e}")
                return

        # Summary
        print("\n" + "=" * 70)
        print("SETUP COMPLETE")
        print("=" * 70)
        print()
        print("Next Steps:")
        print("1. Navigate to http://localhost:5000/pos/multilayer to start building quotes")
        print("2. Or click 'Quote Builder' in the sidebar navigation")
        print("3. From any job detail page, click 'Build Quote' button")
        print()
        print("Admin Configuration:")
        print("- Create POS categories at: /pos/admin")
        print("- Map categories to job specs at: /pos/admin/spec-mappings")
        print()

if __name__ == "__main__":
    setup_pos()
