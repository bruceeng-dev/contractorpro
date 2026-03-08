"""
Granular POS Categories - More Specific, Distilled Categories
Instead of "Kitchen Renovation" we have "Cabinets", "Countertops", etc.
"""

import sys
import codecs
# Set stdout to UTF-8 encoding
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
else:
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

from app import app
from models import db, User, POSCategory, POSActivity
from decimal import Decimal

def seed_granular_pos_categories():
    """Seed with specific, granular categories"""
    with app.app_context():
        user = User.query.first()
        if not user:
            print("ERROR: No users found.")
            return

        print(f"Seeding granular POS categories for user: {user.username}")

        # Delete existing data
        existing = POSCategory.query.filter_by(user_id=user.id).count()
        if existing > 0:
            print(f"Deleting {existing} existing categories...")
            POSCategory.query.filter_by(user_id=user.id).delete()
            db.session.commit()

        categories_data = [
            # ========== CABINETS & MILLWORK ==========
            {
                'name': 'Cabinets & Millwork',
                'icon': '🗄️',
                'desc': 'Kitchen, bathroom, and custom cabinetry',
                'keywords': 'cabinets,vanity,millwork,custom',
                'activities': [
                    {'name': 'Kitchen Upper Cabinets', 'subcategory': 'Kitchen Cabinets', 'cost': Decimal('200'), 'unit': 'linear_ft'},
                    {'name': 'Kitchen Lower Cabinets', 'subcategory': 'Kitchen Cabinets', 'cost': Decimal('250'), 'unit': 'linear_ft'},
                    {'name': 'Kitchen Island Cabinet', 'subcategory': 'Kitchen Cabinets', 'cost': Decimal('3000'), 'unit': 'each'},
                    {'name': 'Pantry Cabinet', 'subcategory': 'Kitchen Cabinets', 'cost': Decimal('1800'), 'unit': 'each'},
                    {'name': 'Cabinet Hardware Install', 'subcategory': 'Kitchen Cabinets', 'cost': Decimal('8'), 'unit': 'each'},

                    {'name': 'Bathroom Vanity 24"', 'subcategory': 'Bathroom Cabinets', 'cost': Decimal('600'), 'unit': 'each'},
                    {'name': 'Bathroom Vanity 48"', 'subcategory': 'Bathroom Cabinets', 'cost': Decimal('1200'), 'unit': 'each'},
                    {'name': 'Bathroom Vanity 60" Double', 'subcategory': 'Bathroom Cabinets', 'cost': Decimal('1800'), 'unit': 'each'},
                    {'name': 'Medicine Cabinet', 'subcategory': 'Bathroom Cabinets', 'cost': Decimal('250'), 'unit': 'each'},
                    {'name': 'Linen Cabinet', 'subcategory': 'Bathroom Cabinets', 'cost': Decimal('800'), 'unit': 'each'},

                    {'name': 'Crown Molding', 'subcategory': 'Trim & Molding', 'cost': Decimal('12'), 'unit': 'linear_ft'},
                    {'name': 'Baseboard Trim', 'subcategory': 'Trim & Molding', 'cost': Decimal('8'), 'unit': 'linear_ft'},
                    {'name': 'Chair Rail', 'subcategory': 'Trim & Molding', 'cost': Decimal('10'), 'unit': 'linear_ft'},
                    {'name': 'Coffered Ceiling', 'subcategory': 'Trim & Molding', 'cost': Decimal('35'), 'unit': 'sqft'},
                ]
            },

            # ========== COUNTERTOPS ==========
            {
                'name': 'Countertops',
                'icon': '⬜',
                'desc': 'Kitchen and bathroom countertop materials',
                'keywords': 'countertop,granite,quartz,marble,laminate',
                'activities': [
                    {'name': 'Laminate Countertops', 'subcategory': 'Budget Options', 'cost': Decimal('25'), 'unit': 'sqft'},
                    {'name': 'Solid Surface (Corian)', 'subcategory': 'Budget Options', 'cost': Decimal('50'), 'unit': 'sqft'},

                    {'name': 'Granite Countertops', 'subcategory': 'Natural Stone', 'cost': Decimal('65'), 'unit': 'sqft'},
                    {'name': 'Marble Countertops', 'subcategory': 'Natural Stone', 'cost': Decimal('100'), 'unit': 'sqft'},
                    {'name': 'Quartzite Countertops', 'subcategory': 'Natural Stone', 'cost': Decimal('120'), 'unit': 'sqft'},
                    {'name': 'Soapstone Countertops', 'subcategory': 'Natural Stone', 'cost': Decimal('90'), 'unit': 'sqft'},

                    {'name': 'Quartz Countertops', 'subcategory': 'Engineered Stone', 'cost': Decimal('80'), 'unit': 'sqft'},
                    {'name': 'Porcelain Countertops', 'subcategory': 'Engineered Stone', 'cost': Decimal('75'), 'unit': 'sqft'},

                    {'name': 'Butcher Block Countertop', 'subcategory': 'Specialty', 'cost': Decimal('60'), 'unit': 'sqft'},
                    {'name': 'Concrete Countertops', 'subcategory': 'Specialty', 'cost': Decimal('95'), 'unit': 'sqft'},

                    {'name': 'Edge Profile Upgrade', 'subcategory': 'Finishing', 'cost': Decimal('15'), 'unit': 'linear_ft'},
                    {'name': 'Undermount Sink Cutout', 'subcategory': 'Finishing', 'cost': Decimal('150'), 'unit': 'each'},
                    {'name': 'Cooktop Cutout', 'subcategory': 'Finishing', 'cost': Decimal('200'), 'unit': 'each'},
                ]
            },

            # ========== FLOORING - TILE ==========
            {
                'name': 'Flooring - Tile',
                'icon': '🔲',
                'desc': 'Ceramic, porcelain, and natural stone tiles',
                'keywords': 'tile,ceramic,porcelain,stone,mosaic',
                'activities': [
                    {'name': 'Ceramic Tile 12x12', 'subcategory': 'Ceramic Tile', 'cost': Decimal('10'), 'unit': 'sqft'},
                    {'name': 'Ceramic Tile 18x18', 'subcategory': 'Ceramic Tile', 'cost': Decimal('12'), 'unit': 'sqft'},
                    {'name': 'Ceramic Subway Tile', 'subcategory': 'Ceramic Tile', 'cost': Decimal('14'), 'unit': 'sqft'},

                    {'name': 'Porcelain Tile 12x24', 'subcategory': 'Porcelain Tile', 'cost': Decimal('15'), 'unit': 'sqft'},
                    {'name': 'Porcelain Tile 24x24', 'subcategory': 'Porcelain Tile', 'cost': Decimal('16'), 'unit': 'sqft'},
                    {'name': 'Porcelain Wood-Look Plank', 'subcategory': 'Porcelain Tile', 'cost': Decimal('18'), 'unit': 'sqft'},

                    {'name': 'Marble Tile', 'subcategory': 'Natural Stone', 'cost': Decimal('25'), 'unit': 'sqft'},
                    {'name': 'Travertine Tile', 'subcategory': 'Natural Stone', 'cost': Decimal('22'), 'unit': 'sqft'},
                    {'name': 'Slate Tile', 'subcategory': 'Natural Stone', 'cost': Decimal('20'), 'unit': 'sqft'},
                    {'name': 'Limestone Tile', 'subcategory': 'Natural Stone', 'cost': Decimal('23'), 'unit': 'sqft'},

                    {'name': 'Glass Mosaic Tile', 'subcategory': 'Specialty Tile', 'cost': Decimal('28'), 'unit': 'sqft'},
                    {'name': 'Penny Round Tile', 'subcategory': 'Specialty Tile', 'cost': Decimal('26'), 'unit': 'sqft'},
                    {'name': 'Hexagon Tile', 'subcategory': 'Specialty Tile', 'cost': Decimal('24'), 'unit': 'sqft'},
                ]
            },

            # ========== FLOORING - WOOD ==========
            {
                'name': 'Flooring - Wood',
                'icon': '🪵',
                'desc': 'Hardwood, engineered, and laminate flooring',
                'keywords': 'wood,hardwood,engineered,laminate,lvp',
                'activities': [
                    {'name': 'Oak Solid Hardwood 3/4"', 'subcategory': 'Solid Hardwood', 'cost': Decimal('18'), 'unit': 'sqft'},
                    {'name': 'Maple Solid Hardwood 3/4"', 'subcategory': 'Solid Hardwood', 'cost': Decimal('20'), 'unit': 'sqft'},
                    {'name': 'Walnut Solid Hardwood 3/4"', 'subcategory': 'Solid Hardwood', 'cost': Decimal('28'), 'unit': 'sqft'},
                    {'name': 'Cherry Solid Hardwood 3/4"', 'subcategory': 'Solid Hardwood', 'cost': Decimal('24'), 'unit': 'sqft'},

                    {'name': 'Engineered Hardwood 5"', 'subcategory': 'Engineered Wood', 'cost': Decimal('14'), 'unit': 'sqft'},
                    {'name': 'Engineered Hardwood 7"', 'subcategory': 'Engineered Wood', 'cost': Decimal('16'), 'unit': 'sqft'},
                    {'name': 'Wide Plank Engineered 9"+', 'subcategory': 'Engineered Wood', 'cost': Decimal('20'), 'unit': 'sqft'},

                    {'name': 'Laminate Flooring AC3', 'subcategory': 'Laminate', 'cost': Decimal('6'), 'unit': 'sqft'},
                    {'name': 'Laminate Flooring AC4', 'subcategory': 'Laminate', 'cost': Decimal('8'), 'unit': 'sqft'},
                    {'name': 'Premium Laminate AC5', 'subcategory': 'Laminate', 'cost': Decimal('10'), 'unit': 'sqft'},

                    {'name': 'Luxury Vinyl Plank (LVP)', 'subcategory': 'Vinyl', 'cost': Decimal('8'), 'unit': 'sqft'},
                    {'name': 'Rigid Core LVP', 'subcategory': 'Vinyl', 'cost': Decimal('10'), 'unit': 'sqft'},
                    {'name': 'WPC Waterproof Flooring', 'subcategory': 'Vinyl', 'cost': Decimal('12'), 'unit': 'sqft'},
                ]
            },

            # ========== FLOORING - SOFT ==========
            {
                'name': 'Flooring - Carpet & Vinyl',
                'icon': '🧶',
                'desc': 'Carpet, padding, and sheet vinyl',
                'keywords': 'carpet,padding,vinyl,sheet',
                'activities': [
                    {'name': 'Builder Grade Carpet', 'subcategory': 'Carpet', 'cost': Decimal('5'), 'unit': 'sqft'},
                    {'name': 'Mid-Grade Plush Carpet', 'subcategory': 'Carpet', 'cost': Decimal('8'), 'unit': 'sqft'},
                    {'name': 'Premium Frieze Carpet', 'subcategory': 'Carpet', 'cost': Decimal('12'), 'unit': 'sqft'},
                    {'name': 'Berber Carpet', 'subcategory': 'Carpet', 'cost': Decimal('10'), 'unit': 'sqft'},
                    {'name': 'Carpet Tiles', 'subcategory': 'Carpet', 'cost': Decimal('7'), 'unit': 'sqft'},

                    {'name': '6lb Carpet Padding', 'subcategory': 'Padding', 'cost': Decimal('1.50'), 'unit': 'sqft'},
                    {'name': '8lb Carpet Padding', 'subcategory': 'Padding', 'cost': Decimal('2'), 'unit': 'sqft'},
                    {'name': 'Memory Foam Padding', 'subcategory': 'Padding', 'cost': Decimal('3'), 'unit': 'sqft'},

                    {'name': 'Sheet Vinyl Budget', 'subcategory': 'Sheet Vinyl', 'cost': Decimal('4'), 'unit': 'sqft'},
                    {'name': 'Sheet Vinyl Mid-Grade', 'subcategory': 'Sheet Vinyl', 'cost': Decimal('6'), 'unit': 'sqft'},
                    {'name': 'Commercial Sheet Vinyl', 'subcategory': 'Sheet Vinyl', 'cost': Decimal('8'), 'unit': 'sqft'},
                ]
            },

            # ========== PLUMBING FIXTURES ==========
            {
                'name': 'Plumbing Fixtures',
                'icon': '🚰',
                'desc': 'Sinks, faucets, toilets, and showers',
                'keywords': 'plumbing,sink,faucet,toilet,shower,tub',
                'activities': [
                    {'name': 'Stainless Undermount Sink', 'subcategory': 'Kitchen Sinks', 'cost': Decimal('500'), 'unit': 'each'},
                    {'name': 'Farmhouse Apron Sink', 'subcategory': 'Kitchen Sinks', 'cost': Decimal('900'), 'unit': 'each'},
                    {'name': 'Granite Composite Sink', 'subcategory': 'Kitchen Sinks', 'cost': Decimal('750'), 'unit': 'each'},

                    {'name': 'Kitchen Faucet Standard', 'subcategory': 'Kitchen Faucets', 'cost': Decimal('250'), 'unit': 'each'},
                    {'name': 'Kitchen Faucet Pull-Down', 'subcategory': 'Kitchen Faucets', 'cost': Decimal('350'), 'unit': 'each'},
                    {'name': 'Kitchen Faucet Touchless', 'subcategory': 'Kitchen Faucets', 'cost': Decimal('500'), 'unit': 'each'},
                    {'name': 'Kitchen Faucet Commercial', 'subcategory': 'Kitchen Faucets', 'cost': Decimal('650'), 'unit': 'each'},

                    {'name': 'Standard Toilet', 'subcategory': 'Toilets', 'cost': Decimal('350'), 'unit': 'each'},
                    {'name': 'Comfort Height Toilet', 'subcategory': 'Toilets', 'cost': Decimal('450'), 'unit': 'each'},
                    {'name': 'Wall-Hung Toilet', 'subcategory': 'Toilets', 'cost': Decimal('800'), 'unit': 'each'},
                    {'name': 'Smart Toilet/Bidet', 'subcategory': 'Toilets', 'cost': Decimal('1500'), 'unit': 'each'},

                    {'name': 'Vanity Faucet Standard', 'subcategory': 'Bathroom Faucets', 'cost': Decimal('150'), 'unit': 'each'},
                    {'name': 'Vanity Faucet Waterfall', 'subcategory': 'Bathroom Faucets', 'cost': Decimal('250'), 'unit': 'each'},
                    {'name': 'Tub Filler Freestanding', 'subcategory': 'Bathroom Faucets', 'cost': Decimal('600'), 'unit': 'each'},

                    {'name': 'Shower Pan Installation', 'subcategory': 'Shower & Tub', 'cost': Decimal('800'), 'unit': 'each'},
                    {'name': 'Standard Bathtub', 'subcategory': 'Shower & Tub', 'cost': Decimal('800'), 'unit': 'each'},
                    {'name': 'Soaking Tub', 'subcategory': 'Shower & Tub', 'cost': Decimal('1500'), 'unit': 'each'},
                    {'name': 'Shower Valve/Trim', 'subcategory': 'Shower & Tub', 'cost': Decimal('400'), 'unit': 'each'},
                    {'name': 'Rain Shower Head', 'subcategory': 'Shower & Tub', 'cost': Decimal('300'), 'unit': 'each'},
                    {'name': 'Frameless Glass Shower Door', 'subcategory': 'Shower & Tub', 'cost': Decimal('1500'), 'unit': 'each'},
                ]
            },

            # ========== APPLIANCES ==========
            {
                'name': 'Appliances',
                'icon': '🔌',
                'desc': 'Kitchen appliance installation',
                'keywords': 'appliance,dishwasher,range,oven,microwave,refrigerator',
                'activities': [
                    {'name': 'Dishwasher Install - Standard', 'subcategory': 'Dishwashers', 'cost': Decimal('300'), 'unit': 'each'},
                    {'name': 'Dishwasher Install - Panel Ready', 'subcategory': 'Dishwashers', 'cost': Decimal('400'), 'unit': 'each'},

                    {'name': 'Electric Range Install', 'subcategory': 'Ranges & Ovens', 'cost': Decimal('250'), 'unit': 'each'},
                    {'name': 'Gas Range Install', 'subcategory': 'Ranges & Ovens', 'cost': Decimal('400'), 'unit': 'each'},
                    {'name': 'Dual Fuel Range Install', 'subcategory': 'Ranges & Ovens', 'cost': Decimal('500'), 'unit': 'each'},
                    {'name': 'Wall Oven Install', 'subcategory': 'Ranges & Ovens', 'cost': Decimal('450'), 'unit': 'each'},
                    {'name': 'Cooktop Install - Electric', 'subcategory': 'Ranges & Ovens', 'cost': Decimal('350'), 'unit': 'each'},
                    {'name': 'Cooktop Install - Gas', 'subcategory': 'Ranges & Ovens', 'cost': Decimal('500'), 'unit': 'each'},

                    {'name': 'Range Hood - Under Cabinet', 'subcategory': 'Ventilation', 'cost': Decimal('400'), 'unit': 'each'},
                    {'name': 'Range Hood - Wall Mount', 'subcategory': 'Ventilation', 'cost': Decimal('800'), 'unit': 'each'},
                    {'name': 'Range Hood - Island', 'subcategory': 'Ventilation', 'cost': Decimal('1200'), 'unit': 'each'},

                    {'name': 'Microwave - Over Range', 'subcategory': 'Microwaves', 'cost': Decimal('250'), 'unit': 'each'},
                    {'name': 'Microwave - Built-In', 'subcategory': 'Microwaves', 'cost': Decimal('400'), 'unit': 'each'},

                    {'name': 'Refrigerator Install', 'subcategory': 'Other', 'cost': Decimal('200'), 'unit': 'each'},
                    {'name': 'Garbage Disposal Install', 'subcategory': 'Other', 'cost': Decimal('250'), 'unit': 'each'},
                ]
            },

            # ========== ROOFING ==========
            {
                'name': 'Roofing',
                'icon': '🏠',
                'desc': 'Roof installation and materials',
                'keywords': 'roof,shingles,metal,underlayment',
                'activities': [
                    {'name': '3-Tab Asphalt Shingles', 'subcategory': 'Asphalt Shingles', 'cost': Decimal('3.50'), 'unit': 'sqft'},
                    {'name': 'Architectural Shingles', 'subcategory': 'Asphalt Shingles', 'cost': Decimal('4.50'), 'unit': 'sqft'},
                    {'name': 'Designer Shingles', 'subcategory': 'Asphalt Shingles', 'cost': Decimal('6'), 'unit': 'sqft'},
                    {'name': 'Impact Resistant Shingles', 'subcategory': 'Asphalt Shingles', 'cost': Decimal('5.50'), 'unit': 'sqft'},

                    {'name': 'Standing Seam Metal', 'subcategory': 'Metal Roofing', 'cost': Decimal('12'), 'unit': 'sqft'},
                    {'name': 'Corrugated Metal', 'subcategory': 'Metal Roofing', 'cost': Decimal('8'), 'unit': 'sqft'},
                    {'name': 'Metal Shingles', 'subcategory': 'Metal Roofing', 'cost': Decimal('10'), 'unit': 'sqft'},

                    {'name': 'Ridge Vent', 'subcategory': 'Accessories', 'cost': Decimal('8'), 'unit': 'linear_ft'},
                    {'name': 'Aluminum Gutters', 'subcategory': 'Accessories', 'cost': Decimal('10'), 'unit': 'linear_ft'},
                    {'name': 'Gutter Guards', 'subcategory': 'Accessories', 'cost': Decimal('6'), 'unit': 'linear_ft'},
                    {'name': 'Ice & Water Shield', 'subcategory': 'Accessories', 'cost': Decimal('2'), 'unit': 'sqft'},
                    {'name': 'Roof Tear Off', 'subcategory': 'Demolition', 'cost': Decimal('1.50'), 'unit': 'sqft'},
                ]
            },

            # ========== PAINTING - INTERIOR ==========
            {
                'name': 'Painting - Interior',
                'icon': '🎨',
                'desc': 'Interior painting and finishing',
                'keywords': 'paint,interior,walls,ceiling,trim',
                'activities': [
                    {'name': 'Interior Walls (2 coats)', 'subcategory': 'Walls', 'cost': Decimal('2.50'), 'unit': 'sqft'},
                    {'name': 'Accent Wall', 'subcategory': 'Walls', 'cost': Decimal('3'), 'unit': 'sqft'},
                    {'name': 'Textured Wall Painting', 'subcategory': 'Walls', 'cost': Decimal('3.50'), 'unit': 'sqft'},

                    {'name': 'Ceiling Painting', 'subcategory': 'Ceilings', 'cost': Decimal('2'), 'unit': 'sqft'},
                    {'name': 'Vaulted Ceiling', 'subcategory': 'Ceilings', 'cost': Decimal('3'), 'unit': 'sqft'},
                    {'name': 'Coffered Ceiling Paint', 'subcategory': 'Ceilings', 'cost': Decimal('4'), 'unit': 'sqft'},

                    {'name': 'Baseboard Painting', 'subcategory': 'Trim', 'cost': Decimal('2.50'), 'unit': 'linear_ft'},
                    {'name': 'Door & Frame Painting', 'subcategory': 'Trim', 'cost': Decimal('75'), 'unit': 'each'},
                    {'name': 'Window Trim Painting', 'subcategory': 'Trim', 'cost': Decimal('45'), 'unit': 'each'},
                    {'name': 'Crown Molding Painting', 'subcategory': 'Trim', 'cost': Decimal('3'), 'unit': 'linear_ft'},

                    {'name': 'Kitchen Cabinet Painting', 'subcategory': 'Specialty', 'cost': Decimal('80'), 'unit': 'linear_ft'},
                    {'name': 'Drywall Repair & Paint', 'subcategory': 'Specialty', 'cost': Decimal('150'), 'unit': 'each'},
                ]
            },

            # ========== PAINTING - EXTERIOR ==========
            {
                'name': 'Painting - Exterior',
                'icon': '🏡',
                'desc': 'Exterior painting and staining',
                'keywords': 'paint,exterior,siding,deck,stain',
                'activities': [
                    {'name': 'Siding Painting (2 coats)', 'subcategory': 'Siding', 'cost': Decimal('3.50'), 'unit': 'sqft'},
                    {'name': 'Brick Painting', 'subcategory': 'Siding', 'cost': Decimal('4'), 'unit': 'sqft'},
                    {'name': 'Stucco Painting', 'subcategory': 'Siding', 'cost': Decimal('4.50'), 'unit': 'sqft'},

                    {'name': 'Exterior Trim Painting', 'subcategory': 'Trim', 'cost': Decimal('4'), 'unit': 'linear_ft'},
                    {'name': 'Fascia & Soffit', 'subcategory': 'Trim', 'cost': Decimal('3.50'), 'unit': 'linear_ft'},
                    {'name': 'Garage Door Painting', 'subcategory': 'Trim', 'cost': Decimal('200'), 'unit': 'each'},

                    {'name': 'Deck Staining', 'subcategory': 'Staining', 'cost': Decimal('2.50'), 'unit': 'sqft'},
                    {'name': 'Fence Staining', 'subcategory': 'Staining', 'cost': Decimal('3'), 'unit': 'sqft'},

                    {'name': 'Power Washing', 'subcategory': 'Prep', 'cost': Decimal('0.50'), 'unit': 'sqft'},
                    {'name': 'Caulking & Sealing', 'subcategory': 'Prep', 'cost': Decimal('2'), 'unit': 'linear_ft'},
                ]
            },

            # ========== DRYWALL & CEILINGS ==========
            {
                'name': 'Drywall & Ceilings',
                'icon': '⬜',
                'desc': 'Drywall installation and ceiling work',
                'keywords': 'drywall,sheetrock,ceiling,texture',
                'activities': [
                    {'name': 'Drywall Install 1/2"', 'subcategory': 'Drywall', 'cost': Decimal('2.50'), 'unit': 'sqft'},
                    {'name': 'Drywall Install 5/8"', 'subcategory': 'Drywall', 'cost': Decimal('2.75'), 'unit': 'sqft'},
                    {'name': 'Moisture Resistant Drywall', 'subcategory': 'Drywall', 'cost': Decimal('3'), 'unit': 'sqft'},
                    {'name': 'Soundproof Drywall', 'subcategory': 'Drywall', 'cost': Decimal('4'), 'unit': 'sqft'},

                    {'name': 'Drywall Finish Level 4', 'subcategory': 'Finishing', 'cost': Decimal('1.50'), 'unit': 'sqft'},
                    {'name': 'Drywall Finish Level 5', 'subcategory': 'Finishing', 'cost': Decimal('2'), 'unit': 'sqft'},
                    {'name': 'Texture - Knockdown', 'subcategory': 'Finishing', 'cost': Decimal('1'), 'unit': 'sqft'},
                    {'name': 'Texture - Orange Peel', 'subcategory': 'Finishing', 'cost': Decimal('0.75'), 'unit': 'sqft'},

                    {'name': 'Tray Ceiling', 'subcategory': 'Specialty Ceilings', 'cost': Decimal('12'), 'unit': 'sqft'},
                    {'name': 'Coffered Ceiling', 'subcategory': 'Specialty Ceilings', 'cost': Decimal('35'), 'unit': 'sqft'},
                    {'name': 'Vaulted Ceiling Drywall', 'subcategory': 'Specialty Ceilings', 'cost': Decimal('4'), 'unit': 'sqft'},
                ]
            },

            # ========== DOORS & WINDOWS ==========
            {
                'name': 'Doors & Windows',
                'icon': '🚪',
                'desc': 'Door and window installation',
                'keywords': 'door,window,entry,french,slider',
                'activities': [
                    {'name': 'Interior Door - Hollow Core', 'subcategory': 'Interior Doors', 'cost': Decimal('200'), 'unit': 'each'},
                    {'name': 'Interior Door - Solid Core', 'subcategory': 'Interior Doors', 'cost': Decimal('350'), 'unit': 'each'},
                    {'name': 'French Doors Interior', 'subcategory': 'Interior Doors', 'cost': Decimal('800'), 'unit': 'each'},
                    {'name': 'Barn Door with Hardware', 'subcategory': 'Interior Doors', 'cost': Decimal('600'), 'unit': 'each'},

                    {'name': 'Entry Door - Steel', 'subcategory': 'Exterior Doors', 'cost': Decimal('800'), 'unit': 'each'},
                    {'name': 'Entry Door - Fiberglass', 'subcategory': 'Exterior Doors', 'cost': Decimal('1200'), 'unit': 'each'},
                    {'name': 'Entry Door - Wood', 'subcategory': 'Exterior Doors', 'cost': Decimal('1500'), 'unit': 'each'},
                    {'name': 'French Doors Exterior', 'subcategory': 'Exterior Doors', 'cost': Decimal('2000'), 'unit': 'each'},
                    {'name': 'Sliding Glass Door', 'subcategory': 'Exterior Doors', 'cost': Decimal('1800'), 'unit': 'each'},
                    {'name': 'Garage Door - Single', 'subcategory': 'Exterior Doors', 'cost': Decimal('1200'), 'unit': 'each'},
                    {'name': 'Garage Door - Double', 'subcategory': 'Exterior Doors', 'cost': Decimal('1800'), 'unit': 'each'},

                    {'name': 'Vinyl Window', 'subcategory': 'Windows', 'cost': Decimal('450'), 'unit': 'each'},
                    {'name': 'Wood Window', 'subcategory': 'Windows', 'cost': Decimal('700'), 'unit': 'each'},
                    {'name': 'Aluminum Clad Window', 'subcategory': 'Windows', 'cost': Decimal('650'), 'unit': 'each'},
                    {'name': 'Bay Window', 'subcategory': 'Windows', 'cost': Decimal('2500'), 'unit': 'each'},
                    {'name': 'Skylight Installation', 'subcategory': 'Windows', 'cost': Decimal('1500'), 'unit': 'each'},
                ]
            },

            # ========== DECKING & OUTDOOR ==========
            {
                'name': 'Decking & Outdoor',
                'icon': '🌳',
                'desc': 'Deck, patio, and outdoor structures',
                'keywords': 'deck,patio,pergola,fence,outdoor',
                'activities': [
                    {'name': 'Pressure Treated Decking', 'subcategory': 'Deck Materials', 'cost': Decimal('25'), 'unit': 'sqft'},
                    {'name': 'Cedar Decking', 'subcategory': 'Deck Materials', 'cost': Decimal('35'), 'unit': 'sqft'},
                    {'name': 'Composite Decking', 'subcategory': 'Deck Materials', 'cost': Decimal('45'), 'unit': 'sqft'},
                    {'name': 'PVC Decking', 'subcategory': 'Deck Materials', 'cost': Decimal('55'), 'unit': 'sqft'},

                    {'name': 'Wood Deck Railing', 'subcategory': 'Railings', 'cost': Decimal('80'), 'unit': 'linear_ft'},
                    {'name': 'Composite Railing', 'subcategory': 'Railings', 'cost': Decimal('120'), 'unit': 'linear_ft'},
                    {'name': 'Cable Railing', 'subcategory': 'Railings', 'cost': Decimal('150'), 'unit': 'linear_ft'},
                    {'name': 'Deck Stairs', 'subcategory': 'Railings', 'cost': Decimal('400'), 'unit': 'each'},

                    {'name': 'Concrete Patio', 'subcategory': 'Patios', 'cost': Decimal('12'), 'unit': 'sqft'},
                    {'name': 'Stamped Concrete Patio', 'subcategory': 'Patios', 'cost': Decimal('18'), 'unit': 'sqft'},
                    {'name': 'Paver Patio', 'subcategory': 'Patios', 'cost': Decimal('20'), 'unit': 'sqft'},

                    {'name': 'Wood Pergola 10x10', 'subcategory': 'Structures', 'cost': Decimal('3500'), 'unit': 'each'},
                    {'name': 'Vinyl Pergola 10x10', 'subcategory': 'Structures', 'cost': Decimal('4500'), 'unit': 'each'},
                    {'name': 'Privacy Fence 6ft Wood', 'subcategory': 'Structures', 'cost': Decimal('30'), 'unit': 'linear_ft'},
                    {'name': 'Vinyl Fence 6ft', 'subcategory': 'Structures', 'cost': Decimal('45'), 'unit': 'linear_ft'},
                ]
            },
        ]

        print(f"\nCreating {len(categories_data)} granular categories...\n")

        total_activities = 0
        for cat_data in categories_data:
            # Create category
            category = POSCategory(
                user_id=user.id,
                name=cat_data['name'],
                description=cat_data['desc'],
                keywords=cat_data['keywords'],
                icon=cat_data['icon']
            )
            db.session.add(category)
            db.session.flush()

            # Add activities
            activities = cat_data['activities']
            for idx, act in enumerate(activities):
                activity = POSActivity(
                    category_id=category.id,
                    name=act['name'],
                    subcategory=act.get('subcategory'),
                    base_cost=act['cost'],
                    unit=act.get('unit', 'each'),
                    has_subitems=False,
                    order_index=idx
                )
                db.session.add(activity)
                total_activities += 1

            print(f"[OK] {cat_data['icon']} {cat_data['name']}: {len(activities)} activities")

        db.session.commit()

        print("\n" + "="*60)
        print("GRANULAR POS CATEGORIES - COMPLETE!")
        print("="*60)
        print(f"Categories created: {len(categories_data)}")
        print(f"Total activities: {total_activities}")
        print("\nCategories are now more specific and distilled!")
        print("="*60)

if __name__ == '__main__':
    seed_granular_pos_categories()
