"""
Comprehensive POS Data Seeding Script
Adds extensive categories, activities, and subitems for all common construction projects
"""

from app import app
from models import db, User, POSCategory, POSActivity, POSSubItem
from decimal import Decimal

def seed_comprehensive_pos_data():
    """Seed the database with comprehensive POS data for construction projects"""
    with app.app_context():
        # Get the first user (admin)
        user = User.query.first()
        if not user:
            print("ERROR: No users found. Please create a user first.")
            return

        print(f"Seeding comprehensive POS data for user: {user.username}")

        # Check if data already exists and automatically delete
        existing_categories = POSCategory.query.filter_by(user_id=user.id).count()
        if existing_categories > 0:
            print(f"WARNING: Found {existing_categories} existing categories. Deleting and reseeding...")
            # Delete existing data
            POSCategory.query.filter_by(user_id=user.id).delete()
            db.session.commit()
            print("Existing POS data deleted.")

        # ========================================
        # KITCHEN RENOVATION - COMPREHENSIVE
        # ========================================
        print("\n[1/6] Creating Kitchen Renovation activities...")
        kitchen_cat = POSCategory(
            user_id=user.id,
            name="Kitchen Renovation",
            description="Complete kitchen remodeling services from demolition to finishing",
            keywords="kitchen,cooking,cabinets,countertops,appliances,sink,remodel",
            icon="🍳"
        )
        db.session.add(kitchen_cat)
        db.session.flush()

        kitchen_activities = [
            # Demolition
            {'name': 'Kitchen Demolition', 'desc': 'Remove existing cabinets, countertops, flooring', 'cost': Decimal('1500'), 'unit': 'room', 'subitems': False},
            {'name': 'Appliance Removal', 'desc': 'Disconnect and remove old appliances', 'cost': Decimal('200'), 'unit': 'each', 'subitems': False},
            {'name': 'Dumpster Rental', 'desc': '20-yard dumpster for debris removal', 'cost': Decimal('450'), 'unit': 'each', 'subitems': False},

            # Cabinets
            {'name': 'Upper Kitchen Cabinets', 'desc': 'Wall-mounted upper cabinets', 'cost': Decimal('3500'), 'unit': 'linear_ft', 'subitems': True,
             'options': [('Stock Laminate', Decimal('150')), ('Semi-Custom Wood', Decimal('250')), ('Custom Hardwood', Decimal('400')), ('Luxury Custom', Decimal('600'))]},
            {'name': 'Lower Kitchen Cabinets', 'desc': 'Base cabinets with drawers', 'cost': Decimal('4500'), 'unit': 'linear_ft', 'subitems': True,
             'options': [('Stock Laminate', Decimal('180')), ('Semi-Custom Wood', Decimal('300')), ('Custom Hardwood', Decimal('500')), ('Luxury Custom', Decimal('750'))]},
            {'name': 'Kitchen Island', 'desc': 'Custom kitchen island with storage', 'cost': Decimal('3000'), 'unit': 'each', 'subitems': True,
             'options': [('Basic Island (4ft)', Decimal('2000')), ('Standard Island (6ft)', Decimal('3000')), ('Large Island (8ft)', Decimal('4500')), ('Custom with Seating', Decimal('6000'))]},
            {'name': 'Pantry Cabinets', 'desc': 'Floor-to-ceiling pantry storage', 'cost': Decimal('1800'), 'unit': 'each', 'subitems': False},
            {'name': 'Cabinet Hardware', 'desc': 'Knobs and pulls for cabinets', 'cost': Decimal('8'), 'unit': 'each', 'subitems': True,
             'options': [('Basic Builder Grade', Decimal('3')), ('Brushed Nickel', Decimal('8')), ('Oil Rubbed Bronze', Decimal('12')), ('Designer Hardware', Decimal('25'))]},

            # Countertops
            {'name': 'Kitchen Countertops', 'desc': 'Countertop material and installation', 'cost': Decimal('65'), 'unit': 'sqft', 'subitems': True,
             'options': [('Laminate', Decimal('25')), ('Solid Surface', Decimal('50')), ('Granite', Decimal('65')), ('Quartz', Decimal('80')), ('Marble', Decimal('100')), ('Quartzite', Decimal('120'))]},
            {'name': 'Island Countertop', 'desc': 'Separate island countertop', 'cost': Decimal('70'), 'unit': 'sqft', 'subitems': False},
            {'name': 'Countertop Edge Profile', 'desc': 'Custom edge finishing', 'cost': Decimal('15'), 'unit': 'linear_ft', 'subitems': True,
             'options': [('Standard Eased', Decimal('0')), ('Beveled', Decimal('8')), ('Bullnose', Decimal('12')), ('Ogee', Decimal('20')), ('Waterfall', Decimal('35'))]},

            # Backsplash
            {'name': 'Tile Backsplash', 'desc': 'Ceramic or glass tile backsplash', 'cost': Decimal('18'), 'unit': 'sqft', 'subitems': True,
             'options': [('Ceramic 4x4', Decimal('12')), ('Subway Tile', Decimal('15')), ('Glass Mosaic', Decimal('25')), ('Natural Stone', Decimal('35')), ('Designer Tile', Decimal('50'))]},
            {'name': 'Backsplash to Ceiling', 'desc': 'Full-height backsplash installation', 'cost': Decimal('22'), 'unit': 'sqft', 'subitems': False},

            # Sinks & Faucets
            {'name': 'Kitchen Sink', 'desc': 'Undermount or drop-in sink installation', 'cost': Decimal('800'), 'unit': 'each', 'subitems': True,
             'options': [('Single Basin Stainless', Decimal('350')), ('Double Basin Stainless', Decimal('500')), ('Farmhouse Apron Sink', Decimal('900')), ('Granite Composite', Decimal('750')), ('Copper Sink', Decimal('1200'))]},
            {'name': 'Kitchen Faucet', 'desc': 'Pull-down or pull-out kitchen faucet', 'cost': Decimal('350'), 'unit': 'each', 'subitems': True,
             'options': [('Basic Chrome', Decimal('120')), ('Pull-Down Stainless', Decimal('250')), ('Touchless Faucet', Decimal('450')), ('Commercial Style', Decimal('600')), ('Luxury Designer', Decimal('1000'))]},
            {'name': 'Garbage Disposal', 'desc': 'In-sink garbage disposal unit', 'cost': Decimal('250'), 'unit': 'each', 'subitems': True,
             'options': [('1/3 HP Basic', Decimal('150')), ('1/2 HP Standard', Decimal('200')), ('3/4 HP Premium', Decimal('300')), ('1 HP Heavy Duty', Decimal('450'))]},
            {'name': 'Water Filtration System', 'desc': 'Under-sink water filter', 'cost': Decimal('600'), 'unit': 'each', 'subitems': True,
             'options': [('Basic Carbon Filter', Decimal('300')), ('Multi-Stage Filter', Decimal('600')), ('Reverse Osmosis', Decimal('1200')), ('Whole House System', Decimal('2500'))]},
            {'name': 'Instant Hot Water Dispenser', 'desc': 'Dedicated hot water tap', 'cost': Decimal('450'), 'unit': 'each', 'subitems': False},

            # Appliances
            {'name': 'Dishwasher Installation', 'desc': 'Built-in dishwasher with electrical/plumbing', 'cost': Decimal('800'), 'unit': 'each', 'subitems': True,
             'options': [('Standard Dishwasher', Decimal('500')), ('Quiet Model', Decimal('800')), ('Stainless Interior', Decimal('1000')), ('Luxury Smart Model', Decimal('1500'))]},
            {'name': 'Range/Oven Installation', 'desc': 'Freestanding or slide-in range', 'cost': Decimal('1200'), 'unit': 'each', 'subitems': True,
             'options': [('Basic Electric Range', Decimal('700')), ('Gas Range', Decimal('1000')), ('Dual Fuel Range', Decimal('2000')), ('Professional Style Range', Decimal('4000'))]},
            {'name': 'Built-in Oven Installation', 'desc': 'Wall-mounted oven installation', 'cost': Decimal('1500'), 'unit': 'each', 'subitems': False},
            {'name': 'Cooktop Installation', 'desc': 'Gas or electric cooktop', 'cost': Decimal('1000'), 'unit': 'each', 'subitems': True,
             'options': [('Electric Cooktop', Decimal('600')), ('Gas Cooktop', Decimal('900')), ('Induction Cooktop', Decimal('1500')), ('Professional Gas', Decimal('3000'))]},
            {'name': 'Range Hood/Ventilation', 'desc': 'Vented or recirculating range hood', 'cost': Decimal('800'), 'unit': 'each', 'subitems': True,
             'options': [('Under-Cabinet Hood', Decimal('400')), ('Wall Mount Hood', Decimal('800')), ('Island Hood', Decimal('1200')), ('Professional Hood', Decimal('2500'))]},
            {'name': 'Microwave Installation', 'desc': 'Over-range or built-in microwave', 'cost': Decimal('500'), 'unit': 'each', 'subitems': True,
             'options': [('Over-Range Microwave', Decimal('300')), ('Built-in Drawer', Decimal('1200')), ('Trim Kit Built-in', Decimal('800'))]},
            {'name': 'Refrigerator Installation', 'desc': 'Freestanding or built-in refrigerator', 'cost': Decimal('300'), 'unit': 'each', 'subitems': False},
            {'name': 'Wine Refrigerator', 'desc': 'Under-counter wine cooler', 'cost': Decimal('1500'), 'unit': 'each', 'subitems': False},
            {'name': 'Ice Maker Line', 'desc': 'Dedicated water line for ice maker', 'cost': Decimal('350'), 'unit': 'each', 'subitems': False},

            # Flooring
            {'name': 'Kitchen Flooring Removal', 'desc': 'Remove existing flooring material', 'cost': Decimal('3'), 'unit': 'sqft', 'subitems': False},
            {'name': 'Kitchen Flooring', 'desc': 'New kitchen floor installation', 'cost': Decimal('12'), 'unit': 'sqft', 'subitems': True,
             'options': [('Vinyl Plank', Decimal('6')), ('Ceramic Tile', Decimal('10')), ('Porcelain Tile', Decimal('12')), ('Hardwood', Decimal('15')), ('Natural Stone', Decimal('20'))]},
            {'name': 'Floor Underlayment', 'desc': 'Subfloor preparation and leveling', 'cost': Decimal('3'), 'unit': 'sqft', 'subitems': False},
            {'name': 'Floor Heating System', 'desc': 'Radiant floor heating', 'cost': Decimal('15'), 'unit': 'sqft', 'subitems': False},

            # Lighting
            {'name': 'Recessed Lighting', 'desc': 'Can lights for general illumination', 'cost': Decimal('200'), 'unit': 'each', 'subitems': True,
             'options': [('Standard 6" Can', Decimal('150')), ('LED Retrofit', Decimal('180')), ('Adjustable Gimbal', Decimal('220')), ('Smart Dimmable', Decimal('280'))]},
            {'name': 'Pendant Lighting', 'desc': 'Decorative pendant lights over island', 'cost': Decimal('350'), 'unit': 'each', 'subitems': True,
             'options': [('Basic Glass Pendant', Decimal('150')), ('Designer Pendant', Decimal('350')), ('Mini Chandelier', Decimal('600')), ('Luxury Fixture', Decimal('1200'))]},
            {'name': 'Under-Cabinet Lighting', 'desc': 'LED strip or puck lights', 'cost': Decimal('100'), 'unit': 'linear_ft', 'subitems': True,
             'options': [('LED Strip Lights', Decimal('35')), ('Puck Lights', Decimal('60')), ('Linear LED Bar', Decimal('100')), ('Smart Color-Changing', Decimal('150'))]},
            {'name': 'Toe Kick Lighting', 'desc': 'LED lighting in cabinet base', 'cost': Decimal('40'), 'unit': 'linear_ft', 'subitems': False},
            {'name': 'Light Switches & Dimmers', 'desc': 'Modern switch and dimmer installation', 'cost': Decimal('125'), 'unit': 'each', 'subitems': True,
             'options': [('Standard Switch', Decimal('50')), ('Dimmer Switch', Decimal('100')), ('Smart Switch', Decimal('150')), ('Touchscreen Panel', Decimal('300'))]},

            # Electrical
            {'name': 'Kitchen Electrical Outlets', 'desc': 'GFCI outlets and USB ports', 'cost': Decimal('150'), 'unit': 'each', 'subitems': True,
             'options': [('Standard GFCI', Decimal('75')), ('USB Combo Outlet', Decimal('120')), ('USB-C Fast Charge', Decimal('180')), ('Pop-up Counter Outlet', Decimal('300'))]},
            {'name': 'Electrical Circuit Addition', 'desc': 'New dedicated circuit for appliances', 'cost': Decimal('450'), 'unit': 'each', 'subitems': False},
            {'name': 'Electrical Panel Upgrade', 'desc': 'Upgrade service panel capacity', 'cost': Decimal('2500'), 'unit': 'each', 'subitems': False},
            {'name': 'Kitchen Wiring Upgrade', 'desc': 'Rewire kitchen to code', 'cost': Decimal('3500'), 'unit': 'room', 'subitems': False},

            # Plumbing
            {'name': 'Kitchen Plumbing Rough-in', 'desc': 'New water and drain lines', 'cost': Decimal('1800'), 'unit': 'room', 'subitems': False},
            {'name': 'Gas Line Installation', 'desc': 'Gas line for range/cooktop', 'cost': Decimal('750'), 'unit': 'each', 'subitems': False},
            {'name': 'Pot Filler Faucet', 'desc': 'Wall-mounted pot filler over stove', 'cost': Decimal('600'), 'unit': 'each', 'subitems': False},

            # Walls & Ceiling
            {'name': 'Drywall Repair', 'desc': 'Patch and repair drywall damage', 'cost': Decimal('350'), 'unit': 'room', 'subitems': False},
            {'name': 'New Drywall Installation', 'desc': 'Full room drywall replacement', 'cost': Decimal('4'), 'unit': 'sqft', 'subitems': False},
            {'name': 'Kitchen Painting', 'desc': 'Walls and ceiling painting', 'cost': Decimal('2.50'), 'unit': 'sqft', 'subitems': True,
             'options': [('Standard Paint 1 Coat', Decimal('1.80')), ('Premium Paint 2 Coats', Decimal('2.50')), ('Designer Colors', Decimal('3.20'))]},
            {'name': 'Crown Molding', 'desc': 'Decorative ceiling trim', 'cost': Decimal('8'), 'unit': 'linear_ft', 'subitems': True,
             'options': [('Simple Profile', Decimal('6')), ('Traditional Profile', Decimal('8')), ('Elaborate Profile', Decimal('12'))]},
            {'name': 'Baseboards & Trim', 'desc': 'Floor trim and door casing', 'cost': Decimal('6'), 'unit': 'linear_ft', 'subitems': False},

            # Windows & Doors
            {'name': 'Kitchen Window Replacement', 'desc': 'Energy-efficient window installation', 'cost': Decimal('800'), 'unit': 'each', 'subitems': True,
             'options': [('Standard Vinyl', Decimal('500')), ('Energy Star Vinyl', Decimal('800')), ('Wood Clad', Decimal('1200')), ('Custom Wood', Decimal('2000'))]},
            {'name': 'Kitchen Door Installation', 'desc': 'Interior or exterior door', 'cost': Decimal('600'), 'unit': 'each', 'subitems': False},
            {'name': 'Patio/French Door', 'desc': 'Sliding or swinging patio door', 'cost': Decimal('2500'), 'unit': 'each', 'subitems': True,
             'options': [('Standard Vinyl Slider', Decimal('1500')), ('Energy Star Slider', Decimal('2500')), ('French Doors', Decimal('3500')), ('Folding Glass Wall', Decimal('8000'))]},
        ]

        for idx, act in enumerate(kitchen_activities, 1):
            activity = POSActivity(
                category_id=kitchen_cat.id,
                name=act['name'],
                description=act['desc'],
                base_cost=act['cost'],
                unit=act['unit'],
                has_subitems=act.get('subitems', False),
                order_index=idx
            )
            db.session.add(activity)
            db.session.flush()

            # Add subitems if specified
            if 'options' in act:
                question = POSSubItem(
                    activity_id=activity.id,
                    name=f"{act['name']} Options",
                    question_text=f"Select {act['name'].lower()} type",
                    option_type='choice',
                    is_required=True)
                db.session.add(question)
                db.session.flush()

                for opt_idx, (opt_name, opt_cost) in enumerate(act['options'], 1):
                    option = POSSubItem(
                        activity_id=activity.id,
                        parent_id=question.id,
                        name=opt_name,
                        cost_modifier=opt_cost,
                        order_index=opt_idx
                    )
                    db.session.add(option)

        print(f"   Created {len(kitchen_activities)} kitchen activities")

        # ========================================
        # BATHROOM RENOVATION - COMPREHENSIVE
        # ========================================
        print("\n[2/6] Creating Bathroom Renovation activities...")
        bathroom_cat = POSCategory(
            user_id=user.id,
            name="Bathroom Renovation",
            description="Full bathroom remodeling from demo to finishing touches",
            keywords="bathroom,shower,tub,toilet,vanity,tile,bath,remodel",
            icon="🚿"
        )
        db.session.add(bathroom_cat)
        db.session.flush()

        bathroom_activities = [
            # Demolition
            {'name': 'Bathroom Demolition', 'desc': 'Remove existing fixtures, tile, flooring', 'cost': Decimal('1200'), 'unit': 'room', 'subitems': False},
            {'name': 'Fixture Removal', 'desc': 'Disconnect and remove old fixtures', 'cost': Decimal('150'), 'unit': 'each', 'subitems': False},

            # Shower & Tub
            {'name': 'Shower Pan Installation', 'desc': 'Custom tile-ready shower base', 'cost': Decimal('800'), 'unit': 'each', 'subitems': True,
             'options': [('Fiberglass Pan', Decimal('400')), ('Acrylic Pan', Decimal('600')), ('Tile-Ready Pan', Decimal('800')), ('Custom Concrete Pan', Decimal('1500'))]},
            {'name': 'Shower Surround/Tile', 'desc': 'Shower wall material and installation', 'cost': Decimal('2500'), 'unit': 'each', 'subitems': True,
             'options': [('Fiberglass Insert', Decimal('800')), ('Acrylic Panels', Decimal('1500')), ('Ceramic Tile', Decimal('2500')), ('Porcelain Tile', Decimal('3200')), ('Natural Stone', Decimal('4500')), ('Luxury Slab', Decimal('7000'))]},
            {'name': 'Shower Door Installation', 'desc': 'Glass shower enclosure', 'cost': Decimal('1200'), 'unit': 'each', 'subitems': True,
             'options': [('Framed Clear Glass', Decimal('700')), ('Semi-Frameless', Decimal('1200')), ('Frameless Clear', Decimal('1800')), ('Frameless Custom', Decimal('3000'))]},
            {'name': 'Shower Valve System', 'desc': 'Thermostatic shower control', 'cost': Decimal('600'), 'unit': 'each', 'subitems': True,
             'options': [('Single Handle Valve', Decimal('350')), ('Thermostatic Valve', Decimal('600')), ('Digital Control', Decimal('1500')), ('Smart Shower System', Decimal('2500'))]},
            {'name': 'Shower Head & Trim', 'desc': 'Fixed or handheld shower head', 'cost': Decimal('350'), 'unit': 'each', 'subitems': True,
             'options': [('Standard Fixed Head', Decimal('100')), ('Rain Shower Head', Decimal('250')), ('Handheld Combo', Decimal('350')), ('Multi-Function System', Decimal('800')), ('Luxury Rain Panel', Decimal('2000'))]},
            {'name': 'Tub/Shower Combo', 'desc': 'Combined bathtub with shower', 'cost': Decimal('2000'), 'unit': 'each', 'subitems': True,
             'options': [('Fiberglass Unit', Decimal('1200')), ('Acrylic Unit', Decimal('2000')), ('Tile Surround', Decimal('3500'))]},
            {'name': 'Bathtub Installation', 'desc': 'Freestanding or alcove tub', 'cost': Decimal('1800'), 'unit': 'each', 'subitems': True,
             'options': [('Standard Alcove Tub', Decimal('800')), ('Soaking Tub', Decimal('1800')), ('Freestanding Tub', Decimal('3000')), ('Jetted Tub', Decimal('4500')), ('Air Bath', Decimal('5500'))]},
            {'name': 'Tub Faucet & Trim', 'desc': 'Bathtub filler and controls', 'cost': Decimal('500'), 'unit': 'each', 'subitems': True,
             'options': [('Standard Tub Faucet', Decimal('300')), ('Deck Mount Faucet', Decimal('500')), ('Floor Mount Filler', Decimal('1200')), ('Wall Mount Designer', Decimal('1800'))]},
            {'name': 'Roman Tub Deck', 'desc': 'Custom surround for drop-in tub', 'cost': Decimal('1500'), 'unit': 'each', 'subitems': False},
            {'name': 'Shower Bench/Seat', 'desc': 'Built-in shower seating', 'cost': Decimal('600'), 'unit': 'each', 'subitems': True,
             'options': [('Tile Bench', Decimal('400')), ('Stone Bench', Decimal('600')), ('Teak Wood Bench', Decimal('900'))]},
            {'name': 'Shower Niche', 'desc': 'Recessed shower storage', 'cost': Decimal('350'), 'unit': 'each', 'subitems': False},

            # Vanity & Sink
            {'name': 'Bathroom Vanity', 'desc': 'Single or double vanity cabinet', 'cost': Decimal('1500'), 'unit': 'each', 'subitems': True,
             'options': [('24" Stock Vanity', Decimal('500')), ('36" Stock Vanity', Decimal('800')), ('48" Semi-Custom', Decimal('1500')), ('60" Double Vanity', Decimal('2500')), ('72" Custom Double', Decimal('4000'))]},
            {'name': 'Vanity Countertop', 'desc': 'Vanity top material and installation', 'cost': Decimal('400'), 'unit': 'each', 'subitems': True,
             'options': [('Cultured Marble', Decimal('300')), ('Solid Surface', Decimal('400')), ('Granite', Decimal('600')), ('Quartz', Decimal('750')), ('Marble', Decimal('900'))]},
            {'name': 'Bathroom Sink', 'desc': 'Undermount, vessel, or drop-in sink', 'cost': Decimal('350'), 'unit': 'each', 'subitems': True,
             'options': [('Undermount Porcelain', Decimal('150')), ('Vessel Sink', Decimal('350')), ('Rectangular Undermount', Decimal('300')), ('Designer Vessel', Decimal('800'))]},
            {'name': 'Bathroom Faucet', 'desc': 'Vanity faucet installation', 'cost': Decimal('250'), 'unit': 'each', 'subitems': True,
             'options': [('Basic Chrome', Decimal('120')), ('Brushed Nickel', Decimal('200')), ('Widespread Faucet', Decimal('300')), ('Wall Mount Faucet', Decimal('450')), ('Designer Faucet', Decimal('800'))]},
            {'name': 'Floating Vanity Installation', 'desc': 'Wall-mounted vanity', 'cost': Decimal('2200'), 'unit': 'each', 'subitems': False},

            # Toilet & Bidet
            {'name': 'Toilet Installation', 'desc': 'Standard or comfort-height toilet', 'cost': Decimal('500'), 'unit': 'each', 'subitems': True,
             'options': [('Standard 2-Piece', Decimal('250')), ('Comfort Height', Decimal('400')), ('One-Piece Elongated', Decimal('500')), ('Dual Flush', Decimal('650')), ('Smart Toilet', Decimal('2500'))]},
            {'name': 'Bidet Installation', 'desc': 'Standalone bidet or toilet seat', 'cost': Decimal('800'), 'unit': 'each', 'subitems': True,
             'options': [('Bidet Attachment', Decimal('200')), ('Electric Bidet Seat', Decimal('800')), ('Standalone Bidet', Decimal('1200')), ('Luxury Bidet Toilet', Decimal('3500'))]},
            {'name': 'Toilet Paper Holder', 'desc': 'Wall-mounted toilet paper holder', 'cost': Decimal('60'), 'unit': 'each', 'subitems': False},

            # Flooring
            {'name': 'Bathroom Flooring Removal', 'desc': 'Remove existing floor and underlayment', 'cost': Decimal('4'), 'unit': 'sqft', 'subitems': False},
            {'name': 'Bathroom Flooring', 'desc': 'Waterproof floor installation', 'cost': Decimal('15'), 'unit': 'sqft', 'subitems': True,
             'options': [('Vinyl Sheet', Decimal('6')), ('Luxury Vinyl Plank', Decimal('8')), ('Ceramic Tile', Decimal('12')), ('Porcelain Tile', Decimal('15')), ('Natural Stone', Decimal('25')), ('Heated Tile Floor', Decimal('35'))]},
            {'name': 'Floor Underlayment', 'desc': 'Cement board or waterproof membrane', 'cost': Decimal('4'), 'unit': 'sqft', 'subitems': False},
            {'name': 'Floor Heating System', 'desc': 'Electric radiant floor heating', 'cost': Decimal('18'), 'unit': 'sqft', 'subitems': False},

            # Wall Tile
            {'name': 'Bathroom Wall Tile', 'desc': 'Decorative or accent wall tile', 'cost': Decimal('18'), 'unit': 'sqft', 'subitems': True,
             'options': [('Ceramic 4x4', Decimal('12')), ('Subway Tile', Decimal('15')), ('Large Format Tile', Decimal('20')), ('Glass Mosaic', Decimal('30')), ('Natural Stone', Decimal('35'))]},
            {'name': 'Wainscoting/Beadboard', 'desc': 'Decorative wall paneling', 'cost': Decimal('12'), 'unit': 'sqft', 'subitems': False},

            # Lighting & Ventilation
            {'name': 'Vanity Lighting', 'desc': 'Above or beside mirror lighting', 'cost': Decimal('300'), 'unit': 'each', 'subitems': True,
             'options': [('Basic Bar Light', Decimal('150')), ('Modern Sconces', Decimal('300')), ('Designer Fixture', Decimal('600')), ('LED Smart Lighting', Decimal('900'))]},
            {'name': 'Recessed Shower Light', 'desc': 'Waterproof recessed lighting', 'cost': Decimal('180'), 'unit': 'each', 'subitems': False},
            {'name': 'Bathroom Ventilation Fan', 'desc': 'Exhaust fan with or without light/heat', 'cost': Decimal('350'), 'unit': 'each', 'subitems': True,
             'options': [('Basic Fan Only', Decimal('200')), ('Fan/Light Combo', Decimal('300')), ('Ultra-Quiet Fan', Decimal('400')), ('Fan/Light/Heater', Decimal('550')), ('Smart Fan with Sensor', Decimal('700'))]},

            # Mirrors & Accessories
            {'name': 'Bathroom Mirror', 'desc': 'Frameless or framed mirror', 'cost': Decimal('250'), 'unit': 'each', 'subitems': True,
             'options': [('Basic Frameless', Decimal('150')), ('Framed Mirror', Decimal('250')), ('LED Lighted Mirror', Decimal('600')), ('Smart Mirror', Decimal('1500'))]},
            {'name': 'Medicine Cabinet', 'desc': 'Recessed or surface mount storage', 'cost': Decimal('350'), 'unit': 'each', 'subitems': True,
             'options': [('Surface Mount Basic', Decimal('150')), ('Recessed Cabinet', Decimal('300')), ('Lighted Medicine Cabinet', Decimal('500')), ('Tri-View Cabinet', Decimal('800'))]},
            {'name': 'Towel Bars & Accessories', 'desc': 'Towel bars, rings, and hooks', 'cost': Decimal('200'), 'unit': 'set', 'subitems': True,
             'options': [('Basic Chrome Set', Decimal('100')), ('Brushed Nickel Set', Decimal('200')), ('Designer Set', Decimal('400'))]},
            {'name': 'Shower Shelving/Caddy', 'desc': 'Corner shelf or built-in storage', 'cost': Decimal('150'), 'unit': 'each', 'subitems': False},
            {'name': 'Towel Warmer', 'desc': 'Electric or hydronic towel warmer', 'cost': Decimal('600'), 'unit': 'each', 'subitems': False},

            # Doors & Windows
            {'name': 'Bathroom Door Replacement', 'desc': 'Interior door with hardware', 'cost': Decimal('500'), 'unit': 'each', 'subitems': True,
             'options': [('Hollow Core', Decimal('300')), ('Solid Core', Decimal('500')), ('Pocket Door', Decimal('800')), ('Barn Door', Decimal('1200'))]},
            {'name': 'Bathroom Window', 'desc': 'Privacy window installation', 'cost': Decimal('700'), 'unit': 'each', 'subitems': True,
             'options': [('Standard Vinyl', Decimal('500')), ('Frosted Glass', Decimal('700')), ('Glass Block', Decimal('1200'))]},

            # Plumbing & Electrical
            {'name': 'Bathroom Plumbing Rough-in', 'desc': 'New water supply and drain lines', 'cost': Decimal('2200'), 'unit': 'room', 'subitems': False},
            {'name': 'Bathroom Electrical Wiring', 'desc': 'New circuits and outlets', 'cost': Decimal('1500'), 'unit': 'room', 'subitems': False},
            {'name': 'GFCI Outlet Installation', 'desc': 'Code-required GFCI outlets', 'cost': Decimal('125'), 'unit': 'each', 'subitems': False},

            # Finishing
            {'name': 'Bathroom Painting', 'desc': 'Moisture-resistant paint', 'cost': Decimal('3'), 'unit': 'sqft', 'subitems': False},
            {'name': 'Drywall & Greenboard', 'desc': 'Moisture-resistant drywall', 'cost': Decimal('5'), 'unit': 'sqft', 'subitems': False},
            {'name': 'Crown Molding', 'desc': 'Decorative ceiling trim', 'cost': Decimal('7'), 'unit': 'linear_ft', 'subitems': False},
            {'name': 'Baseboards & Trim', 'desc': 'Waterproof base molding', 'cost': Decimal('5'), 'unit': 'linear_ft', 'subitems': False},
        ]

        for idx, act in enumerate(bathroom_activities, 1):
            activity = POSActivity(
                category_id=bathroom_cat.id,
                name=act['name'],
                description=act['desc'],
                base_cost=act['cost'],
                unit=act['unit'],
                has_subitems=act.get('subitems', False),
                order_index=idx
            )
            db.session.add(activity)
            db.session.flush()

            if 'options' in act:
                question = POSSubItem(
                    activity_id=activity.id,
                    name=f"{act['name']} Options",
                    question_text=f"Select {act['name'].lower()} type",
                    option_type='choice',
                    is_required=True)
                db.session.add(question)
                db.session.flush()

                for opt_idx, (opt_name, opt_cost) in enumerate(act['options'], 1):
                    option = POSSubItem(
                        activity_id=activity.id,
                        parent_id=question.id,
                        name=opt_name,
                        cost_modifier=opt_cost,
                        order_index=opt_idx
                    )
                    db.session.add(option)

        print(f"   Created {len(bathroom_activities)} bathroom activities")

        # ========================================
        # ROOFING - COMPREHENSIVE
        # ========================================
        print("\n[3/6] Creating Roofing activities...")
        roofing_cat = POSCategory(
            user_id=user.id,
            name="Roofing",
            description="Complete roofing services from inspection to installation",
            keywords="roof,roofing,shingles,metal,tile,leak,repair,replacement",
            icon="🏠")
        db.session.add(roofing_cat)
        db.session.flush()

        roofing_activities = [
            # Inspection & Prep
            {'name': 'Roof Inspection', 'desc': 'Professional roof condition assessment', 'cost': Decimal('350'), 'unit': 'each', 'subitems': False},
            {'name': 'Roof Tear-off', 'desc': 'Remove existing roofing materials', 'cost': Decimal('150'), 'unit': 'square', 'subitems': True,
             'options': [('1 Layer Removal', Decimal('120')), ('2 Layers Removal', Decimal('180')), ('3 Layers Removal', Decimal('250'))]},
            {'name': 'Dumpster for Roofing', 'desc': 'Debris removal and disposal', 'cost': Decimal('550'), 'unit': 'each', 'subitems': False},

            # Decking & Underlayment
            {'name': 'Roof Decking Replacement', 'desc': 'Replace damaged plywood/OSB', 'cost': Decimal('85'), 'unit': 'sheet', 'subitems': True,
             'options': [('OSB Sheathing', Decimal('70')), ('Plywood Sheathing', Decimal('85')), ('Tongue & Groove', Decimal('120'))]},
            {'name': 'Roof Underlayment', 'desc': 'Synthetic or felt underlayment', 'cost': Decimal('0.75'), 'unit': 'sqft', 'subitems': True,
             'options': [('30lb Felt Paper', Decimal('0.50')), ('Synthetic Underlayment', Decimal('0.75')), ('Premium Synthetic', Decimal('1.20'))]},
            {'name': 'Ice & Water Shield', 'desc': 'Waterproof membrane for valleys/eaves', 'cost': Decimal('1.50'), 'unit': 'sqft', 'subitems': False},
            {'name': 'Roof Edge Drip Edge', 'desc': 'Metal drip edge installation', 'cost': Decimal('3'), 'unit': 'linear_ft', 'subitems': False},

            # Roofing Materials
            {'name': 'Asphalt Shingle Roof', 'desc': '3-tab or architectural shingles', 'cost': Decimal('450'), 'unit': 'square', 'subitems': True,
             'options': [('3-Tab 20yr Shingles', Decimal('350')), ('Architectural 30yr', Decimal('450')), ('Designer 50yr', Decimal('650')), ('Premium Luxury', Decimal('900'))]},
            {'name': 'Metal Roof Installation', 'desc': 'Standing seam or corrugated metal', 'cost': Decimal('900'), 'unit': 'square', 'subitems': True,
             'options': [('Corrugated Steel', Decimal('600')), ('Standing Seam Steel', Decimal('900')), ('Aluminum', Decimal('1200')), ('Copper', Decimal('2500'))]},
            {'name': 'Tile Roof Installation', 'desc': 'Clay or concrete tile roofing', 'cost': Decimal('1200'), 'unit': 'square', 'subitems': True,
             'options': [('Concrete Tile', Decimal('900')), ('Clay Tile', Decimal('1200')), ('Spanish Tile', Decimal('1500'))]},
            {'name': 'Slate Roof Installation', 'desc': 'Natural slate roofing', 'cost': Decimal('2000'), 'unit': 'square', 'subitems': False},
            {'name': 'Flat Roof System', 'desc': 'TPO, EPDM, or modified bitumen', 'cost': Decimal('650'), 'unit': 'square', 'subitems': True,
             'options': [('EPDM Rubber', Decimal('550')), ('TPO White', Decimal('650')), ('Modified Bitumen', Decimal('700')), ('PVC Membrane', Decimal('850'))]},
            {'name': 'Roof Coating', 'desc': 'Reflective roof coating application', 'cost': Decimal('150'), 'unit': 'square', 'subitems': False},

            # Flashing & Valleys
            {'name': 'Chimney Flashing', 'desc': 'Step and counter flashing around chimney', 'cost': Decimal('600'), 'unit': 'each', 'subitems': False},
            {'name': 'Skylight Flashing', 'desc': 'Waterproof skylight integration', 'cost': Decimal('400'), 'unit': 'each', 'subitems': False},
            {'name': 'Valley Flashing', 'desc': 'Metal valley installation', 'cost': Decimal('15'), 'unit': 'linear_ft', 'subitems': True,
             'options': [('Open Valley', Decimal('12')), ('Woven Valley', Decimal('10')), ('Metal Valley', Decimal('15'))]},
            {'name': 'Pipe Boot Flashing', 'desc': 'Vent pipe waterproofing', 'cost': Decimal('65'), 'unit': 'each', 'subitems': False},
            {'name': 'Chimney Cricket', 'desc': 'Diverter behind chimney', 'cost': Decimal('800'), 'unit': 'each', 'subitems': False},

            # Ventilation
            {'name': 'Ridge Vent Installation', 'desc': 'Continuous ridge ventilation', 'cost': Decimal('8'), 'unit': 'linear_ft', 'subitems': False},
            {'name': 'Roof Vents', 'desc': 'Box or turbine vents', 'cost': Decimal('150'), 'unit': 'each', 'subitems': True,
             'options': [('Box Vent', Decimal('120')), ('Turbine Vent', Decimal('180')), ('Power Attic Fan', Decimal('450'))]},
            {'name': 'Soffit Vents', 'desc': 'Intake ventilation at eaves', 'cost': Decimal('5'), 'unit': 'linear_ft', 'subitems': False},
            {'name': 'Gable Vent', 'desc': 'End wall ventilation', 'cost': Decimal('250'), 'unit': 'each', 'subitems': False},

            # Skylights
            {'name': 'Skylight Installation', 'desc': 'Fixed or venting skylight', 'cost': Decimal('1200'), 'unit': 'each', 'subitems': True,
             'options': [('Fixed Skylight', Decimal('800')), ('Venting Skylight', Decimal('1200')), ('Solar Powered', Decimal('1800')), ('Tubular Skylight', Decimal('600'))]},

            # Gutters & Drainage
            {'name': 'Gutter Installation', 'desc': 'Seamless aluminum gutters', 'cost': Decimal('12'), 'unit': 'linear_ft', 'subitems': True,
             'options': [('Aluminum K-Style', Decimal('10')), ('Seamless Aluminum', Decimal('12')), ('Copper Gutters', Decimal('30')), ('Half-Round', Decimal('15'))]},
            {'name': 'Gutter Guards', 'desc': 'Leaf protection system', 'cost': Decimal('8'), 'unit': 'linear_ft', 'subitems': True,
             'options': [('Screen Guards', Decimal('5')), ('Micro-Mesh Guards', Decimal('8')), ('Premium System', Decimal('15'))]},
            {'name': 'Downspout Installation', 'desc': 'Vertical drainage pipes', 'cost': Decimal('10'), 'unit': 'linear_ft', 'subitems': False},
            {'name': 'Downspout Extensions', 'desc': 'Ground-level drainage', 'cost': Decimal('75'), 'unit': 'each', 'subitems': False},
            {'name': 'Underground Drainage', 'desc': 'Buried downspout drainage', 'cost': Decimal('25'), 'unit': 'linear_ft', 'subitems': False},

            # Fascia & Soffit
            {'name': 'Fascia Board Replacement', 'desc': 'Replace rotted fascia boards', 'cost': Decimal('12'), 'unit': 'linear_ft', 'subitems': True,
             'options': [('Wood Fascia', Decimal('10')), ('Composite Fascia', Decimal('12')), ('Aluminum Wrap', Decimal('8'))]},
            {'name': 'Soffit Replacement', 'desc': 'Vented or solid soffit panels', 'cost': Decimal('10'), 'unit': 'linear_ft', 'subitems': True,
             'options': [('Vinyl Soffit', Decimal('8')), ('Aluminum Soffit', Decimal('10')), ('Wood Soffit', Decimal('15'))]},

            # Repairs
            {'name': 'Roof Leak Repair', 'desc': 'Emergency leak repair', 'cost': Decimal('500'), 'unit': 'each', 'subitems': False},
            {'name': 'Shingle Replacement', 'desc': 'Replace damaged shingles', 'cost': Decimal('300'), 'unit': 'patch', 'subitems': False},
            {'name': 'Emergency Tarp Service', 'desc': 'Temporary weather protection', 'cost': Decimal('400'), 'unit': 'each', 'subitems': False},
        ]

        for idx, act in enumerate(roofing_activities, 1):
            activity = POSActivity(
                category_id=roofing_cat.id,
                name=act['name'],
                description=act['desc'],
                base_cost=act['cost'],
                unit=act['unit'],
                has_subitems=act.get('subitems', False),
                order_index=idx
            )
            db.session.add(activity)
            db.session.flush()

            if 'options' in act:
                question = POSSubItem(
                    activity_id=activity.id,
                    name=f"{act['name']} Options",
                    question_text=f"Select {act['name'].lower()} type",
                    option_type='choice',
                    is_required=True)
                db.session.add(question)
                db.session.flush()

                for opt_idx, (opt_name, opt_cost) in enumerate(act['options'], 1):
                    option = POSSubItem(
                        activity_id=activity.id,
                        parent_id=question.id,
                        name=opt_name,
                        cost_modifier=opt_cost,
                        order_index=opt_idx
                    )
                    db.session.add(option)

        print(f"   Created {len(roofing_activities)} roofing activities")

        # ========================================
        # FLOORING - COMPREHENSIVE
        # ========================================
        print("\n[4/6] Creating Flooring activities...")
        flooring_cat = POSCategory(
            user_id=user.id,
            name="Flooring",
            description="Complete flooring installation for all room types",
            keywords="floor,flooring,hardwood,tile,vinyl,carpet,laminate,bamboo",
            icon="🪵")
        db.session.add(flooring_cat)
        db.session.flush()

        flooring_activities = [
            # Removal & Prep
            {'name': 'Floor Removal', 'desc': 'Remove existing flooring material', 'cost': Decimal('3'), 'unit': 'sqft', 'subitems': True,
             'options': [('Carpet Removal', Decimal('1.50')), ('Vinyl Removal', Decimal('2')), ('Tile Removal', Decimal('4')), ('Hardwood Removal', Decimal('3'))]},
            {'name': 'Subfloor Repair', 'desc': 'Replace damaged subfloor sections', 'cost': Decimal('8'), 'unit': 'sqft', 'subitems': False},
            {'name': 'Floor Leveling', 'desc': 'Self-leveling compound application', 'cost': Decimal('4'), 'unit': 'sqft', 'subitems': False},

            # Hardwood
            {'name': 'Solid Hardwood Flooring', 'desc': '3/4" solid hardwood installation', 'cost': Decimal('15'), 'unit': 'sqft', 'subitems': True,
             'options': [('Oak 3/4"', Decimal('12')), ('Maple 3/4"', Decimal('14')), ('Cherry', Decimal('18')), ('Walnut', Decimal('22')), ('Exotic Species', Decimal('30'))]},
            {'name': 'Engineered Hardwood', 'desc': 'Engineered wood planks', 'cost': Decimal('12'), 'unit': 'sqft', 'subitems': True,
             'options': [('Basic Engineered', Decimal('8')), ('Premium Engineered', Decimal('12')), ('Wide Plank Engineered', Decimal('16'))]},
            {'name': 'Hardwood Refinishing', 'desc': 'Sand and refinish existing hardwood', 'cost': Decimal('5'), 'unit': 'sqft', 'subitems': True,
             'options': [('Standard Sanding & Poly', Decimal('4')), ('Premium Finish', Decimal('5')), ('Hand-Scraped Refinish', Decimal('7'))]},

            # Tile
            {'name': 'Ceramic Tile Flooring', 'desc': 'Ceramic floor tile installation', 'cost': Decimal('10'), 'unit': 'sqft', 'subitems': True,
             'options': [('12x12 Ceramic', Decimal('8')), ('18x18 Ceramic', Decimal('10')), ('Mosaic Pattern', Decimal('15'))]},
            {'name': 'Porcelain Tile Flooring', 'desc': 'Porcelain floor tile installation', 'cost': Decimal('14'), 'unit': 'sqft', 'subitems': True,
             'options': [('12x24 Porcelain', Decimal('12')), ('24x24 Large Format', Decimal('14')), ('Wood-Look Plank Tile', Decimal('16')), ('Rectified Edge', Decimal('18'))]},
            {'name': 'Natural Stone Flooring', 'desc': 'Marble, granite, or travertine', 'cost': Decimal('25'), 'unit': 'sqft', 'subitems': True,
             'options': [('Travertine', Decimal('18')), ('Slate', Decimal('20')), ('Marble', Decimal('25')), ('Granite', Decimal('28'))]},
            {'name': 'Tile Backerboard', 'desc': 'Cement board underlayment', 'cost': Decimal('3'), 'unit': 'sqft', 'subitems': False},
            {'name': 'Tile Waterproofing', 'desc': 'Waterproof membrane for wet areas', 'cost': Decimal('2.50'), 'unit': 'sqft', 'subitems': False},

            # Vinyl & Resilient
            {'name': 'Luxury Vinyl Plank (LVP)', 'desc': 'Click-lock or glue-down LVP', 'cost': Decimal('7'), 'unit': 'sqft', 'subitems': True,
             'options': [('Basic LVP', Decimal('5')), ('Premium LVP', Decimal('7')), ('Waterproof Core LVP', Decimal('9')), ('Commercial Grade LVP', Decimal('12'))]},
            {'name': 'Sheet Vinyl', 'desc': 'Continuous sheet vinyl flooring', 'cost': Decimal('5'), 'unit': 'sqft', 'subitems': False},
            {'name': 'Vinyl Tile (VCT)', 'desc': 'Vinyl composition tile', 'cost': Decimal('4'), 'unit': 'sqft', 'subitems': False},

            # Laminate
            {'name': 'Laminate Flooring', 'desc': 'Click-lock laminate planks', 'cost': Decimal('6'), 'unit': 'sqft', 'subitems': True,
             'options': [('AC3 Residential', Decimal('4')), ('AC4 Premium', Decimal('6')), ('AC5 Commercial', Decimal('8'))]},

            # Carpet
            {'name': 'Carpet Installation', 'desc': 'Wall-to-wall carpeting with pad', 'cost': Decimal('6'), 'unit': 'sqft', 'subitems': True,
             'options': [('Builder Grade', Decimal('3')), ('Mid-Grade Plush', Decimal('5')), ('Premium Frieze', Decimal('7')), ('Luxury Wool', Decimal('15'))]},
            {'name': 'Carpet Padding', 'desc': 'Quality carpet underlayment', 'cost': Decimal('1.50'), 'unit': 'sqft', 'subitems': True,
             'options': [('Standard 6lb Pad', Decimal('0.80')), ('Premium 8lb Pad', Decimal('1.50')), ('Memory Foam Pad', Decimal('2.50'))]},
            {'name': 'Carpet Removal & Disposal', 'desc': 'Remove and haul away old carpet', 'cost': Decimal('1.50'), 'unit': 'sqft', 'subitems': False},

            # Specialty
            {'name': 'Cork Flooring', 'desc': 'Eco-friendly cork tiles or planks', 'cost': Decimal('10'), 'unit': 'sqft', 'subitems': False},
            {'name': 'Bamboo Flooring', 'desc': 'Sustainable bamboo installation', 'cost': Decimal('9'), 'unit': 'sqft', 'subitems': True,
             'options': [('Horizontal Grain', Decimal('8')), ('Vertical Grain', Decimal('9')), ('Strand Woven', Decimal('12'))]},
            {'name': 'Rubber Flooring', 'desc': 'Commercial or gym rubber flooring', 'cost': Decimal('8'), 'unit': 'sqft', 'subitems': False},

            # Transitions & Finishing
            {'name': 'Floor Transitions', 'desc': 'Threshold and transition strips', 'cost': Decimal('35'), 'unit': 'each', 'subitems': True,
             'options': [('Basic T-Molding', Decimal('25')), ('Reducer Strip', Decimal('30')), ('Threshold', Decimal('35')), ('Stair Nose', Decimal('45'))]},
            {'name': 'Baseboards Installation', 'desc': 'Baseboard trim after flooring', 'cost': Decimal('5'), 'unit': 'linear_ft', 'subitems': False},
            {'name': 'Quarter Round/Shoe Molding', 'desc': 'Floor edge trim', 'cost': Decimal('3'), 'unit': 'linear_ft', 'subitems': False},
        ]

        for idx, act in enumerate(flooring_activities, 1):
            activity = POSActivity(
                category_id=flooring_cat.id,
                name=act['name'],
                description=act['desc'],
                base_cost=act['cost'],
                unit=act['unit'],
                has_subitems=act.get('subitems', False),
                order_index=idx
            )
            db.session.add(activity)
            db.session.flush()

            if 'options' in act:
                question = POSSubItem(
                    activity_id=activity.id,
                    name=f"{act['name']} Options",
                    question_text=f"Select {act['name'].lower()} type",
                    option_type='choice',
                    is_required=True)
                db.session.add(question)
                db.session.flush()

                for opt_idx, (opt_name, opt_cost) in enumerate(act['options'], 1):
                    option = POSSubItem(
                        activity_id=activity.id,
                        parent_id=question.id,
                        name=opt_name,
                        cost_modifier=opt_cost,
                        order_index=opt_idx
                    )
                    db.session.add(option)

        print(f"   Created {len(flooring_activities)} flooring activities")

        # ========================================
        # PAINTING - COMPREHENSIVE
        # ========================================
        print("\n[5/6] Creating Painting activities...")
        painting_cat = POSCategory(
            user_id=user.id,
            name="Painting",
            description="Interior and exterior painting services",
            keywords="paint,painting,interior,exterior,walls,ceiling,trim,cabinet",
            icon="🎨")
        db.session.add(painting_cat)
        db.session.flush()

        painting_activities = [
            # Prep Work
            {'name': 'Surface Preparation', 'desc': 'Sanding, patching, and priming', 'cost': Decimal('1.50'), 'unit': 'sqft', 'subitems': False},
            {'name': 'Wallpaper Removal', 'desc': 'Remove and prep walls after wallpaper', 'cost': Decimal('2'), 'unit': 'sqft', 'subitems': False},
            {'name': 'Texture Removal', 'desc': 'Remove popcorn or orange peel texture', 'cost': Decimal('2.50'), 'unit': 'sqft', 'subitems': False},
            {'name': 'Drywall Repair', 'desc': 'Patch holes and cracks', 'cost': Decimal('150'), 'unit': 'room', 'subitems': False},

            # Interior Painting
            {'name': 'Interior Wall Painting', 'desc': 'Paint walls with premium paint', 'cost': Decimal('2.50'), 'unit': 'sqft', 'subitems': True,
             'options': [('1 Coat Builder Grade', Decimal('1.50')), ('2 Coats Standard', Decimal('2.50')), ('2 Coats Premium', Decimal('3.20')), ('Designer Colors', Decimal('3.80'))]},
            {'name': 'Ceiling Painting', 'desc': 'Ceiling paint application', 'cost': Decimal('2'), 'unit': 'sqft', 'subitems': True,
             'options': [('Flat White 1 Coat', Decimal('1.50')), ('Flat White 2 Coats', Decimal('2')), ('Textured Ceiling', Decimal('2.50'))]},
            {'name': 'Accent Wall', 'desc': 'Feature wall with designer color', 'cost': Decimal('3.50'), 'unit': 'sqft', 'subitems': False},
            {'name': 'Two-Tone Walls', 'desc': 'Dual color with chair rail', 'cost': Decimal('3.80'), 'unit': 'sqft', 'subitems': False},

            # Trim & Doors
            {'name': 'Trim & Baseboard Painting', 'desc': 'Paint all trim and baseboards', 'cost': Decimal('3'), 'unit': 'linear_ft', 'subitems': True,
             'options': [('1 Coat', Decimal('2')), ('2 Coats Semi-Gloss', Decimal('3')), ('Premium Finish', Decimal('4'))]},
            {'name': 'Door Painting', 'desc': 'Paint interior doors (both sides)', 'cost': Decimal('85'), 'unit': 'each', 'subitems': True,
             'options': [('Hollow Core 1 Coat', Decimal('60')), ('Solid Core 2 Coats', Decimal('85')), ('6-Panel Detailed', Decimal('120'))]},
            {'name': 'Crown Molding Painting', 'desc': 'Detailed crown molding finish', 'cost': Decimal('4'), 'unit': 'linear_ft', 'subitems': False},
            {'name': 'Window Trim Painting', 'desc': 'Paint window casings and sills', 'cost': Decimal('50'), 'unit': 'each', 'subitems': False},

            # Cabinets
            {'name': 'Cabinet Painting/Refinishing', 'desc': 'Professional cabinet refinishing', 'cost': Decimal('150'), 'unit': 'linear_ft', 'subitems': True,
             'options': [('Standard Paint', Decimal('100')), ('Premium Paint', Decimal('150')), ('Lacquer Finish', Decimal('200')), ('Spray Finish', Decimal('250'))]},
            {'name': 'Cabinet Hardware Installation', 'desc': 'Install new knobs and pulls', 'cost': Decimal('8'), 'unit': 'each', 'subitems': False},

            # Exterior Painting
            {'name': 'Exterior House Painting', 'desc': 'Full exterior house painting', 'cost': Decimal('3.50'), 'unit': 'sqft', 'subitems': True,
             'options': [('1 Coat Standard', Decimal('2.50')), ('2 Coats Premium', Decimal('3.50')), ('Elastomeric Coating', Decimal('4.50'))]},
            {'name': 'Exterior Trim Painting', 'desc': 'Windows, doors, fascia, soffit', 'cost': Decimal('4'), 'unit': 'linear_ft', 'subitems': False},
            {'name': 'Deck/Fence Staining', 'desc': 'Stain and seal wood surfaces', 'cost': Decimal('2.50'), 'unit': 'sqft', 'subitems': True,
             'options': [('Semi-Transparent Stain', Decimal('2')), ('Solid Stain', Decimal('2.50')), ('Premium Sealant', Decimal('3'))]},
            {'name': 'Garage Door Painting', 'desc': 'Paint garage door exterior', 'cost': Decimal('250'), 'unit': 'each', 'subitems': False},
            {'name': 'Shutters Painting', 'desc': 'Paint or stain shutters', 'cost': Decimal('40'), 'unit': 'each', 'subitems': False},
            {'name': 'Power Washing', 'desc': 'Pressure wash before painting', 'cost': Decimal('0.50'), 'unit': 'sqft', 'subitems': False},

            # Specialty
            {'name': 'Staircase Painting', 'desc': 'Paint stairs, risers, balusters', 'cost': Decimal('500'), 'unit': 'staircase', 'subitems': False},
            {'name': 'Textured Finish Application', 'desc': 'Venetian plaster or faux finish', 'cost': Decimal('8'), 'unit': 'sqft', 'subitems': False},
            {'name': 'Mural/Custom Artwork', 'desc': 'Hand-painted custom design', 'cost': Decimal('150'), 'unit': 'hour', 'subitems': False},
        ]

        for idx, act in enumerate(painting_activities, 1):
            activity = POSActivity(
                category_id=painting_cat.id,
                name=act['name'],
                description=act['desc'],
                base_cost=act['cost'],
                unit=act['unit'],
                has_subitems=act.get('subitems', False),
                order_index=idx
            )
            db.session.add(activity)
            db.session.flush()

            if 'options' in act:
                question = POSSubItem(
                    activity_id=activity.id,
                    name=f"{act['name']} Options",
                    question_text=f"Select {act['name'].lower()} type",
                    option_type='choice',
                    is_required=True)
                db.session.add(question)
                db.session.flush()

                for opt_idx, (opt_name, opt_cost) in enumerate(act['options'], 1):
                    option = POSSubItem(
                        activity_id=activity.id,
                        parent_id=question.id,
                        name=opt_name,
                        cost_modifier=opt_cost,
                        order_index=opt_idx
                    )
                    db.session.add(option)

        print(f"   Created {len(painting_activities)} painting activities")

        # ========================================
        # DECKING & OUTDOOR - COMPREHENSIVE
        # ========================================
        print("\n[6/6] Creating Decking & Outdoor activities...")
        deck_cat = POSCategory(
            user_id=user.id,
            name="Decking & Outdoor",
            description="Decks, patios, pergolas, and outdoor living spaces",
            keywords="deck,patio,pergola,outdoor,gazebo,porch,railing",
            icon="🏡")
        db.session.add(deck_cat)
        db.session.flush()

        deck_activities = [
            # Deck Construction
            {'name': 'Pressure-Treated Deck', 'desc': 'PT lumber deck construction', 'cost': Decimal('35'), 'unit': 'sqft', 'subitems': True,
             'options': [('Basic Ground-Level', Decimal('25')), ('Elevated Deck', Decimal('35')), ('Multi-Level Deck', Decimal('50'))]},
            {'name': 'Composite Decking', 'desc': 'Low-maintenance composite boards', 'cost': Decimal('45'), 'unit': 'sqft', 'subitems': True,
             'options': [('Standard Composite', Decimal('40')), ('Premium Composite', Decimal('45')), ('Luxury Capped Composite', Decimal('55'))]},
            {'name': 'Cedar/Redwood Deck', 'desc': 'Natural wood decking', 'cost': Decimal('50'), 'unit': 'sqft', 'subitems': True,
             'options': [('Cedar', Decimal('45')), ('Redwood', Decimal('55')), ('Ipe Hardwood', Decimal('75'))]},
            {'name': 'Deck Railing', 'desc': 'Safety railing installation', 'cost': Decimal('75'), 'unit': 'linear_ft', 'subitems': True,
             'options': [('Wood Balusters', Decimal('60')), ('Composite Railing', Decimal('75')), ('Cable Railing', Decimal('100')), ('Glass Panel Railing', Decimal('150'))]},
            {'name': 'Deck Stairs', 'desc': 'Exterior stairs with railing', 'cost': Decimal('150'), 'unit': 'step', 'subitems': False},
            {'name': 'Deck Lighting', 'desc': 'Low-voltage deck lighting', 'cost': Decimal('45'), 'unit': 'each', 'subitems': True,
             'options': [('Basic Post Cap Lights', Decimal('30')), ('Recessed Step Lights', Decimal('45')), ('Smart Color Changing', Decimal('80'))]},
            {'name': 'Built-in Deck Benches', 'desc': 'Integrated seating', 'cost': Decimal('100'), 'unit': 'linear_ft', 'subitems': False},
            {'name': 'Deck Removal/Demo', 'desc': 'Remove existing deck structure', 'cost': Decimal('8'), 'unit': 'sqft', 'subitems': False},

            # Patio
            {'name': 'Concrete Patio', 'desc': 'Poured concrete patio slab', 'cost': Decimal('12'), 'unit': 'sqft', 'subitems': True,
             'options': [('Basic Brushed Finish', Decimal('10')), ('Stamped Concrete', Decimal('15')), ('Stained Concrete', Decimal('14')), ('Decorative Overlay', Decimal('18'))]},
            {'name': 'Paver Patio', 'desc': 'Interlocking paver installation', 'cost': Decimal('18'), 'unit': 'sqft', 'subitems': True,
             'options': [('Concrete Pavers', Decimal('15')), ('Brick Pavers', Decimal('18')), ('Natural Stone Pavers', Decimal('28')), ('Flagstone', Decimal('30'))]},
            {'name': 'Patio Excavation', 'desc': 'Site prep and base materials', 'cost': Decimal('5'), 'unit': 'sqft', 'subitems': False},
            {'name': 'Gravel Base & Compaction', 'desc': 'Crushed stone base preparation', 'cost': Decimal('3'), 'unit': 'sqft', 'subitems': False},
            {'name': 'Paver Sealing', 'desc': 'Protective sealer application', 'cost': Decimal('2'), 'unit': 'sqft', 'subitems': False},

            # Pergolas & Structures
            {'name': 'Pergola Installation', 'desc': 'Freestanding or attached pergola', 'cost': Decimal('3500'), 'unit': 'each', 'subitems': True,
             'options': [('10x10 Basic Wood', Decimal('2500')), ('12x12 Cedar', Decimal('3500')), ('16x16 Premium', Decimal('6000')), ('Custom Large', Decimal('10000'))]},
            {'name': 'Gazebo Installation', 'desc': 'Octagonal or square gazebo', 'cost': Decimal('5000'), 'unit': 'each', 'subitems': False},
            {'name': 'Covered Porch', 'desc': 'Roofed porch addition', 'cost': Decimal('75'), 'unit': 'sqft', 'subitems': False},
            {'name': 'Screen Room Enclosure', 'desc': 'Screened porch conversion', 'cost': Decimal('35'), 'unit': 'sqft', 'subitems': False},

            # Outdoor Features
            {'name': 'Outdoor Kitchen Frame', 'desc': 'Built-in BBQ island structure', 'cost': Decimal('8000'), 'unit': 'each', 'subitems': False},
            {'name': 'Fire Pit Installation', 'desc': 'Stone or metal fire pit', 'cost': Decimal('2500'), 'unit': 'each', 'subitems': True,
             'options': [('Pre-Fab Fire Ring', Decimal('800')), ('Stone Fire Pit', Decimal('2500')), ('Gas Fire Table', Decimal('3500'))]},
            {'name': 'Retaining Wall', 'desc': 'Structural landscape wall', 'cost': Decimal('35'), 'unit': 'sqft', 'subitems': True,
             'options': [('Timber Wall', Decimal('25')), ('Block Wall', Decimal('35')), ('Natural Stone Wall', Decimal('50'))]},
            {'name': 'Outdoor Shower', 'desc': 'Exterior shower installation', 'cost': Decimal('1500'), 'unit': 'each', 'subitems': False},
        ]

        for idx, act in enumerate(deck_activities, 1):
            activity = POSActivity(
                category_id=deck_cat.id,
                name=act['name'],
                description=act['desc'],
                base_cost=act['cost'],
                unit=act['unit'],
                has_subitems=act.get('subitems', False),
                order_index=idx
            )
            db.session.add(activity)
            db.session.flush()

            if 'options' in act:
                question = POSSubItem(
                    activity_id=activity.id,
                    name=f"{act['name']} Options",
                    question_text=f"Select {act['name'].lower()} type",
                    option_type='choice',
                    is_required=True)
                db.session.add(question)
                db.session.flush()

                for opt_idx, (opt_name, opt_cost) in enumerate(act['options'], 1):
                    option = POSSubItem(
                        activity_id=activity.id,
                        parent_id=question.id,
                        name=opt_name,
                        cost_modifier=opt_cost,
                        order_index=opt_idx
                    )
                    db.session.add(option)

        print(f"   Created {len(deck_activities)} deck & outdoor activities")

        # Commit all data
        db.session.commit()

        # Print summary
        total_categories = POSCategory.query.filter_by(user_id=user.id).count()
        total_activities = POSActivity.query.join(POSCategory).filter(POSCategory.user_id == user.id).count()
        total_subitems = POSSubItem.query.join(POSActivity).join(POSCategory).filter(POSCategory.user_id == user.id).count()

        print("\n" + "="*60)
        print("COMPREHENSIVE POS DATA SEEDING COMPLETE!")
        print("="*60)
        print(f"Categories created: {total_categories}")
        print(f"Activities created: {total_activities}")
        print(f"Sub-options created: {total_subitems}")
        print(f"\nAccess the POS system at: http://localhost:5000/pos")
        print("="*60)

if __name__ == '__main__':
    seed_comprehensive_pos_data()
