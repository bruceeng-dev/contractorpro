# POS Quote System - Complete Workflow

**Last Updated:** March 2, 2026
**Status:** Active - This is the ONLY quote system

---

## 🎯 Overview

The **POS (Point of Sale) Multilayer Quote System** is the exclusive quoting system for ContractorPro. The old "Estimates" system has been deprecated and removed from the UI.

---

## 📋 Complete Workflow

### **Step 1: Create POS Quote**

**From Job Detail Page:**
1. Navigate to job: Jobs → Select Job
2. Scroll to "💰 Quotes" section
3. Click "+ Create Quote"
4. Redirects to POS Multilayer Builder

**From Sidebar:**
1. Click "Quote Builder"
2. Select job from dropdown (or leave blank for standalone quote)
3. Click "Manual (POS)" tab
4. Redirects to POS Multilayer Builder

**In POS Builder:**
- Select categories (Kitchen, Bathroom, Roofing, etc.)
- Add activities per category (Demolition, Framing, Electrical, etc.)
- Add sub-items with quantities and unit prices
- System calculates subtotal, tax, total automatically
- Save quote

---

### **Step 2: Review Quote**

**On POS Quote Detail Page:**
- View all line items organized by category
- See itemized costs with quantities
- Check subtotal, tax, and total
- Verify scope of work description
- Confirm client information

**Available Actions:**
- 📧 **Send to Client** - Email quote to client
- ✅ **Accept Quote** - Mark as accepted (contractor action)
- ❌ **Reject Quote** - Mark as rejected
- 📄 **Generate Contract** - Create formal contract from quote

---

### **Step 3: Send to Client**

**Process:**
1. Click "📧 Send to Client" button
2. Confirm action
3. System sends professional email to client with:
   - Quote summary
   - Itemized breakdown
   - Total amount
   - Link to accept/view quote (if enabled)

**Requirements:**
- Quote must be linked to a job
- Job must have client email address

**Status Change:** Draft → Sent

---

### **Step 4: Client Response**

**Option A: Client Accepts**
- Contractor clicks "✅ Accept Quote"
- Status changes: Sent → Accepted
- Ready for contract generation

**Option B: Client Rejects**
- Contractor clicks "❌ Reject Quote"
- Status changes: Sent → Rejected
- Can create revised quote

**Option C: Client Requests Changes**
- Edit quote in POS system
- Send updated version
- Repeat until accepted

---

### **Step 5: Generate Contract**

**After Quote Accepted:**
1. Click "📄 Generate Contract" (or "Accept & Generate Contract")
2. System creates formal construction contract with:
   - All quote line items integrated
   - Payment terms
   - Scope of work from quote
   - Standard terms & conditions
   - Signature blocks

**Contract Location:**
- Job Detail → Contract dropdown → View Contract
- Sidebar → Contracts → Find job contract

---

### **Step 6: Job Execution**

**Use Contract for:**
- Client signature
- Project scope reference
- Payment milestone tracking
- Change order baseline

**Quote remains linked:**
- View original quote anytime from job detail
- Reference for billing
- Track what was quoted vs. actual costs

---

## 🔄 Quote Statuses

| Status | Description | Next Actions |
|--------|-------------|--------------|
| **Draft** | Quote being built | Edit, Send to Client |
| **Sent** | Emailed to client | Accept, Reject, Edit |
| **Accepted** | Client approved | Generate Contract |
| **Rejected** | Client declined | Create new quote |
| ~~Converted~~ | ~~(Deprecated)~~ | ~~N/A - removed~~ |

---

## ✅ What You CAN Do with POS Quotes

1. ✅ Create detailed multi-category quotes
2. ✅ Email quotes to clients
3. ✅ Accept/reject quotes
4. ✅ Generate contracts from quotes
5. ✅ Link quotes to jobs
6. ✅ Track quote history per job
7. ✅ Calculate automatic totals with tax
8. ✅ Organize items by room/location
9. ✅ Add custom activities and sub-items
10. ✅ Send professional formatted quotes

---

## ❌ What You CANNOT Do (Removed Features)

1. ❌ ~~Convert to old-style Estimate~~ - REMOVED
2. ❌ ~~Create Quick Estimates~~ - Use POS instead
3. ❌ ~~Use template-based estimates~~ - POS is more detailed
4. ❌ ~~Mix POS and Estimate systems~~ - POS only now

---

## 🎨 POS Quote Structure

