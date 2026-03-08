# POS Line Item Description Customization

## Overview

Now you can customize not just the contract template sections, but also the **individual POS line item descriptions**! When you edit a line item's description in a contract, that custom description is saved and will automatically appear in future contracts that include the same POS item.

## How It Works

### The Two-Level System:

```
Level 1: Contract Sections (Template Language)
└─ "## 3.4 Electrical Work"
   └─ Template text: "Contractor shall provide..."

Level 2: POS Line Items (Specific Work Items)
└─ Individual items with pricing:
   ├─ "Install electrical panel: $2,500"
   ├─ "Install GFCI outlets (10): $800"
   └─ "Install under-cabinet lighting: $600"
```

**Both levels are now fully editable and persist!**

## Example Workflow

### First Contract - Kitchen Renovation:

**POS Selection:**
- Activity: "Electrical Panel Installation"
- Sub-item: "Install 200A panel" → $2,500

**Contract Generated:**
```
Line item shows: "Install 200A panel: $2,500"
```

**You Edit:**
```
Change to: "Provide and install new 200-amp electrical service panel
with main breaker, surge protection, and proper grounding per NEC
code requirements: $2,500"
```

**Save** → Custom description stored in database

### Second Contract - Bathroom Renovation:

**POS Selection:**
- Activity: "Electrical Panel Installation"
- Sub-item: "Install 200A panel" → $2,500

**Contract Generated:**
```
Line item automatically shows: "Provide and install new 200-amp
electrical service panel with main breaker, surge protection, and
proper grounding per NEC code requirements: $2,500"
```

**No editing needed!** Your custom description appears automatically.

## Benefits

### 🎯 **Build Your Custom POS Library**
- Start with generic POS items
- Customize descriptions as you create contracts
- Build a library of professional, detailed line item descriptions
- Future contracts automatically use your refined descriptions

### ⏱️ **Massive Time Savings**
- Edit once per POS item
- Use forever across all contracts
- No more rewriting the same descriptions
- Consistency across all your quotes

### 📝 **Professional Detail**
- Add technical specifications
- Include code requirements
- Specify brands/materials
- Clarify scope boundaries

### 🔒 **User-Specific**
- Each contractor has their own custom descriptions
- Your terminology doesn't affect other users
- Perfect for teams with different specialties

## Database Structure

```python
POSItemTemplate:
- id: Unique identifier
- user_id: Links to the user
- pos_subitem_id: Links to the specific POS sub-item
- custom_description: Your customized description text
- original_description: Original POS description (for reference)
- created_date: When first customized
- updated_date: When last modified
```

## Technical Flow

### When Generating a Contract:

```python
# 1. Get POS quote items
quote_items = POSQuoteItem.query.filter_by(quote_id=quote.id).all()

# 2. For each item, check if user has custom description
for item in quote_items:
    custom_template = POSItemTemplate.query.filter_by(
        user_id=current_user.id,
        pos_subitem_id=item.pos_subitem_id
    ).first()

    if custom_template:
        # Use custom description
        description = custom_template.custom_description
    else:
        # Use default POS description
        description = item.pos_subitem.name
```

### When Saving Edits:

```python
# Save custom description to database
template = POSItemTemplate.query.filter_by(
    user_id=current_user.id,
    pos_subitem_id=item.pos_subitem_id
).first()

if template:
    template.custom_description = new_description
else:
    template = POSItemTemplate(
        user_id=current_user.id,
        pos_subitem_id=item.pos_subitem_id,
        custom_description=new_description,
        original_description=item.pos_subitem.name
    )
    db.session.add(template)

db.session.commit()
```

## User Interface

### In Contract View:

Each POS line item will have:
- **View mode**: Shows the description (custom or default)
- **Edit button**: Click to modify the description
- **Textarea**: Edit the description text
- **Save button**: Save to database as custom template
- **Cancel button**: Discard changes

### Visual Example:

