# Multi-Layer POS System Documentation

## Overview

The Multi-Layer POS (Point of Sale) System is an intelligent quote-building feature for ContractorPro that filters available activities based on job specifications selected by the user. This creates a curated, streamlined experience where users only see relevant options for their specific project.

## System Architecture

### Layer 1: Job Specification Selection
Users select from 28 standard construction job specifications:

1. **Place and Permits** - Site preparation, permits, regulatory approvals
2. **Tear Out and Demolition** - Removal of existing structures
3. **Excavation and Grading** - Earth moving, site preparation
4. **Concrete** - Foundation, slabs, footings
5. **Masonry** - Brick, block, stone work
6. **Floor Framing** - Floor joists, subfloor systems
7. **Wall Framing** - Wall studs, plates, headers
8. **Roof Framing** - Rafters, trusses, roof decking
9. **Roof Covering** - Shingles, tiles, waterproofing
10. **Flashing** - Roof drainage, water management
11. **Exterior Trim** - Fascia, soffit, rake boards
12. **Porches and Decks** - Outdoor structures, railings
13. **Siding** - Exterior cladding, weather protection
14. **Doors and Door Trim** - Interior/exterior doors
15. **Windows and Window Trim** - Glazing, window installation
16. **Plumbing** - Water supply, drainage, fixtures
17. **Heating and A/C** - HVAC systems, ductwork
18. **Electrical** - Wiring, panels, outlets
19. **Insulation** - Thermal and sound insulation
20. **Interior Wall Covering** - Drywall, plaster, paneling
21. **Ceiling Covering** - Ceiling finishes
22. **Millwork Trim** - Baseboards, crown molding
23. **Stairs** - Stairways, railings
24. **Cabinets and Appliances** - Kitchen/bathroom cabinetry
25. **Specialties** - Mirrors, shelving, hardware
26. **Floor Covering** - Tile, carpet, hardwood
27. **Painting and Decorating** - Interior/exterior painting
28. **Clean Up** - Final cleaning, debris removal

### Layer 2: Filtered Categories & Activities
Based on Layer 1 selections, the system displays only relevant POS categories and their activities.

**Example Flow:**
```
User selects: "Plumbing", "Electrical", "Cabinets and Appliances"
↓
System shows categories: "Kitchen", "Bathroom"
↓
User selects "Kitchen" category
↓
System shows only activities mapped to selected job specs:
  - Install New Sink (Plumbing)
  - Install Electrical Outlets (Electrical)
  - Install Cabinets (Cabinets and Appliances)
```

## Database Schema

### New Tables

#### `job_specification`
Stores the 28 standard construction job specifications.

