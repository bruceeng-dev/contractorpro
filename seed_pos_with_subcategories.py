"""
Updated POS Seed Script with Subcategory Organization
Activities within each category are now grouped by subcategory
"""

from app import app
from models import db, User, POSCategory, POSActivity, POSSubItem
from decimal import Decimal

def seed_pos_with_subcategories():
    """Seed POS data with subcategory organization"""
    with app.app_context():
        user = User.query.first()
        if not user:
            print("ERROR: No users found. Please create a user first.")
            return

        print(f"Seeding POS data with subcategories for user: {user.username}")

        # Delete existing data
        existing = POSCategory.query.filter_by(user_id=user.id).count()
        if existing > 0:
            print(f"Deleting {existing} existing categories...")
            POSCategory.query.filter_by(user_id=user.id).delete()
            db.session.commit()

        # ========================================
        # FLOORING - WITH SUBCATEGORIES
        # ========================================
        print("\n[1/6] Creating Flooring with subcategories...")
        flooring_cat = POSCategory(
            user_id=user.id,
            name="Flooring",
            description="All types of flooring installation",
            keywords="floor,tile,wood,carpet,vinyl,laminate",
            icon="📐"
        )
        db.session.add(flooring_cat)
        db.session.flush()

        flooring_activities = [
            # TILE OPTIONS
            {'name': 'Ceramic Tile Installation', 'subcategory': 'Tile Options', 'desc': 'Standard ceramic floor tiles', 'cost': Decimal('12'), 'unit': 'sqft', 'order': 1},
            {'name': 'Porcelain Tile Installation', 'subcategory': 'Tile Options', 'desc': 'Premium porcelain floor tiles', 'cost': Decimal('15'), 'unit': 'sqft', 'order': 2},
            {'name': 'Natural Stone Tile', 'subcategory': 'Tile Options', 'desc': 'Marble, travertine, slate tiles', 'cost': Decimal('25'), 'unit': 'sqft', 'order': 3},
            {'name': 'Large Format Tile', 'subcategory': 'Tile Options', 'desc': '12x24, 24x24 tiles', 'cost': Decimal('18'), 'unit': 'sqft', 'order': 4},
            {'name': 'Mosaic Tile', 'subcategory': 'Tile Options', 'desc': 'Small mosaic pattern tiles', 'cost': Decimal('22'), 'unit': 'sqft', 'order': 5},

            # WOOD FLOORING
            {'name': 'Solid Hardwood', 'subcategory': 'Wood Flooring', 'desc': '3/4" solid oak, maple, or cherry', 'cost': Decimal('18'), 'unit': 'sqft', 'order': 10},
            {'name': 'Engineered Hardwood', 'subcategory': 'Wood Flooring', 'desc': 'Multi-layer engineered planks', 'cost': Decimal('14'), 'unit': 'sqft', 'order': 11},
            {'name': 'Luxury Vinyl Plank (LVP)', 'subcategory': 'Wood Flooring', 'desc': 'Wood-look vinyl planks', 'cost': Decimal('8'), 'unit': 'sqft', 'order': 12},
            {'name': 'Laminate Flooring', 'subcategory': 'Wood Flooring', 'desc': 'Snap-together laminate', 'cost': Decimal('6'), 'unit': 'sqft', 'order': 13},

            # SOFT FLOORING
            {'name': 'Carpet Installation', 'subcategory': 'Soft Flooring', 'desc': 'Wall-to-wall carpeting', 'cost': Decimal('7'), 'unit': 'sqft', 'order': 20},
            {'name': 'Premium Carpet', 'subcategory': 'Soft Flooring', 'desc': 'Upgraded plush or Berber', 'cost': Decimal('12'), 'unit': 'sqft', 'order': 21},
            {'name': 'Carpet Padding', 'subcategory': 'Soft Flooring', 'desc': 'Premium carpet underlay', 'cost': Decimal('2'), 'unit': 'sqft', 'order': 22},
            {'name': 'Sheet Vinyl', 'subcategory': 'Soft Flooring', 'desc': 'Roll vinyl flooring', 'cost': Decimal('5'), 'unit': 'sqft', 'order': 23},

            # TRIM & FINISHING
            {'name': 'Baseboard Installation', 'subcategory': 'Trim & Finishing', 'desc': '4-6" baseboards with finish', 'cost': Decimal('8'), 'unit': 'linear_ft', 'order': 30},
            {'name': 'Quarter Round', 'subcategory': 'Trim & Finishing', 'desc': 'Floor transition trim', 'cost': Decimal('3'), 'unit': 'linear_ft', 'order': 31},
            {'name': 'Transition Strips', 'subcategory': 'Trim & Finishing', 'desc': 'Metal or wood transitions', 'cost': Decimal('25'), 'unit': 'each', 'order': 32},
            {'name': 'Stair Nosing', 'subcategory': 'Trim & Finishing', 'desc': 'Stair edge protection', 'cost': Decimal('35'), 'unit': 'linear_ft', 'order': 33},

            # PREP & DEMOLITION
            {'name': 'Floor Removal', 'subcategory': 'Prep & Demolition', 'desc': 'Remove existing flooring', 'cost': Decimal('3'), 'unit': 'sqft', 'order': 40},
            {'name': 'Subfloor Repair', 'subcategory': 'Prep & Demolition', 'desc': 'Replace damaged subfloor', 'cost': Decimal('6'), 'unit': 'sqft', 'order': 41},
            {'name': 'Self-Leveling Compound', 'subcategory': 'Prep & Demolition', 'desc': 'Level uneven concrete', 'cost': Decimal('4'), 'unit': 'sqft', 'order': 42},
            {'name': 'Moisture Barrier', 'subcategory': 'Prep & Demolition', 'desc': 'Vapor barrier installation', 'cost': Decimal('1.50'), 'unit': 'sqft', 'order': 43},
        ]

        for idx, act in enumerate(flooring_activities):
            activity = POSActivity(
                category_id=flooring_cat.id,
                name=act['name'],
                subcategory=act.get('subcategory'),
                description=act['desc'],
                base_cost=act['cost'],
                unit=act.get('unit', 'each'),
                has_subitems=False,
                order_index=act.get('order', idx)
            )
            db.session.add(activity)

        print(f"   Created {len(flooring_activities)} flooring activities in subcategories")

        # ========================================
        # KITCHEN RENOVATION - WITH SUBCATEGORIES
        # ========================================
        print("\n[2/6] Creating Kitchen with subcategories...")
        kitchen_cat = POSCategory(
            user_id=user.id,
            name="Kitchen Renovation",
            description="Complete kitchen remodeling",
            keywords="kitchen,cabinets,countertops,appliances",
            icon="🍳"
        )
        db.session.add(kitchen_cat)
        db.session.flush()

        kitchen_activities = [
            # CABINETRY
            {'name': 'Upper Cabinets', 'subcategory': 'Cabinetry', 'desc': 'Wall-mounted cabinets', 'cost': Decimal('3500'), 'unit': 'linear_ft', 'order': 1},
            {'name': 'Lower Cabinets', 'subcategory': 'Cabinetry', 'desc': 'Base cabinets with drawers', 'cost': Decimal('4500'), 'unit': 'linear_ft', 'order': 2},
            {'name': 'Kitchen Island', 'subcategory': 'Cabinetry', 'desc': 'Custom island with storage', 'cost': Decimal('3000'), 'unit': 'each', 'order': 3},
            {'name': 'Pantry Cabinets', 'subcategory': 'Cabinetry', 'desc': 'Floor-to-ceiling pantry', 'cost': Decimal('1800'), 'unit': 'each', 'order': 4},
            {'name': 'Cabinet Hardware', 'subcategory': 'Cabinetry', 'desc': 'Knobs and pulls', 'cost': Decimal('8'), 'unit': 'each', 'order': 5},

            # COUNTERTOPS
            {'name': 'Laminate Countertops', 'subcategory': 'Countertops', 'desc': 'Budget-friendly laminate', 'cost': Decimal('25'), 'unit': 'sqft', 'order': 10},
            {'name': 'Granite Countertops', 'subcategory': 'Countertops', 'desc': 'Natural granite slabs', 'cost': Decimal('65'), 'unit': 'sqft', 'order': 11},
            {'name': 'Quartz Countertops', 'subcategory': 'Countertops', 'desc': 'Engineered quartz', 'cost': Decimal('80'), 'unit': 'sqft', 'order': 12},
            {'name': 'Marble Countertops', 'subcategory': 'Countertops', 'desc': 'Premium marble', 'cost': Decimal('100'), 'unit': 'sqft', 'order': 13},
            {'name': 'Edge Profile', 'subcategory': 'Countertops', 'desc': 'Custom edge finishing', 'cost': Decimal('15'), 'unit': 'linear_ft', 'order': 14},

            # BACKSPLASH
            {'name': 'Ceramic Tile Backsplash', 'subcategory': 'Backsplash', 'desc': '4x4 ceramic tiles', 'cost': Decimal('12'), 'unit': 'sqft', 'order': 20},
            {'name': 'Subway Tile Backsplash', 'subcategory': 'Backsplash', 'desc': '3x6 subway tiles', 'cost': Decimal('15'), 'unit': 'sqft', 'order': 21},
            {'name': 'Glass Mosaic Backsplash', 'subcategory': 'Backsplash', 'desc': 'Glass mosaic tiles', 'cost': Decimal('25'), 'unit': 'sqft', 'order': 22},
            {'name': 'Natural Stone Backsplash', 'subcategory': 'Backsplash', 'desc': 'Stone backsplash', 'cost': Decimal('35'), 'unit': 'sqft', 'order': 23},

            # SINKS & PLUMBING
            {'name': 'Stainless Steel Sink', 'subcategory': 'Sinks & Plumbing', 'desc': 'Undermount stainless', 'cost': Decimal('500'), 'unit': 'each', 'order': 30},
            {'name': 'Farmhouse Sink', 'subcategory': 'Sinks & Plumbing', 'desc': 'Apron front sink', 'cost': Decimal('900'), 'unit': 'each', 'order': 31},
            {'name': 'Kitchen Faucet', 'subcategory': 'Sinks & Plumbing', 'desc': 'Pull-down faucet', 'cost': Decimal('350'), 'unit': 'each', 'order': 32},
            {'name': 'Garbage Disposal', 'subcategory': 'Sinks & Plumbing', 'desc': '1/2 HP disposal', 'cost': Decimal('250'), 'unit': 'each', 'order': 33},
            {'name': 'Water Filtration', 'subcategory': 'Sinks & Plumbing', 'desc': 'Under-sink filter', 'cost': Decimal('600'), 'unit': 'each', 'order': 34},

            # APPLIANCES
            {'name': 'Dishwasher Installation', 'subcategory': 'Appliances', 'desc': 'Built-in dishwasher', 'cost': Decimal('800'), 'unit': 'each', 'order': 40},
            {'name': 'Range Installation', 'subcategory': 'Appliances', 'desc': 'Slide-in range', 'cost': Decimal('1200'), 'unit': 'each', 'order': 41},
            {'name': 'Range Hood', 'subcategory': 'Appliances', 'desc': 'Ventilation hood', 'cost': Decimal('800'), 'unit': 'each', 'order': 42},
            {'name': 'Microwave Installation', 'subcategory': 'Appliances', 'desc': 'Over-range microwave', 'cost': Decimal('500'), 'unit': 'each', 'order': 43},

            # DEMOLITION
            {'name': 'Kitchen Demolition', 'subcategory': 'Demolition', 'desc': 'Remove existing cabinets', 'cost': Decimal('1500'), 'unit': 'room', 'order': 50},
            {'name': 'Appliance Removal', 'subcategory': 'Demolition', 'desc': 'Disconnect and remove', 'cost': Decimal('200'), 'unit': 'each', 'order': 51},
            {'name': 'Dumpster Rental', 'subcategory': 'Demolition', 'desc': '20-yard dumpster', 'cost': Decimal('450'), 'unit': 'each', 'order': 52},
        ]

        for idx, act in enumerate(kitchen_activities):
            activity = POSActivity(
                category_id=kitchen_cat.id,
                name=act['name'],
                subcategory=act.get('subcategory'),
                description=act['desc'],
                base_cost=act['cost'],
                unit=act.get('unit', 'each'),
                has_subitems=False,
                order_index=act.get('order', idx)
            )
            db.session.add(activity)

        print(f"   Created {len(kitchen_activities)} kitchen activities in subcategories")

        # BATHROOM, ROOFING, PAINTING, DECKING would follow similar pattern...
        # For brevity, I'll add simplified versions

        # ========================================
        # BATHROOM - WITH SUBCATEGORIES
        # ========================================
        print("\n[3/6] Creating Bathroom with subcategories...")
        bathroom_cat = POSCategory(
            user_id=user.id,
            name="Bathroom Renovation",
            description="Complete bathroom remodeling",
            keywords="bathroom,shower,tub,vanity,toilet",
            icon="🚿"
        )
        db.session.add(bathroom_cat)
        db.session.flush()

        bathroom_activities = [
            # FIXTURES
            {'name': 'Toilet Installation', 'subcategory': 'Fixtures', 'desc': 'Standard toilet', 'cost': Decimal('450'), 'unit': 'each'},
            {'name': 'Vanity Cabinet', 'subcategory': 'Fixtures', 'desc': '48" vanity with top', 'cost': Decimal('1200'), 'unit': 'each'},
            {'name': 'Bathroom Faucet', 'subcategory': 'Fixtures', 'desc': 'Single-hole faucet', 'cost': Decimal('250'), 'unit': 'each'},

            # SHOWER & TUB
            {'name': 'Shower Pan Installation', 'subcategory': 'Shower & Tub', 'desc': 'Custom shower base', 'cost': Decimal('800'), 'unit': 'each'},
            {'name': 'Tub Installation', 'subcategory': 'Shower & Tub', 'desc': 'Standard bathtub', 'cost': Decimal('1000'), 'unit': 'each'},
            {'name': 'Glass Shower Door', 'subcategory': 'Shower & Tub', 'desc': 'Frameless glass', 'cost': Decimal('1500'), 'unit': 'each'},

            # TILE WORK
            {'name': 'Shower Tile', 'subcategory': 'Tile Work', 'desc': 'Ceramic shower walls', 'cost': Decimal('15'), 'unit': 'sqft'},
            {'name': 'Floor Tile', 'subcategory': 'Tile Work', 'desc': 'Porcelain floor tile', 'cost': Decimal('12'), 'unit': 'sqft'},
        ]

        for idx, act in enumerate(bathroom_activities):
            activity = POSActivity(
                category_id=bathroom_cat.id,
                name=act['name'],
                subcategory=act.get('subcategory'),
                description=act['desc'],
                base_cost=act['cost'],
                unit=act.get('unit', 'each'),
                has_subitems=False,
                order_index=idx
            )
            db.session.add(activity)

        print(f"   Created {len(bathroom_activities)} bathroom activities in subcategories")

        # ========================================
        # ROOFING - WITH SUBCATEGORIES
        # ========================================
        print("\n[4/6] Creating Roofing with subcategories...")
        roofing_cat = POSCategory(
            user_id=user.id,
            name="Roofing",
            description="Roof installation and repair",
            keywords="roof,shingles,metal,flat",
            icon="🏠"
        )
        db.session.add(roofing_cat)
        db.session.flush()

        roofing_activities = [
            # SHINGLE ROOFING
            {'name': '3-Tab Asphalt Shingles', 'subcategory': 'Shingle Roofing', 'desc': 'Basic shingles', 'cost': Decimal('3.50'), 'unit': 'sqft'},
            {'name': 'Architectural Shingles', 'subcategory': 'Shingle Roofing', 'desc': 'Premium dimensional', 'cost': Decimal('4.50'), 'unit': 'sqft'},
            {'name': 'Designer Shingles', 'subcategory': 'Shingle Roofing', 'desc': 'High-end shingles', 'cost': Decimal('6'), 'unit': 'sqft'},

            # METAL ROOFING
            {'name': 'Standing Seam Metal', 'subcategory': 'Metal Roofing', 'desc': 'Concealed fasteners', 'cost': Decimal('12'), 'unit': 'sqft'},
            {'name': 'Corrugated Metal', 'subcategory': 'Metal Roofing', 'desc': 'Exposed fastener', 'cost': Decimal('8'), 'unit': 'sqft'},

            # ACCESSORIES
            {'name': 'Ridge Vent', 'subcategory': 'Accessories', 'desc': 'Continuous ridge vent', 'cost': Decimal('8'), 'unit': 'linear_ft'},
            {'name': 'Gutters & Downspouts', 'subcategory': 'Accessories', 'desc': 'Aluminum gutters', 'cost': Decimal('12'), 'unit': 'linear_ft'},
            {'name': 'Ice & Water Shield', 'subcategory': 'Accessories', 'desc': 'Underlayment protection', 'cost': Decimal('2'), 'unit': 'sqft'},

            # TEAR OFF
            {'name': 'Roof Tear Off', 'subcategory': 'Tear Off', 'desc': 'Remove old shingles', 'cost': Decimal('1.50'), 'unit': 'sqft'},
            {'name': 'Roof Deck Repair', 'subcategory': 'Tear Off', 'desc': 'Plywood replacement', 'cost': Decimal('3'), 'unit': 'sqft'},
        ]

        for idx, act in enumerate(roofing_activities):
            activity = POSActivity(
                category_id=roofing_cat.id,
                name=act['name'],
                subcategory=act.get('subcategory'),
                description=act['desc'],
                base_cost=act['cost'],
                unit=act.get('unit', 'each'),
                has_subitems=False,
                order_index=idx
            )
            db.session.add(activity)

        print(f"   Created {len(roofing_activities)} roofing activities in subcategories")

        # ========================================
        # PAINTING - WITH SUBCATEGORIES
        # ========================================
        print("\n[5/6] Creating Painting with subcategories...")
        painting_cat = POSCategory(
            user_id=user.id,
            name="Painting",
            description="Interior and exterior painting",
            keywords="paint,primer,stain,finish",
            icon="🎨"
        )
        db.session.add(painting_cat)
        db.session.flush()

        painting_activities = [
            # INTERIOR PAINTING
            {'name': 'Interior Wall Painting', 'subcategory': 'Interior Painting', 'desc': '2 coats with primer', 'cost': Decimal('2.50'), 'unit': 'sqft'},
            {'name': 'Ceiling Painting', 'subcategory': 'Interior Painting', 'desc': 'Ceiling with primer', 'cost': Decimal('2'), 'unit': 'sqft'},
            {'name': 'Trim Painting', 'subcategory': 'Interior Painting', 'desc': 'Baseboards, doors, windows', 'cost': Decimal('3'), 'unit': 'linear_ft'},
            {'name': 'Cabinet Painting', 'subcategory': 'Interior Painting', 'desc': 'Kitchen cabinet refinish', 'cost': Decimal('80'), 'unit': 'linear_ft'},

            # EXTERIOR PAINTING
            {'name': 'Exterior Walls', 'subcategory': 'Exterior Painting', 'desc': 'Siding with primer', 'cost': Decimal('3.50'), 'unit': 'sqft'},
            {'name': 'Exterior Trim', 'subcategory': 'Exterior Painting', 'desc': 'Fascia, soffit, trim', 'cost': Decimal('4'), 'unit': 'linear_ft'},
            {'name': 'Deck Staining', 'subcategory': 'Exterior Painting', 'desc': 'Deck with stain/sealer', 'cost': Decimal('2.50'), 'unit': 'sqft'},

            # PREP WORK
            {'name': 'Drywall Repair', 'subcategory': 'Prep Work', 'desc': 'Patch holes and cracks', 'cost': Decimal('150'), 'unit': 'each'},
            {'name': 'Power Washing', 'subcategory': 'Prep Work', 'desc': 'Exterior surface cleaning', 'cost': Decimal('0.50'), 'unit': 'sqft'},
            {'name': 'Primer Application', 'subcategory': 'Prep Work', 'desc': 'Stain-blocking primer', 'cost': Decimal('1'), 'unit': 'sqft'},
        ]

        for idx, act in enumerate(painting_activities):
            activity = POSActivity(
                category_id=painting_cat.id,
                name=act['name'],
                subcategory=act.get('subcategory'),
                description=act['desc'],
                base_cost=act['cost'],
                unit=act.get('unit', 'each'),
                has_subitems=False,
                order_index=idx
            )
            db.session.add(activity)

        print(f"   Created {len(painting_activities)} painting activities in subcategories")

        # ========================================
        # DECKING - WITH SUBCATEGORIES
        # ========================================
        print("\n[6/6] Creating Decking with subcategories...")
        decking_cat = POSCategory(
            user_id=user.id,
            name="Decking & Outdoor",
            description="Deck and outdoor structures",
            keywords="deck,patio,pergola,fence",
            icon="🌳"
        )
        db.session.add(decking_cat)
        db.session.flush()

        decking_activities = [
            # DECK MATERIALS
            {'name': 'Pressure Treated Deck', 'subcategory': 'Deck Materials', 'desc': 'PT lumber decking', 'cost': Decimal('25'), 'unit': 'sqft'},
            {'name': 'Cedar Deck', 'subcategory': 'Deck Materials', 'desc': 'Natural cedar', 'cost': Decimal('35'), 'unit': 'sqft'},
            {'name': 'Composite Decking', 'subcategory': 'Deck Materials', 'desc': 'Low-maintenance composite', 'cost': Decimal('45'), 'unit': 'sqft'},
            {'name': 'PVC Decking', 'subcategory': 'Deck Materials', 'desc': 'Premium PVC boards', 'cost': Decimal('55'), 'unit': 'sqft'},

            # RAILINGS & STAIRS
            {'name': 'Wood Railing', 'subcategory': 'Railings & Stairs', 'desc': 'Traditional wood rail', 'cost': Decimal('80'), 'unit': 'linear_ft'},
            {'name': 'Composite Railing', 'subcategory': 'Railings & Stairs', 'desc': 'Composite rail system', 'cost': Decimal('120'), 'unit': 'linear_ft'},
            {'name': 'Deck Stairs', 'subcategory': 'Railings & Stairs', 'desc': '3-step deck stairs', 'cost': Decimal('400'), 'unit': 'each'},

            # STRUCTURES
            {'name': 'Pergola', 'subcategory': 'Structures', 'desc': '10x10 pergola', 'cost': Decimal('3500'), 'unit': 'each'},
            {'name': 'Privacy Fence', 'subcategory': 'Structures', 'desc': '6ft wood fence', 'cost': Decimal('30'), 'unit': 'linear_ft'},
        ]

        for idx, act in enumerate(decking_activities):
            activity = POSActivity(
                category_id=decking_cat.id,
                name=act['name'],
                subcategory=act.get('subcategory'),
                description=act['desc'],
                base_cost=act['cost'],
                unit=act.get('unit', 'each'),
                has_subitems=False,
                order_index=idx
            )
            db.session.add(activity)

        print(f"   Created {len(decking_activities)} decking activities in subcategories")

        # Commit all data
        db.session.commit()

        print("\n" + "="*60)
        print("POS DATA WITH SUBCATEGORIES - COMPLETE!")
        print("="*60)
        print(f"Categories: 6")
        print(f"Total Activities: {len(flooring_activities) + len(kitchen_activities) + len(bathroom_activities) + len(roofing_activities) + len(painting_activities) + len(decking_activities)}")
        print("\nSubcategory organization enables better UX!")
        print("="*60)

if __name__ == '__main__':
    seed_pos_with_subcategories()
