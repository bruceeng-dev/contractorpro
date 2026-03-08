"""
Automatically tag POS activities with relevant job specifications
"""
from app import app, db
from models import POSActivity
import json

# Mapping of keywords to job spec names
TAG_RULES = {
    # Demolition & Site Work
    'demolition': ['tearout_demolition'],
    'removal': ['tearout_demolition'],
    'tear': ['tearout_demolition'],
    'dumpster': ['tearout_demolition', 'cleanup'],

    # Plumbing
    'plumbing': ['plumbing'],
    'sink': ['plumbing'],
    'faucet': ['plumbing'],
    'toilet': ['plumbing'],
    'shower': ['plumbing'],
    'tub': ['plumbing'],
    'bathtub': ['plumbing'],
    'disposal': ['plumbing'],
    'water': ['plumbing'],
    'drain': ['plumbing'],
    'bidet': ['plumbing'],
    'ice maker': ['plumbing'],
    'gas line': ['plumbing'],
    'pot filler': ['plumbing'],

    # Electrical
    'electrical': ['electrical'],
    'wiring': ['electrical'],
    'lighting': ['electrical'],
    'light': ['electrical'],
    'outlet': ['electrical'],
    'switch': ['electrical'],
    'dimmer': ['electrical'],
    'circuit': ['electrical'],
    'panel': ['electrical'],
    'gfci': ['electrical'],
    'recessed': ['electrical'],
    'pendant': ['electrical'],

    # HVAC
    'ventilation': ['hvac'],
    'heating': ['hvac'],
    'fan': ['hvac'],

    # Cabinets & Appliances
    'cabinet': ['cabinets_appliances'],
    'vanity': ['cabinets_appliances'],
    'island': ['cabinets_appliances'],
    'pantry': ['cabinets_appliances'],
    'appliance': ['cabinets_appliances'],
    'dishwasher': ['cabinets_appliances'],
    'range': ['cabinets_appliances'],
    'oven': ['cabinets_appliances'],
    'cooktop': ['cabinets_appliances'],
    'hood': ['cabinets_appliances'],
    'microwave': ['cabinets_appliances'],
    'refrigerator': ['cabinets_appliances'],
    'wine': ['cabinets_appliances'],

    # Flooring
    'flooring': ['floor_covering'],
    'floor': ['floor_covering'],
    'hardwood': ['floor_covering'],
    'tile': ['floor_covering'],
    'vinyl': ['floor_covering'],
    'laminate': ['floor_covering'],
    'carpet': ['floor_covering'],
    'cork': ['floor_covering'],
    'bamboo': ['floor_covering'],
    'subfloor': ['floor_covering', 'floor_framing'],
    'underlayment': ['floor_covering'],

    # Countertops
    'countertop': ['cabinets_appliances'],

    # Backsplash & Tile
    'backsplash': ['interior_wall_covering'],
    'wall tile': ['interior_wall_covering'],

    # Painting & Decorating
    'painting': ['painting_decorating'],
    'paint': ['painting_decorating'],
    'staining': ['painting_decorating'],

    # Drywall & Wall Covering
    'drywall': ['interior_wall_covering'],
    'greenboard': ['interior_wall_covering'],
    'wainscoting': ['interior_wall_covering'],
    'beadboard': ['interior_wall_covering'],

    # Trim & Millwork
    'molding': ['millwork_trim'],
    'trim': ['millwork_trim'],
    'baseboard': ['millwork_trim'],
    'crown': ['millwork_trim'],

    # Windows & Doors
    'window': ['windows_trim'],
    'door': ['doors_trim'],
    'french door': ['doors_trim'],
    'patio door': ['doors_trim'],

    # Roofing
    'roof': ['roof_covering', 'roof_framing'],
    'shingle': ['roof_covering'],
    'metal roof': ['roof_covering'],
    'decking': ['roof_framing'],
    'underlayment': ['roof_covering'],
    'flashing': ['flashing'],
    'gutter': ['flashing'],
    'downspout': ['flashing'],
    'fascia': ['exterior_trim'],
    'soffit': ['exterior_trim'],
    'vent': ['hvac'],
    'skylight': ['windows_trim', 'roof_covering'],

    # Outdoor/Deck
    'deck': ['porches_decks'],
    'patio': ['porches_decks', 'concrete'],
    'pergola': ['porches_decks'],
    'porch': ['porches_decks'],
    'railing': ['porches_decks'],

    # Concrete
    'concrete': ['concrete'],
    'paver': ['masonry'],

    # Specialties
    'mirror': ['specialties'],
    'medicine cabinet': ['specialties'],
    'towel': ['specialties'],
    'shelving': ['specialties'],
    'hardware': ['specialties'],
    'accessories': ['specialties'],
}

def auto_tag_activities():
    """Automatically tag activities based on name keywords"""

    with app.app_context():
        print("="*70)
        print("AUTO-TAGGING POS ACTIVITIES")
        print("="*70)
        print()

        activities = POSActivity.query.all()
        tagged_count = 0

        for activity in activities:
            activity_name_lower = activity.name.lower()
            activity_tags = set()

            # Check each rule
            for keyword, specs in TAG_RULES.items():
                if keyword in activity_name_lower:
                    activity_tags.update(specs)

            if activity_tags:
                # Convert to JSON array
                activity.job_spec_tags = json.dumps(list(activity_tags))
                tagged_count += 1
                print(f"[OK] {activity.name}")
                print(f"  Tags: {', '.join(activity_tags)}")
            else:
                print(f"[WARN] {activity.name} - No tags matched")

        db.session.commit()

        print()
        print("="*70)
        print(f"SUCCESS! Tagged {tagged_count} out of {len(activities)} activities")
        print("="*70)
        print()
        print("You can now test the multi-layer POS system:")
        print("1. Go to http://localhost:5000/pos/multilayer")
        print("2. Select job specs like 'Plumbing' and 'Electrical'")
        print("3. Continue to categories")
        print("4. Click 'Bathroom' - you'll see ONLY plumbing/electrical activities!")
        print()

if __name__ == '__main__':
    auto_tag_activities()