```sql
CREATE TABLE job_specification (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    display_name VARCHAR(150) NOT NULL,
    description TEXT,
    order_index INTEGER DEFAULT 1,
    is_active BOOLEAN DEFAULT TRUE,
    created_date DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

#### `pos_category_spec_mapping`
Maps POS categories to job specifications for filtering.

```sql
CREATE TABLE pos_category_spec_mapping (
    id INTEGER PRIMARY KEY,
    category_id INTEGER NOT NULL,
    spec_id INTEGER NOT NULL,
    specific_activity_ids TEXT,  -- JSON array (optional)
    created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES pos_category(id),
    FOREIGN KEY (spec_id) REFERENCES job_specification(id),
    UNIQUE(category_id, spec_id)
);
```

#### `pos_session`
Tracks user's current POS session and selections.

```sql
CREATE TABLE pos_session (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    session_token VARCHAR(100) UNIQUE NOT NULL,
    selected_spec_ids TEXT,  -- JSON array of spec IDs
    current_layer INTEGER DEFAULT 1,
    current_category_id INTEGER,
    project_description TEXT,
    created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (current_category_id) REFERENCES pos_category(id)
);
```

## API Endpoints

### Job Specification Endpoints

#### `GET /api/pos/job-specifications`
Get all active job specifications.

**Response:**
```json
[
  {
    "id": 1,
    "name": "place_and_permits",
    "display_name": "Place and Permits",
    "description": "Site preparation, permits, and regulatory approvals",
    "order_index": 1
  },
  ...
]
```

### Session Management Endpoints

#### `POST /api/pos/session/start`
Start a new POS session with selected job specifications.

**Request:**
```json
{
  "selected_specs": [16, 18, 24],  // IDs for Plumbing, Electrical, Cabinets
  "project_description": "Kitchen renovation"
}
```

**Response:**
```json
{
  "success": true,
  "session_token": "550e8400-e29b-41d4-a716-446655440000",
  "selected_specs": [16, 18, 24],
  "next_layer": 2
}
```

#### `GET /api/pos/session/{token}/categories`
Get filtered categories based on session's job specification selections.

**Response:**
```json
{
  "session_token": "550e8400-e29b-41d4-a716-446655440000",
  "categories": [
    {
      "id": 5,
      "name": "Kitchen",
      "description": "Kitchen renovation activities",
      "icon": "🍳",
      "keywords": ["kitchen", "cooking", "culinary"]
    }
  ],
  "count": 1
}
```

#### `GET /api/pos/session/{token}/category/{id}/activities`
Get filtered activities for a specific category based on job specs.

**Response:**
```json
{
  "session_token": "550e8400-e29b-41d4-a716-446655440000",
  "category": {
    "id": 5,
    "name": "Kitchen",
    "description": "Kitchen renovation activities"
  },
  "activities": [
    {
      "id": 42,
      "name": "Install New Sink",
      "description": "Install kitchen sink with faucet",
      "base_cost": 800.00,
      "unit": "each",
      "has_subitems": true
    }
  ],
  "count": 1
}
```

### Admin Endpoints

#### `GET /api/pos/spec-mappings`
Get all specification mappings for the current user's categories.

**Response:**
```json
[
  {
    "id": 1,
    "category_id": 5,
    "spec_id": 16,
    "specific_activity_ids": null
  }
]
```

#### `POST /api/pos/spec-mappings`
Save specification mappings for a category.

**Request:**
```json
{
  "category_id": 5,
  "spec_ids": [16, 18, 24]  // Plumbing, Electrical, Cabinets
}
```

**Response:**
```json
{
  "success": true,
  "message": "Saved 3 mappings for category Kitchen"
}
```

## Setup Instructions

### 1. Run Setup Script

```bash
python setup_multilayer_pos.py
```

This will:
- Create new database tables
- Seed 28 job specifications
- Display next steps

### 2. Create POS Categories

Navigate to: `http://localhost:5000/pos/admin`

Create categories relevant to your business:
- Kitchen
- Bathroom
- Roofing
- Siding
- Flooring
- etc.

For each category, provide:
- **Name**: Kitchen
- **Description**: Kitchen renovation and remodeling
- **Icon**: 🍳 (emoji or icon class)
- **Keywords**: kitchen,cooking,culinary,appliances

### 3. Add Activities to Categories

In the POS Admin interface, add activities to each category:

**Example: Kitchen Category**
| Activity | Base Cost | Unit |
|----------|-----------|------|
| Install New Cabinets | $5,000 | each |
| Countertop Installation | $2,500 | sqft |
| Install Sink and Faucet | $800 | each |
| Install Dishwasher | $600 | each |
| Electrical Outlets | $150 | each |
| Plumbing Rough-In | $1,200 | job |
| Paint Kitchen | $800 | room |
| Install Flooring | $2,000 | sqft |

### 4. Map Categories to Job Specifications

Navigate to: `http://localhost:5000/pos/admin/spec-mappings`

For each category, select which job specifications apply:

**Example: Kitchen Category Mappings**
- ✅ Tear Out and Demolition
- ✅ Plumbing
- ✅ Electrical
- ✅ Interior Wall Covering
- ✅ Cabinets and Appliances
- ✅ Floor Covering
- ✅ Painting and Decorating
- ✅ Clean Up