```
POS Quote
├── Header
│   ├── Quote Number (auto-generated)
│   ├── Client Name
│   ├── Job Link (optional)
│   ├── Created Date
│   └── Status Badge
│
├── Scope of Work (text description)
│
├── Line Items (organized by category)
│   ├── Category 1: Kitchen
│   │   ├── Activity: Demolition
│   │   │   ├── Sub-item: Remove cabinets (qty × price)
│   │   │   └── Sub-item: Disposal fees (qty × price)
│   │   └── Activity: Installation
│   │       ├── Sub-item: New cabinets (qty × price)
│   │       └── Sub-item: Labor hours (qty × price)
│   │
│   └── Category 2: Bathroom
│       └── (same structure)
│
├── Calculations
│   ├── Subtotal (sum of all items)
│   ├── Tax (if applicable)
│   └── Total
│
└── Actions
    ├── Send to Client
    ├── Accept Quote
    ├── Reject Quote
    └── Generate Contract
```

---

## 💡 Best Practices

### Creating Quotes:
1. **Be specific** - Include exact quantities and materials
2. **Use categories** - Organize by room or trade for clarity
3. **Add descriptions** - Note specifications in scope of work
4. **Check totals** - Review calculations before sending
5. **Link to job** - Always associate with a job if possible

### Sending to Clients:
1. **Review first** - Double-check all details
2. **Professional language** - Use scope description for overview
3. **Clear breakdown** - Organize logically by room/area
4. **Follow up** - Track when sent, follow up if no response

### After Acceptance:
1. **Generate contract ASAP** - Lock in terms
2. **Get signature** - Physical or digital
3. **Track progress** - Use contract as baseline
4. **Document changes** - Use change orders for variations

---

## 🔧 Technical Details

### Database Tables:
- **`pos_quote`** - Main quote record
- **`pos_category`** - Categories (Kitchen, Bathroom, etc.)
- **`pos_activity`** - Activities per category (Demolition, Framing, etc.)
- **`pos_subitem`** - Line items with quantities and prices
- **`pos_session`** - Draft sessions before saving

### API Endpoints:
```
POST   /api/pos/session/<token>/save-quote    - Save POS quote
POST   /api/pos/quotes/<id>/send-to-client    - Email quote
POST   /api/pos/quotes/<id>/accept            - Mark accepted
POST   /api/pos/quotes/<id>/reject            - Mark rejected
POST   /api/pos/quotes/<id>/accept-and-contract - Accept + generate contract
GET    /api/jobs/<id>/pos-quotes              - Get quotes for job
```

### Routes:
```
/pos/multilayer                - POS builder interface
/pos/quotes                    - List all quotes
/pos/quotes/<id>               - Quote detail page
```

---

## 📊 Reporting & Analytics

### Available Data:
- Total quotes created
- Acceptance rate (accepted / sent)
- Average quote value
- Quotes by category
- Quotes by job
- Quote turnaround time (created → sent → accepted)

### Future Enhancements:
- Quote comparison (multiple quotes per job)
- Win/loss analysis
- Category profitability tracking
- Material cost trending

---

## 🚀 Advantages Over Old Estimate System

| Feature | POS Quotes | Old Estimates |
|---------|------------|---------------|
| Detail Level | High (category → activity → sub-items) | Low (just line items) |
| Organization | Structured by room/trade | Flat list |
| Calculations | Automatic per level | Manual only |
| Client View | Professional categorized | Simple list |
| Integration | Direct to contract | Required conversion |
| Flexibility | Add unlimited items | Limited structure |
| Scope Clarity | Built-in descriptions | Separate notes |
| Change Tracking | Category-based | Line-by-line only |

---

## 📞 Support & Training

**For Users:**
- Hover tooltips in POS builder explain each field
- Category suggestions based on job type
- Auto-save prevents data loss
- Undo/redo for mistakes

**For Admins:**
- Configure default categories via POS admin
- Set tax rates per jurisdiction
- Customize contract templates
- Set up email templates for quotes

---

## 🎯 Summary

**POS Quote System** is your complete solution for:
1. Creating detailed, professional quotes
2. Sending to clients via email
3. Tracking acceptance/rejection
4. Generating formal contracts
5. Managing project scope

**No conversion needed.** No duplicate systems. Just one clean workflow from quote to contract to job completion.

---

**Questions?** Check the [User Manual](docs/USER_MANUAL.md) or [API Documentation](docs/API_DOCUMENTATION.md)

**Need Help?** The POS system is designed to be intuitive - just start building a quote and explore!