```
┌─────────────────────────────────────────────┐
│ Electrical Work                             │
├─────────────────────────────────────────────┤
│ ☐ Install 200A panel: $2,500        [Edit] │
│                                             │
│ Description:                                │
│ Install 200A panel                          │
└─────────────────────────────────────────────┘

        ↓ (User clicks Edit)

┌─────────────────────────────────────────────┐
│ Electrical Work                             │
├─────────────────────────────────────────────┤
│ ☐ Install 200A panel: $2,500               │
│                                             │
│ Description:                                │
│ ┌─────────────────────────────────────────┐ │
│ │ Provide and install new 200-amp        │ │
│ │ electrical service panel with main     │ │
│ │ breaker, surge protection...           │ │
│ └─────────────────────────────────────────┘ │
│                                             │
│ [💾 Save] [❌ Cancel]                       │
└─────────────────────────────────────────────┘
```

## Use Cases

### 1. **Detailed Specifications**
**Default:** "Install plumbing fixtures"
**Custom:** "Provide and install Kohler K-596-VS Simplice kitchen faucet in vibrant stainless finish with pull-down sprayhead and DockNetik magnetic docking"

### 2. **Code Compliance**
**Default:** "Install GFCI outlets"
**Custom:** "Install tamper-resistant GFCI receptacles per NEC 210.8 requirements, with weather-resistant covers in all exterior and wet locations"

### 3. **Scope Clarification**
**Default:** "Tile installation"
**Custom:** "Provide and install 12x24 porcelain tile in running bond pattern, including thin-set mortar, waterproofing membrane, and unsanded grout. Does NOT include demolition, substrate prep, or tile material (owner-supplied)"

### 4. **Brand/Quality Standards**
**Default:** "Install insulation"
**Custom:** "Install Owens Corning R-19 EcoTouch Pink Fiberglass insulation in all exterior wall cavities, with proper compression fit and vapor barrier per manufacturer specifications"

## Integration with Contract Sections

Both systems work together:

```
Contract Structure:
├─ Section 3.4: ELECTRICAL WORK (editable template)
│   └─ Template text: "Contractor shall provide..."
│       ├─ POS Item 1: "Install panel..." (editable line item)
│       ├─ POS Item 2: "Install outlets..." (editable line item)
│       └─ POS Item 3: "Install lighting..." (editable line item)
```

**You can edit:**
- The section template (framework language)
- Individual line items (specific descriptions)

## Best Practices

### ✅ Start Generic, Get Specific
1. Use default POS descriptions initially
2. Customize as you review contracts
3. Add detail where it matters most
4. Build your library over time

### ✅ Focus on High-Value Items
- Customize expensive items first
- Add detail to frequently disputed items
- Clarify scope boundaries
- Specify quality standards

### ✅ Use Consistent Terminology
- Develop your standard phrases
- Use same terms across similar items
- Create templates for common work
- Maintain professional tone

### ✅ Include Key Details
- Brand/model numbers when relevant
- Code requirements
- Installation methods
- Exclusions/limitations
- Materials included vs. owner-supplied

## Resetting Descriptions

### To Reset a Single Item:
```python
# Delete the custom template
template = POSItemTemplate.query.filter_by(
    user_id=user_id,
    pos_subitem_id=subitem_id
).first()
db.session.delete(template)
db.session.commit()
```

### To Reset All Your Customizations:
```python
POSItemTemplate.query.filter_by(user_id=user_id).delete()
db.session.commit()
```

## Future Enhancements

- 📤 **Export/Import**: Share custom descriptions with team
- 🔄 **Version History**: Track changes to descriptions
- 📚 **Template Library**: Pre-built professional descriptions
- 🏷️ **Categories**: Organize custom descriptions by trade
- 🔍 **Search**: Find and reuse custom descriptions

---

**Your POS library, your way!** Combine editable contract sections with customizable line item descriptions to create the perfect contracts for your business.
