"""
Seed script to map TradeCategory to JobSpecification
This defines which job specs are relevant for each trade category
"""

import sys
import codecs
# Set stdout to UTF-8 encoding
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
else:
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

from app import create_app
from models import db, TradeCategory, JobSpecification

def seed_trade_spec_mappings():
    """Map trade categories to relevant job specifications"""
    app, _, _ = create_app()

    with app.app_context():
        # Define the mappings
        mappings = {
            'Sitework & Foundation': [
                'place_and_permits',
                'excavation_grading',
                'concrete',
                'masonry'
            ],
            'Framing': [
                'floor_framing',
                'wall_framing',
                'roof_framing'
            ],
            'Exterior Envelope': [
                'roof_covering',
                'flashing',
                'exterior_trim',
                'porches_decks',
                'siding',
                'doors_trim',
                'windows_trim'
            ],
            'MEP (Mechanical, Electrical, Plumbing)': [
                'plumbing',
                'hvac',
                'electrical'
            ],
            'Insulation & Drywall': [
                'insulation',
                'interior_wall_covering',
                'ceiling_covering'
            ],
            'Interior Finishes': [
                'millwork_trim',
                'stairs',
                'cabinets_appliances',
                'floor_covering',
                'doors_trim'  # Interior doors
            ],
            'Painting & Specialties': [
                'painting_decorating',
                'specialties'
            ],
            'Final & Cleanup': [
                'cleanup',
                'tearout_demolition'
            ]
        }

        # Clear existing mappings
        print("Clearing existing trade-spec mappings...")
        for trade in TradeCategory.query.all():
            trade.specifications.clear()
        db.session.commit()

        # Create new mappings
        print("\nCreating trade category to job specification mappings...")
        for trade_name, spec_names in mappings.items():
            trade = TradeCategory.query.filter_by(name=trade_name).first()

            if not trade:
                print(f"Warning: Trade category '{trade_name}' not found!")
                continue

            print(f"\n{trade.icon} {trade.name}:")
            for spec_name in spec_names:
                spec = JobSpecification.query.filter_by(name=spec_name).first()

                if not spec:
                    print(f"  Warning: Job spec '{spec_name}' not found!")
                    continue

                # Add the relationship
                trade.specifications.append(spec)
                print(f"  + {spec.display_name}")

        # Commit all mappings
        db.session.commit()
        print(f"\nSuccessfully created trade-spec mappings!")

        # Print summary
        print("\n=== MAPPING SUMMARY ===")
        for trade in TradeCategory.query.order_by(TradeCategory.order_index).all():
            print(f"{trade.icon} {trade.name}: {len(trade.specifications)} specifications")

if __name__ == '__main__':
    seed_trade_spec_mappings()
