"""
Seed job specifications organized by construction sections
"""
from app import app, db
from models import JobSpecification

# Job specifications organized by section
JOB_SPECS_BY_SECTION = {
    "Site Work & Permits": [
        {"name": "place_and_permits", "display_name": "Place and Permits", "description": "Site preparation, permits, and regulatory approvals"},
        {"name": "tearout_demolition", "display_name": "Tear Out and Demolition", "description": "Removal of existing structures, fixtures, and materials"},
        {"name": "excavation_grading", "display_name": "Excavation and Grading", "description": "Earth moving, grading, and site preparation"},
    ],

    "Foundation & Structure": [
        {"name": "concrete", "display_name": "Concrete", "description": "Foundation, slabs, footings, and concrete work"},
        {"name": "masonry", "display_name": "Masonry", "description": "Brick, block, stone, and masonry work"},
        {"name": "floor_framing", "display_name": "Floor Framing", "description": "Floor joists, subfloor, and structural floor systems"},
        {"name": "wall_framing", "display_name": "Wall Framing", "description": "Wall studs, plates, headers, and wall structure"},
        {"name": "roof_framing", "display_name": "Roof Framing", "description": "Rafters, trusses, roof decking, and structural roof"},
    ],

    "Exterior": [
        {"name": "roof_covering", "display_name": "Roof Covering", "description": "Shingles, tiles, metal roofing, and waterproofing"},
        {"name": "flashing", "display_name": "Flashing", "description": "Roof flashing, drainage, and water management"},
        {"name": "exterior_trim", "display_name": "Exterior Trim", "description": "Fascia, soffit, rake boards, and exterior trim work"},
        {"name": "porches_decks", "display_name": "Porches and Decks", "description": "Decks, porches, railings, and outdoor structures"},
        {"name": "siding", "display_name": "Siding", "description": "Exterior siding, cladding, and weather protection"},
    ],

    "Openings": [
        {"name": "doors_trim", "display_name": "Doors and Door Trim", "description": "Interior and exterior doors, frames, and trim"},
        {"name": "windows_trim", "display_name": "Windows and Window Trim", "description": "Windows, glazing, and window trim installation"},
    ],

    "MEP Systems": [
        {"name": "plumbing", "display_name": "Plumbing", "description": "Water supply, drainage, fixtures, and plumbing systems"},
        {"name": "hvac", "display_name": "Heating and A/C", "description": "HVAC systems, ductwork, and climate control"},
        {"name": "electrical", "display_name": "Electrical", "description": "Wiring, panels, outlets, switches, and electrical systems"},
    ],

    "Insulation & Walls": [
        {"name": "insulation", "display_name": "Insulation", "description": "Thermal and sound insulation for walls, ceilings, floors"},
        {"name": "interior_wall_covering", "display_name": "Interior Wall Covering", "description": "Drywall, plaster, paneling, and wall finishes"},
        {"name": "ceiling_covering", "display_name": "Ceiling Covering", "description": "Ceiling drywall, tiles, and ceiling finishes"},
    ],

    "Interior Finishes": [
        {"name": "millwork_trim", "display_name": "Millwork Trim", "description": "Baseboards, crown molding, chair rail, and interior trim"},
        {"name": "stairs", "display_name": "Stairs", "description": "Stairways, railings, treads, and risers"},
        {"name": "cabinets_appliances", "display_name": "Cabinets and Appliances", "description": "Kitchen cabinets, bathroom vanities, and appliances"},
        {"name": "specialties", "display_name": "Specialties", "description": "Mirrors, shelving, hardware, and specialty items"},
        {"name": "floor_covering", "display_name": "Floor Covering", "description": "Flooring materials, tile, carpet, hardwood, vinyl"},
        {"name": "painting_decorating", "display_name": "Painting and Decorating", "description": "Interior and exterior painting, staining, finishing"},
    ],

    "Final": [
        {"name": "cleanup", "display_name": "Clean Up", "description": "Final cleaning, debris removal, and site cleanup"},
    ]
}

def seed_sectioned_specs():
    """Seed job specifications with section organization"""

    with app.app_context():
        print("=" * 70)
        print("SEEDING JOB SPECIFICATIONS BY SECTION")
        print("=" * 70)
        print()

        # Check if specs already exist
        existing_count = JobSpecification.query.count()
        if existing_count > 0:
            print(f"Found {existing_count} existing job specifications")
            response = input("Clear and re-seed? (yes/no): ")
            if response.lower() != 'yes':
                print("Keeping existing specifications. Exiting.")
                return

            JobSpecification.query.delete()
            db.session.commit()
            print("Cleared existing specifications")
            print()

        # Add specifications by section
        order_index = 1
        total_added = 0

        for section_name, specs in JOB_SPECS_BY_SECTION.items():
            print(f"{section_name}:")
            print("-" * 70)

            for spec_data in specs:
                spec = JobSpecification(
                    name=spec_data['name'],
                    display_name=spec_data['display_name'],
                    description=spec_data['description'],
                    section=section_name,
                    order_index=order_index,
                    is_active=True
                )
                db.session.add(spec)
                print(f"  {order_index:2d}. {spec_data['display_name']}")
                order_index += 1
                total_added += 1

            print()

        db.session.commit()
        print("=" * 70)
        print(f"SUCCESS! Added {total_added} job specifications in {len(JOB_SPECS_BY_SECTION)} sections")
        print("=" * 70)
        print()
        print("Next steps:")
        print("1. Restart the Flask app if it's running")
        print("2. Go to http://localhost:5000/pos/multilayer")
        print("3. You'll see job specs organized by section!")
        print()

if __name__ == '__main__':
    seed_sectioned_specs()
