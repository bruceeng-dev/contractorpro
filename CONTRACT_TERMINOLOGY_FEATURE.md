# Contract Terminology Customization Feature

## Overview

ContractorPro now allows users to customize the contract language and terminology. When you edit any section of a contract, your changes are automatically saved as **your personal contract template**. The next time you generate a contract, it will use your customized terminology instead of the default language.

## How It Works

### 1. **Generate a Contract**
- Navigate to any job
- Click "View Contract"
- The system generates a comprehensive contract with individual editable sections

### 2. **Edit Contract Sections**
- Each section has an **"Edit" button**
- Click Edit to modify the language/terminology in that section
- Make your changes in the textarea
- Click **"Save"** to store your custom terminology

### 3. **Your Customizations Are Saved**
When you save a section:
- ✅ The current contract is updated
- ✅ Your custom terminology is **saved to the database** as a template
- ✅ Future contracts will **automatically use** your custom language for that section

### 4. **Generate Next Contract**
- Create a new quote and convert to contract
- Navigate to "View Contract"
- **Your custom terminology** is automatically used!
- The system replaces default text with your saved verbiage

## Example Workflow

### First Contract:
1. User generates contract for Kitchen Renovation
2. Sees default section: "## 3.4 Electrical Work (MEP)"
3. Default content: "Install new electrical panel, outlets, and lighting..."
4. User clicks **Edit** and changes to: "Provide comprehensive electrical system including updated panel, GFCI outlets, under-cabinet lighting..."
5. Clicks **Save**

### Second Contract:
1. User generates contract for Bathroom Renovation
2. Goes to "View Contract"
3. **Automatically sees their custom electrical section language!**
4. Section "## 3.4 Electrical Work (MEP)" shows: "Provide comprehensive electrical system including updated panel, GFCI outlets, under-cabinet lighting..."
5. No need to re-type - their custom terminology is now the default

## Features

### ✅ **Per-User Customization**
- Each user has their own contract templates
- User A's customizations don't affect User B's contracts
- Perfect for multi-user setups

### ✅ **Section-by-Section Control**
- Customize only the sections you want
- Leave other sections as default
- Mix and match custom and default language

### ✅ **Automatic Persistence**
- No "Save Template" button needed
- Every time you save a contract section, it becomes your template
- Future contracts automatically use your latest edits

### ✅ **Individual Section Editing**
- Each section (headings, content) can be edited separately
- Edit one section without affecting others
- Save sections individually or all at once

## Database Structure

The system stores custom terminology in the `contract_template` table:

```
ContractTemplate:
- id: Unique identifier
- user_id: Links to the user who created it
- section_id: Identifier for the section (e.g., "section_0", "section_3")
- section_title: The section heading (e.g., "3.4 Electrical Work (MEP)")
- section_content: Your custom verbiage/terminology
- section_type: "section" or "subsection"
- created_date: When first created
- updated_date: When last modified
```

## Technical Implementation

### When Viewing a Contract:

```python
# 1. Generate default contract from template
contract_text = generate_contract()

# 2. Parse into individual sections
sections = parse_contract_into_sections(contract_text)

# 3. Load user's custom templates
user_templates = ContractTemplate.query.filter_by(user_id=current_user.id).all()

# 4. Replace default content with user's custom terminology
for section in sections:
    if section['id'] in user_templates:
        section['content'] = user_templates[section['id']].content
```

### When Saving a Contract:

```python
# 1. Save contract to current job
contract.scope_of_work = json.dumps(sections)

# 2. Update/create user's contract templates
for section_id, section_data in sections.items():
    template = ContractTemplate.query.filter_by(
        user_id=current_user.id,
        section_id=section_id
    ).first()

    if template:
        template.section_content = section_data['content']
    else:
        new_template = ContractTemplate(
            user_id=current_user.id,
            section_id=section_id,
            section_content=section_data['content']
        )
        db.session.add(new_template)
```

## Benefits

### 🎯 **Consistency**
- Use the same language across all your contracts
- Maintain your company's standard terminology
- Ensure compliance with your preferred legal language

### ⏱️ **Time Savings**
- Edit once, use forever
- No need to manually update every contract
- Customizations persist automatically

### 📝 **Flexibility**
- Update specific sections without affecting others
- Gradually customize your contracts over time
- Easy to revert by re-editing and saving

### 🔒 **User-Specific**
- Each team member can have their own templates
- Different contractors can use different terminology
- Privacy between users

## Tips & Best Practices

### ✅ **Start with One Project**
1. Generate your first contract
2. Carefully edit the sections to match your preferences
3. Save each section
4. Future contracts will use this as the baseline

### ✅ **Iterative Improvement**
- Don't try to perfect everything at once
- Edit sections as you review contracts
- Refine over time based on client feedback

### ✅ **Legal Review**
- Have your attorney review your customized language
- Ensure your terminology is legally sound
- Update sections after legal consultation

### ✅ **Backup Your Templates**
- Export your contracts periodically
- Save copies of your finalized templates
- Consider documenting major terminology changes

## Resetting to Defaults

If you want to revert to default contract language:

### Option 1: Delete Specific Template
```python
# In Flask shell or custom script
from models import ContractTemplate, db
template = ContractTemplate.query.filter_by(
    user_id=your_user_id,
    section_id='section_3'  # The section to reset
).first()
db.session.delete(template)
db.session.commit()
```

### Option 2: Delete All Your Templates
```python
ContractTemplate.query.filter_by(user_id=your_user_id).delete()
db.session.commit()
```

### Option 3: Manual Override
- Simply edit the section again
- Replace with default text
- Save - this becomes your new template

## API Endpoints

### Save Contract Sections
```
POST /jobs/<job_id>/contract/save-comprehensive
Body: {
  "sections": {
    "section_0": {
      "id": "section_0",
      "title": "1. PARTIES TO THE AGREEMENT",
      "content": "Your custom content here...",
      "type": "section"
    },
    ...
  }
}
```

### View Contract (Loads Custom Templates Automatically)
```
GET /jobs/<job_id>/contract/view
```

## Future Enhancements

Potential improvements for this feature:

- 🎨 **Template Library**: Pre-built contract templates for different project types
- 📤 **Export/Import**: Share contract templates between users
- 📊 **Version History**: Track changes to contract language over time
- 🔄 **Template Marketplace**: Community-shared contract sections
- 🎓 **Legal Compliance Checker**: Validate terminology against legal standards

---

**Your contract language, your way!** The terminology customization feature gives you complete control over how your contracts read, while maintaining consistency across all your projects.
