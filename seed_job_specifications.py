"""
Seed database with standard construction job specifications for multi-layer POS system
"""
from app import app, db
from models import JobSpecification

# Standard CSI MasterFormat-inspired job specifications
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

def seed_job_specifications():
    """Add all standard job specifications to the database"""

    with app.app_context():
        print("Seeding job specifications...")

        # Check if specifications already exist
        existing_count = JobSpecification.query.count()
        if existing_count > 0:
            print(f"Found {existing_count} existing specifications.")
            response = input("Do you want to clear and re-seed? (yes/no): ")
            if response.lower() == 'yes':
                JobSpecification.query.delete()
                db.session.commit()
                print("Cleared existing specifications.")
            else:
                print("Keeping existing specifications. Exiting.")
                return

        # Add all specifications
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
            print(f"  + {spec_data['display_name']}")

        db.session.commit()
        print(f"\n✓ Successfully added {added_count} job specifications!")

        # Display summary
        print("\n" + "="*60)
        print("Job Specification Summary:")
        print("="*60)
        all_specs = JobSpecification.query.order_by(JobSpecification.order_index).all()
        for spec in all_specs:
            print(f"{spec.order_index:2d}. {spec.display_name:<30s} [{spec.name}]")
        print("="*60)

if __name__ == '__main__':
    seed_job_specifications()