**Example: Bathroom Category Mappings**
- ✅ Tear Out and Demolition
- ✅ Plumbing
- ✅ Electrical
- ✅ Interior Wall Covering
- ✅ Ceiling Covering
- ✅ Cabinets and Appliances
- ✅ Specialties (mirrors, shelving)
- ✅ Floor Covering
- ✅ Painting and Decorating
- ✅ Clean Up

**Example: Roofing Category Mappings**
- ✅ Roof Framing
- ✅ Roof Covering
- ✅ Flashing
- ✅ Clean Up

### 5. Use the Multi-Layer POS System

Navigate to: `http://localhost:5000/pos/multilayer`

**User Flow:**

1. **Layer 1: Job Specifications**
   - User sees 28 checkboxes with construction specifications
   - User selects applicable specs (e.g., Plumbing, Electrical, Cabinets)
   - User clicks "Continue to Categories"

2. **Layer 2: Filtered Categories**
   - System displays only categories mapped to selected specs
   - In our example, Kitchen and Bathroom would appear
   - User selects a category (e.g., Kitchen)

3. **Layer 2: Filtered Activities**
   - System displays only activities within the category
   - User configures quantity and options
   - User adds items to cart

4. **Quote Completion**
   - User reviews cart
   - User saves quote
   - System redirects to quote detail page

## Configuration Options

### Global Settings

In the POS Admin interface, you can:

1. **Activate/Deactivate Job Specifications**
   - Edit `job_specification` table
   - Set `is_active = FALSE` to hide specs

2. **Reorder Job Specifications**
   - Modify `order_index` values
   - Lower numbers appear first

3. **Customize Descriptions**
   - Update `description` field
   - Provide context-specific guidance

### Advanced: Activity-Level Filtering

The system supports filtering specific activities within a category:

```python
# In POSCategorySpecMapping
mapping = POSCategorySpecMapping(
    category_id=5,  # Kitchen
    spec_id=16,     # Plumbing
    specific_activity_ids='[42, 45, 48]'  # Only show specific activities
)
```

This allows fine-grained control over which activities appear for each job spec.

## User Interface

### Layer 1: Job Specifications
![Layer 1 Screenshot Placeholder]

**Features:**
- Grid layout with checkboxes
- Visual feedback on selection
- Running count of selected specs
- Disabled "Continue" button until selection made

### Layer 2: Categories & Activities
![Layer 2 Screenshot Placeholder]

**Features:**
- Breadcrumb navigation (Layer 1 → Layer 2)
- Filtered category cards
- Activity cards with pricing
- Sticky cart sidebar
- Real-time total calculation

### Admin: Specification Mappings
![Admin Screenshot Placeholder]

**Features:**
- Category-by-category configuration
- Visual checkboxes for all 28 specs
- Save button per category
- Success feedback

## Workflow Examples

### Example 1: Kitchen Renovation Quote

**User Selections (Layer 1):**
- ✅ Tear Out and Demolition
- ✅ Plumbing
- ✅ Electrical
- ✅ Cabinets and Appliances
- ✅ Floor Covering
- ✅ Painting and Decorating

**System Response (Layer 2):**
- Shows: Kitchen, Bathroom (both mapped to these specs)
- User selects Kitchen
- Shows only kitchen activities mapped to selected specs
- Cart total: $12,450

### Example 2: Bathroom Remodel Quote

**User Selections (Layer 1):**
- ✅ Plumbing
- ✅ Electrical
- ✅ Interior Wall Covering
- ✅ Cabinets and Appliances
- ✅ Specialties

**System Response (Layer 2):**
- Shows: Bathroom (only category mapped to all these specs)
- User selects Bathroom
- Shows bathroom activities
- Cart total: $8,200

### Example 3: New Construction Quote

**User Selections (Layer 1):**
- ✅ (All 28 specifications selected)

**System Response (Layer 2):**
- Shows: All POS categories
- Maximum flexibility
- User builds comprehensive quote

## Benefits

### For Contractors

