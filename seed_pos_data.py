"""
Seed script for POS system data
Adds sample categories, activities, and subitems for common construction projects
"""

from app import app
from models import db, User, POSCategory, POSActivity, POSSubItem
from decimal import Decimal

def seed_pos_data():
    """Seed the database with sample POS data"""
    with app.app_context():
        # Get the first user (admin)
        user = User.query.first()
        if not user:
            print("Error: No users found. Please create a user first.")
            return

        print(f"Seeding POS data for user: {user.username}")

        # Check if data already exists
        existing_categories = POSCategory.query.filter_by(user_id=user.id).count()
        if existing_categories > 0:
            response = input(f"Found {existing_categories} existing categories. Delete and reseed? (y/n): ")
            if response.lower() == 'y':
                # Delete existing data
                POSCategory.query.filter_by(user_id=user.id).delete()
                db.session.commit()
                print("Existing POS data deleted.")
            else:
                print("Keeping existing data. Exiting.")
                return

        # KITCHEN RENOVATION Category
        kitchen_cat = POSCategory(
            user_id=user.id,
            name="Kitchen Renovation",
            description="Complete kitchen remodeling services",
            keywords="kitchen,cooking,cabinets,countertops,appliances,sink",
            icon="🍳"
        )
        db.session.add(kitchen_cat)
        db.session.flush()

        # Kitchen Activities
        kitchen_activities = [
            {
                'name': 'Kitchen Cabinets',
                'description': 'New kitchen cabinet installation',
                'base_cost': Decimal('5000.00'),
                'unit': 'set',
                'has_subitems': True
            },
            {
                'name': 'Countertops',
                'description': 'Countertop installation',
                'base_cost': Decimal('3000.00'),
                'unit': 'sqft',
                'has_subitems': True
            },
            {
                'name': 'Kitchen Sink',
                'description': 'Sink installation with plumbing',
                'base_cost': Decimal('800.00'),
                'unit': 'each',
                'has_subitems': True
            },
            {
                'name': 'Backsplash',
                'description': 'Tile backsplash installation',
                'base_cost': Decimal('1200.00'),
                'unit': 'sqft',
                'has_subitems': False
            },
            {
                'name': 'Kitchen Flooring',
                'description': 'Kitchen floor installation',
                'base_cost': Decimal('2500.00'),
                'unit': 'sqft',
                'has_subitems': True
            }
        ]

        for idx, act_data in enumerate(kitchen_activities, 1):
            activity = POSActivity(
                category_id=kitchen_cat.id,
                name=act_data['name'],
                description=act_data['description'],
                base_cost=act_data['base_cost'],
                unit=act_data['unit'],
                has_subitems=act_data['has_subitems'],
                order_index=idx
            )
            db.session.add(activity)
            db.session.flush()

            # Add subitems for cabinets
            if act_data['name'] == 'Kitchen Cabinets':
                material_question = POSSubItem(
                    activity_id=activity.id,
                    name='Cabinet Material',
                    question_text='What cabinet material would you like?',
                    option_type='choice',
                    is_required=True,
                    order_index=1
                )
                db.session.add(material_question)
                db.session.flush()

                # Material options
                materials = [
                    ('Laminate', Decimal('0')),
                    ('Wood Veneer', Decimal('1500')),
                    ('Solid Wood', Decimal('3000')),
                    ('High-End Custom', Decimal('5000'))
                ]
                for mat_idx, (mat_name, mat_cost) in enumerate(materials, 1):
                    mat_option = POSSubItem(
                        activity_id=activity.id,
                        parent_id=material_question.id,
                        name=mat_name,
                        cost_modifier=mat_cost,
                        order_index=mat_idx
                    )
                    db.session.add(mat_option)

            # Add subitems for countertops
            elif act_data['name'] == 'Countertops':
                material_question = POSSubItem(
                    activity_id=activity.id,
                    name='Countertop Material',
                    question_text='What countertop material?',
                    option_type='choice',
                    is_required=True,
                    order_index=1
                )
                db.session.add(material_question)
                db.session.flush()

                materials = [
                    ('Laminate', Decimal('0')),
                    ('Granite', Decimal('50')),
                    ('Quartz', Decimal('75')),
                    ('Marble', Decimal('100'))
                ]
                for mat_idx, (mat_name, mat_cost) in enumerate(materials, 1):
                    mat_option = POSSubItem(
                        activity_id=activity.id,
                        parent_id=material_question.id,
                        name=mat_name,
                        cost_modifier=mat_cost,
                        order_index=mat_idx
                    )
                    db.session.add(mat_option)

            # Add subitems for sink
            elif act_data['name'] == 'Kitchen Sink':
                sink_question = POSSubItem(
                    activity_id=activity.id,
                    name='Sink Type',
                    question_text='What type of sink?',
                    option_type='choice',
                    is_required=True,
                    order_index=1
                )
                db.session.add(sink_question)
                db.session.flush()

                sinks = [
                    ('Single Basin Stainless', Decimal('0')),
                    ('Double Basin Stainless', Decimal('150')),
                    ('Farmhouse Sink', Decimal('400')),
                    ('Granite Composite', Decimal('350'))
                ]
                for sink_idx, (sink_name, sink_cost) in enumerate(sinks, 1):
                    sink_option = POSSubItem(
                        activity_id=activity.id,
                        parent_id=sink_question.id,
                        name=sink_name,
                        cost_modifier=sink_cost,
                        order_index=sink_idx
                    )
                    db.session.add(sink_option)

        # BATHROOM RENOVATION Category
        bathroom_cat = POSCategory(
            user_id=user.id,
            name="Bathroom Renovation",
            description="Full bathroom remodeling services",
            keywords="bathroom,shower,tub,toilet,vanity,tile",
            icon="🚿"
        )
        db.session.add(bathroom_cat)
        db.session.flush()

        # Bathroom Activities
        bathroom_activities = [
            {
                'name': 'Shower Installation',
                'description': 'New shower with tile surround',
                'base_cost': Decimal('3500.00'),
                'unit': 'each',
                'has_subitems': True
            },
            {
                'name': 'Bathtub Replacement',
                'description': 'Replace existing bathtub',
                'base_cost': Decimal('2000.00'),
                'unit': 'each',
                'has_subitems': True
            },
            {
                'name': 'Vanity & Sink',
                'description': 'Bathroom vanity installation',
                'base_cost': Decimal('1500.00'),
                'unit': 'each',
                'has_subitems': True
            },
            {
                'name': 'Toilet Replacement',
                'description': 'New toilet installation',
                'base_cost': Decimal('400.00'),
                'unit': 'each',
                'has_subitems': True
            },
            {
                'name': 'Bathroom Flooring',
                'description': 'Tile or vinyl flooring',
                'base_cost': Decimal('1800.00'),
                'unit': 'sqft',
                'has_subitems': True
            }
        ]

        for idx, act_data in enumerate(bathroom_activities, 1):
            activity = POSActivity(
                category_id=bathroom_cat.id,
                name=act_data['name'],
                description=act_data['description'],
                base_cost=act_data['base_cost'],
                unit=act_data['unit'],
                has_subitems=act_data['has_subitems'],
                order_index=idx
            )
            db.session.add(activity)
            db.session.flush()

            # Add subitems for shower
            if act_data['name'] == 'Shower Installation':
                shower_question = POSSubItem(
                    activity_id=activity.id,
                    name='Shower Type',
                    question_text='What type of shower?',
                    option_type='choice',
                    is_required=True,
                    order_index=1
                )
                db.session.add(shower_question)
                db.session.flush()

                showers = [
                    ('Standard Fiberglass', Decimal('0')),
                    ('Tile Surround', Decimal('1200')),
                    ('Custom Tile with Glass Door', Decimal('2500')),
                    ('Luxury Walk-in Shower', Decimal('4000'))
                ]
                for sh_idx, (sh_name, sh_cost) in enumerate(showers, 1):
                    sh_option = POSSubItem(
                        activity_id=activity.id,
                        parent_id=shower_question.id,
                        name=sh_name,
                        cost_modifier=sh_cost,
                        order_index=sh_idx
                    )
                    db.session.add(sh_option)

        # ROOFING Category
        roofing_cat = POSCategory(
            user_id=user.id,
            name="Roofing",
            description="Roof repair and replacement services",
            keywords="roof,shingles,roofing,leak,repair",
            icon="🏠"
        )
        db.session.add(roofing_cat)
        db.session.flush()

        # Roofing Activities
        roofing_activities = [
            {
                'name': 'Asphalt Shingle Roof',
                'description': 'Complete roof replacement with asphalt shingles',
                'base_cost': Decimal('45.00'),
                'unit': 'sqft',
                'has_subitems': True
            },
            {
                'name': 'Metal Roof',
                'description': 'Metal roofing installation',
                'base_cost': Decimal('85.00'),
                'unit': 'sqft',
                'has_subitems': False
            },
            {
                'name': 'Roof Repair',
                'description': 'Leak repair and shingle replacement',
                'base_cost': Decimal('500.00'),
                'unit': 'each',
                'has_subitems': False
            },
            {
                'name': 'Gutter Installation',
                'description': 'New gutter system',
                'base_cost': Decimal('15.00'),
                'unit': 'linear_ft',
                'has_subitems': True
            }
        ]

        for idx, act_data in enumerate(roofing_activities, 1):
            activity = POSActivity(
                category_id=roofing_cat.id,
                name=act_data['name'],
                description=act_data['description'],
                base_cost=act_data['base_cost'],
                unit=act_data['unit'],
                has_subitems=act_data['has_subitems'],
                order_index=idx
            )
            db.session.add(activity)

        # FLOORING Category
        flooring_cat = POSCategory(
            user_id=user.id,
            name="Flooring",
            description="Flooring installation services",
            keywords="floor,flooring,hardwood,tile,vinyl,carpet,laminate",
            icon="🪵"
        )
        db.session.add(flooring_cat)
        db.session.flush()

        # Flooring Activities
        flooring_activities = [
            {
                'name': 'Hardwood Flooring',
                'description': 'Solid hardwood floor installation',
                'base_cost': Decimal('12.00'),
                'unit': 'sqft',
                'has_subitems': True
            },
            {
                'name': 'Tile Flooring',
                'description': 'Ceramic or porcelain tile',
                'base_cost': Decimal('8.00'),
                'unit': 'sqft',
                'has_subitems': True
            },
            {
                'name': 'Vinyl Plank',
                'description': 'LVP flooring installation',
                'base_cost': Decimal('6.00'),
                'unit': 'sqft',
                'has_subitems': False
            },
            {
                'name': 'Carpet',
                'description': 'Wall-to-wall carpeting',
                'base_cost': Decimal('4.50'),
                'unit': 'sqft',
                'has_subitems': True
            }
        ]

        for idx, act_data in enumerate(flooring_activities, 1):
            activity = POSActivity(
                category_id=flooring_cat.id,
                name=act_data['name'],
                description=act_data['description'],
                base_cost=act_data['base_cost'],
                unit=act_data['unit'],
                has_subitems=act_data['has_subitems'],
                order_index=idx
            )
            db.session.add(activity)

        # PAINTING Category
        painting_cat = POSCategory(
            user_id=user.id,
            name="Painting",
            description="Interior and exterior painting services",
            keywords="paint,painting,interior,exterior,walls,trim",
            icon="🎨"
        )
        db.session.add(painting_cat)
        db.session.flush()

        # Painting Activities
        painting_activities = [
            {
                'name': 'Interior Painting',
                'description': 'Interior wall and ceiling painting',
                'base_cost': Decimal('2.50'),
                'unit': 'sqft',
                'has_subitems': False
            },
            {
                'name': 'Exterior Painting',
                'description': 'Exterior house painting',
                'base_cost': Decimal('3.50'),
                'unit': 'sqft',
                'has_subitems': False
            },
            {
                'name': 'Trim & Door Painting',
                'description': 'Paint trim, doors, and baseboards',
                'base_cost': Decimal('400.00'),
                'unit': 'room',
                'has_subitems': False
            },
            {
                'name': 'Cabinet Painting',
                'description': 'Kitchen cabinet refinishing',
                'base_cost': Decimal('2500.00'),
                'unit': 'set',
                'has_subitems': False
            }
        ]

        for idx, act_data in enumerate(painting_activities, 1):
            activity = POSActivity(
                category_id=painting_cat.id,
                name=act_data['name'],
                description=act_data['description'],
                base_cost=act_data['base_cost'],
                unit=act_data['unit'],
                has_subitems=act_data['has_subitems'],
                order_index=idx
            )
            db.session.add(activity)

        # Commit all changes
        db.session.commit()

        # Print summary
        total_categories = POSCategory.query.filter_by(user_id=user.id).count()
        total_activities = POSActivity.query.join(POSCategory).filter(POSCategory.user_id == user.id).count()
        total_subitems = POSSubItem.query.join(POSActivity).join(POSCategory).filter(POSCategory.user_id == user.id).count()

        print("\n✅ POS Data Seeding Complete!")
        print(f"📦 Categories created: {total_categories}")
        print(f"🔧 Activities created: {total_activities}")
        print(f"⚙️  Sub-options created: {total_subitems}")
        print(f"\n🎉 You can now access the POS system at: http://localhost:5000/pos")

if __name__ == '__main__':
    seed_pos_data()
