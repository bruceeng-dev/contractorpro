# Multi-Layer POS System - Architecture Clarification

## Current System Behavior (As Implemented)

### Layer 1: Job Specification Selection
- User selects job specs that apply to the ENTIRE JOB (global scope)
- Examples: "Plumbing", "Electrical", "Roof Covering"
- These selections are stored in POSSession and apply to all subsequent filtering

### Layer 2: Category Selection
- **ALL categories are ALWAYS shown** (Kitchen, Bathroom, Roofing, Flooring, Painting, Decking, Permits & Inspections, Demolition & Site Prep)
- Categories are NOT filtered based on Layer 1 selections
- User can select any category to view activities

### Activity Filtering (The Smart Part)
- When user selects a category, activities within that category ARE filtered
- Filtering logic (app.py lines 1335-1352):
  ```python
  # Get activities for selected category
  all_activities = POSActivity.query.filter_by(category_id=category_id).all()

  # Filter based on job_spec_tags matching selected specs from Layer 1
  for activity in all_activities:
      if activity.job_spec_tags:
          activity_tags = json.loads(activity.job_spec_tags)
          if any(tag in selected_spec_names for tag in activity_tags):
              filtered_activities.append(activity)  # SHOW THIS
  ```

**Example Flow**:
1. User selects "Plumbing" and "Electrical" in Layer 1
2. User sees ALL 8 categories in Layer 2
3. User clicks "Kitchen" category
4. System shows ONLY activities tagged with "plumbing" or "electrical"
   - ✅ "Install Kitchen Sink" (tagged: plumbing)
   - ✅ "Install Electrical Outlets" (tagged: electrical)
   - ❌ "Install Cabinets" (tagged: cabinets_appliances) - HIDDEN
   - ❌ "Paint Kitchen" (tagged: painting_decorating) - HIDDEN

## Room/Location Organization (Separate Layer)

Rooms/locations are used for **output organization**, not filtering:
- Job specs filter activities (global scope)
- User builds cart with selected activities
- When generating contract/quote, activities are organized by room
- Contract shows cost breakdown per room

**Contract Output Example**:
```
Kitchen:
  - Install Kitchen Sink: $800
  - Install Electrical Outlets: $450
  Subtotal: $1,250

Bathroom 1:
  - Install Bathroom Sink: $600
  - Install GFCI Outlet: $150
  Subtotal: $750

TOTAL CONTRACT: $2,000
```

## POSCategorySpecMapping (Admin Tool Only)

The POSCategorySpecMapping table exists but is **NOT used for filtering**. It's an admin configuration tool to help manage which specs are relevant to which categories during setup.

**It does NOT affect runtime filtering.** All filtering is done via activity-level `job_spec_tags`.

## Summary

✅ **Job specs apply to the entire job** (global filtering)
✅ **Categories are always shown** (no category-level filtering)
✅ **Activities are filtered** based on job_spec_tags
✅ **Rooms are used for organization** in contract output, not for filtering

This is exactly what the user requested: "spec mappings should be for the entire job, not for each room, however each room can be broken out on the next layer"

The system is working correctly as designed.