1. **Faster Quote Generation**
   - Users only see relevant options
   - Reduced cognitive load
   - Streamlined selection process

2. **Fewer Errors**
   - Intelligent filtering prevents irrelevant selections
   - Context-aware options

3. **Professionalism**
   - Curated experience shows expertise
   - Industry-standard terminology (CSI MasterFormat-inspired)

4. **Scalability**
   - Add new categories without overwhelming users
   - System automatically filters based on job specs

### For Clients

1. **Clarity**
   - Understand exactly what work is included
   - Specifications listed explicitly

2. **Customization**
   - Select only applicable work categories
   - See relevant options immediately

3. **Transparency**
   - Clear breakdown by specification
   - No hidden assumptions

## Troubleshooting

### Issue: No categories appear in Layer 2

**Solution:**
- Verify you've created POS categories in `/pos/admin`
- Check that categories are mapped to job specs in `/pos/admin/spec-mappings`
- Ensure selected job specs have at least one category mapping

### Issue: No activities appear for a category

**Solution:**
- Verify activities exist for the category in `/pos/admin`
- Check that the category is mapped to the job specs you selected in Layer 1
- If using `specific_activity_ids`, verify the activity IDs are correct

### Issue: Session errors

**Solution:**
- Sessions are stored in database with unique tokens
- If experiencing issues, clear old sessions:
  ```python
  POSSession.query.filter(POSSession.is_active == False).delete()
  ```

### Issue: Mappings not saving

**Solution:**
- Check browser console for JavaScript errors
- Verify `/api/pos/spec-mappings` route is accessible
- Check database foreign key constraints

## Future Enhancements

### Planned Features

1. **Layer 3: Sub-Activity Drill-Down**
   - Further granularity based on activity options
   - Dynamic forms based on previous selections

2. **Smart Recommendations**
   - AI-suggested job spec combinations
   - "Customers who selected X also selected Y"

3. **Template Job Specs**
   - Pre-configured spec bundles
   - "Kitchen Remodel" = auto-select 8 specs
   - "New Construction" = auto-select all specs

4. **Export Job Specs**
   - PDF export of selected specifications
   - Include descriptions and scope details

5. **Import from CSI MasterFormat**
   - Direct import of CSI codes
   - Industry-standard compliance

6. **Multi-User Spec Libraries**
   - Share spec configurations across team
   - Company-wide standardization

## Technical Details

### Session Management

Sessions use UUID tokens for security and uniqueness:

```python
import uuid
session_token = str(uuid.uuid4())
# Example: '550e8400-e29b-41d4-a716-446655440000'
```

Sessions track:
- User ID (for data isolation)
- Selected specification IDs (JSON array)
- Current layer (1 or 2)
- Current category (if in Layer 2)
- Project description (optional)

### Filtering Algorithm

```python
# Pseudocode for category filtering
selected_specs = [16, 18, 24]  # Plumbing, Electrical, Cabinets

# Get all mappings where spec_id is in selected_specs
mappings = POSCategorySpecMapping.filter(spec_id IN selected_specs)

# Get unique category IDs from mappings
category_ids = unique([m.category_id for m in mappings])

# Return only these categories
filtered_categories = POSCategory.filter(id IN category_ids)
```

### Performance Optimization

1. **Database Indexes**
   ```sql
   CREATE INDEX idx_mapping_spec ON pos_category_spec_mapping(spec_id);
   CREATE INDEX idx_mapping_category ON pos_category_spec_mapping(category_id);
   CREATE INDEX idx_session_token ON pos_session(session_token);
   ```

2. **Caching** (Future)
   - Cache job specifications (rarely change)
   - Cache category-spec mappings per user
   - Invalidate on admin changes

## Support

For questions or issues:
1. Check this documentation
2. Review `/pos/admin` for configuration
3. Check browser console for JavaScript errors
4. Review application logs for API errors

## License

Part of ContractorPro - Intelligent Construction Business Automation Platform

---

**Version:** 1.0.0
**Last Updated:** 2025-01-01
**Author:** ContractorPro Development Team
