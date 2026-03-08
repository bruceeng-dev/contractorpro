"""
Seed script for broad trade categories
Run with: python seed_trade_categories.py
"""
from app import create_app
from models import db, TradeCategory

def seed_trade_categories():
    app, _, _ = create_app()

    with app.app_context():
        print("Seeding Trade Categories...")

        # Check if already seeded
        existing = TradeCategory.query.first()
        if existing:
            print("Trade categories already exist. Skipping seed.")
            return

        # Define the 8 broad trade categories
        categories = [
            {
                'name': 'Sitework & Foundation',
                'description': 'Site preparation, excavation, concrete, masonry',
                'icon': '🏗️',
                'color': '#8B4513',
                'order_index': 1
            },
            {
                'name': 'Framing',
                'description': 'Floor, wall, and roof framing, structural carpentry',
                'icon': '🔨',
                'color': '#D2691E',
                'order_index': 2
            },
            {
                'name': 'Exterior Envelope',
                'description': 'Roofing, siding, windows, doors, trim',
                'icon': '🏠',
                'color': '#4682B4',
                'order_index': 3
            },
            {
                'name': 'MEP (Mechanical, Electrical, Plumbing)',
                'description': 'Plumbing, HVAC, electrical systems',
                'icon': '⚡',
                'color': '#FFD700',
                'order_index': 4
            },
            {
                'name': 'Insulation & Drywall',
                'description': 'Insulation, drywall installation and finishing',
                'icon': '📐',
                'color': '#A9A9A9',
                'order_index': 5
            },
            {
                'name': 'Interior Finishes',
                'description': 'Trim, doors, cabinets, flooring',
                'icon': '🚪',
                'color': '#CD853F',
                'order_index': 6
            },
            {
                'name': 'Painting & Specialties',
                'description': 'Painting, staining, special installations',
                'icon': '🎨',
                'color': '#FF6347',
                'order_index': 7
            },
            {
                'name': 'Final & Cleanup',
                'description': 'Final cleaning, punch list, project closeout',
                'icon': '✨',
                'color': '#32CD32',
                'order_index': 8
            }
        ]

        # Create trade categories
        for cat_data in categories:
            category = TradeCategory(**cat_data)
            db.session.add(category)

        db.session.commit()

        print(f"\n✓ Successfully added {len(categories)} trade categories!")
        print("\nTrade Categories:")
        for cat in categories:
            print(f"  {cat['icon']} {cat['name']}")

        print("\nYou can now use these categories when creating jobs!")

if __name__ == '__main__':
    seed_trade_categories()
