# Testing Guide - Navigation & Feature Improvements

## 🚀 Quick Start Testing

### 1. Start the Application
```bash
cd c:\Users\RLESo\Downloads\Website_Test_Folder
python app.py
```

Access at: `http://localhost:5000`

---

## ✅ Testing Checklist

### **Navigation Tests**

#### Sidebar Navigation
- [ ] Click "Dashboard" → Loads dashboard
- [ ] Click "Jobs" → Shows job list
- [ ] Click "Leads" → Shows leads
- [ ] Click "Schedule" (renamed from Calendar) → Shows calendar
- [ ] Click "Reports" → Shows reports
- [ ] Click "Quote Builder" → Opens unified quote builder
- [ ] Click "Contracts" → Shows contracts list
- [ ] Click "Templates" → Shows task templates
- [ ] Click "Documents" → Shows documents

**Expected:** All links work, no 404 errors

#### Job Detail Actions
1. Go to Jobs → Click any job
2. Check action buttons:
   - [ ] "← Back" → Returns to jobs list
   - [ ] "Create Quote" → Opens quote builder with job pre-selected
   - [ ] "Contract ▼" dropdown:
     - [ ] Click dropdown → Menu appears
     - [ ] "View Contract" → Opens contract in view mode
     - [ ] "Edit Contract" → Opens contract in edit mode
     - [ ] "Generate with AI" → Opens AI generator
     - [ ] "Download PDF" → Initiates PDF download
     - [ ] Click outside → Dropdown closes
   - [ ] "Schedule" → Opens calendar filtered to this job

**Expected:** All buttons work, dropdown opens/closes smoothly

---

### **Quote Builder Tests**

#### Access Quote Builder
1. **From Sidebar:**
   - Click "Quote Builder" in Tools section
   - [ ] Opens with AI tab active by default

2. **From Job Detail:**
   - Click "Create Quote" button
   - [ ] Opens with job pre-selected

#### Tab Navigation
- [ ] Click "AI Quote" tab → Shows AI interface
- [ ] Click "Manual (POS)" tab → Redirects to POS multilayer
- [ ] Click "Quick Estimate" tab → Redirects to new estimate form

#### AI Quote Builder (if OpenAI configured)
- [ ] Job dropdown shows all jobs
- [ ] Select job → Shows "Quote for: [Client Name]"
- [ ] Type in chat box → Text accepts input
- [ ] Click suggestion chip → Fills input with sample text
- [ ] Click "Generate Quote" → Shows loading spinner
- [ ] If no API key → Shows warning message with setup instructions

**Expected:** Tabs switch correctly, redirects work, UI is responsive

---

### **Contract Management Tests**

#### Contracts List
1. Go to Sidebar → Contracts
2. **If you have contracts:**
   - [ ] Shows grid of contract cards
   - [ ] Each card shows: Client name, project type, contract #, value, created date
   - [ ] Status badge displays correctly
   - [ ] "View" button → Opens contract in view mode
   - [ ] "Edit" button → Opens contract in edit mode
   - [ ] "Job Details" button → Goes to job detail page

3. **If no contracts:**
   - [ ] Shows empty state with icon
   - [ ] "View Jobs" button works
   - [ ] "Create Quote" button works

#### Unified Contract Interface
1. Go to Job Detail → Contract dropdown → View Contract
2. **View Mode:**
   - [ ] Shows formatted contract document
   - [ ] Mode tabs at top: View (active) | Edit | AI
   - [ ] Print button works
   - [ ] Download PDF button (placeholder for now)
   - [ ] Contract displays: parties, project description, scope, payment terms, signatures

3. Switch to **Edit Mode:**
   - [ ] Mode tab updates (Edit becomes active)
   - [ ] Shows location & task management interface
   - [ ] "Add Location" button → Form appears
   - [ ] Can add location (submits to existing route)
   - [ ] "Add Task" button → Modal appears
   - [ ] Modal has close button and form
   - [ ] Click outside modal → Modal closes

4. Switch to **AI Mode:**
   - [ ] Mode tab updates (AI becomes active)
   - [ ] If OpenAI available: Shows scope input form
   - [ ] If not available: Shows warning with setup instructions
   - [ ] Checkboxes for "generate tasks" and "include POS quotes"
   - [ ] "Generate Contract with AI" button present

**Expected:** Mode switching works, all forms functional, no errors

---

### **Route Tests**

Test these URLs directly:

#### Quote Builder Routes
```
http://localhost:5000/quotes/builder
http://localhost:5000/quotes/builder?mode=ai
http://localhost:5000/quotes/builder?mode=ai&job_id=1
```
**Expected:** Loads quote builder, tabs work, job pre-selection works

#### Contract Routes
```
http://localhost:5000/contracts
http://localhost:5000/jobs/1/contract
http://localhost:5000/jobs/1/contract?mode=view
http://localhost:5000/jobs/1/contract?mode=edit
http://localhost:5000/jobs/1/contract?mode=ai
```
**Expected:** All routes load without 404 errors

#### Legacy Routes (should still work)
```
http://localhost:5000/jobs/1/contract/legacy
http://localhost:5000/pos/multilayer
http://localhost:5000/estimates/new
```
**Expected:** Backward compatibility maintained

---

### **Mobile Responsiveness Tests**

#### Test at Different Widths
1. Desktop (1920px):
   - [ ] Tabs display in horizontal row
   - [ ] Contract cards in 2-3 column grid
   - [ ] Dropdown menus align correctly

2. Tablet (768px):
   - [ ] Tabs remain horizontal
   - [ ] Cards adjust to 2 columns
   - [ ] Sidebar toggle works

3. Mobile (375px):
   - [ ] Tabs stack vertically
   - [ ] Cards show in single column
   - [ ] Text remains readable
   - [ ] Buttons don't overlap

**How to Test:**
- Chrome DevTools → Toggle device toolbar (Ctrl+Shift+M)
- Test on: iPhone SE, iPad, Desktop

---

### **JavaScript Functionality Tests**

#### Dropdown Menu
```javascript
// Contract dropdown in job_detail.html
- Click contract button → Dropdown appears
- Click again → Dropdown disappears
- Click outside → Dropdown closes
```

#### Modal Windows
```javascript
// Task modal in contract edit mode
- Click "Add Task" → Modal opens
- Click "×" close button → Modal closes
- Click outside modal → Modal closes
- Press Escape key → Modal closes (if implemented)
```

#### Form Validation
- [ ] Try submitting empty scope in AI generator → Shows HTML5 validation
- [ ] Try submitting task without name → Shows validation
- [ ] All required fields marked with * or required attribute

---

## 🐛 Common Issues & Solutions

### Issue: "Route not found" (404 Error)

**Symptom:** Clicking link shows 404
**Check:**
1. Is Flask app running?
2. Did you restart app after adding new routes?
3. Check `app.py` for typos in route decorator

**Fix:**
```bash
# Restart Flask app
Ctrl+C  # Stop current instance
python app.py  # Start fresh
```

---

### Issue: "TemplateNotFound" Error

**Symptom:** `jinja2.exceptions.TemplateNotFound: unified_contract.html`
**Fix:**
1. Verify all templates created in `templates/` folder
2. Check filename spelling exactly matches `render_template()` call
3. Restart Flask app

---

### Issue: Dropdown Menu Doesn't Close

**Symptom:** Click outside dropdown, menu stays open
**Check:**
1. Inspect browser console for JavaScript errors
2. Verify script at bottom of `job_detail.html` loaded
3. Check no other click handlers interfering

**Fix:**
```javascript
// Add this at bottom of job_detail.html if missing:
document.addEventListener('click', function() {
  document.querySelectorAll('.contract-dropdown').forEach(d => d.style.display = 'none');
});
```

---

### Issue: AI Features Show "Not Available"

**Symptom:** AI modes show warning message
**This is expected if:**
- OpenAI library not installed
- No API key in `.env` file

**To Enable:**
```bash
pip install openai
```

Add to `.env`:
```
OPENAI_API_KEY=sk-your-key-here
```

Restart app.

---

### Issue: Styles Not Loading

**Symptom:** Pages look unstyled
**Check:**
1. `static/css/styles.css` exists
2. Browser console shows no 404 for CSS file
3. Hard refresh browser (Ctrl+F5)

**Fix:**
```bash
# Clear browser cache
Ctrl+Shift+Delete → Clear cache

# Or hard reload
Ctrl+F5
```

---

## 📊 Database Tests

### Required Tables
Verify these tables exist:
```sql
SELECT name FROM sqlite_master WHERE type='table';
```

**Expected tables:**
- jobs
- contracts
- pos_quotes
- tasks
- job_locations
- users

### Test Data
Create test job if needed:
```python
python migrate.py seed
```

---

## 🧪 Automated Testing (Optional)

Create `test_navigation.py`:
```python
import unittest
from app import create_app

class NavigationTests(unittest.TestCase):
    def setUp(self):
        self.app, _, _ = create_app('testing')
        self.client = self.app.test_client()

    def test_quote_builder_loads(self):
        response = self.client.get('/quotes/builder')
        self.assertEqual(response.status_code, 200)

    def test_contracts_list_loads(self):
        response = self.client.get('/contracts')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
```

Run:
```bash
python test_navigation.py
```

---

## ✅ Final Verification

### Before Deployment
- [ ] All routes tested manually
- [ ] No 404 errors
- [ ] No JavaScript console errors
- [ ] Mobile layout works
- [ ] Database migrations run
- [ ] Environment variables set
- [ ] Static files serving correctly

### Performance Checks
- [ ] Pages load in < 2 seconds
- [ ] No N+1 query issues
- [ ] Images optimized
- [ ] CSS/JS minified (for production)

---

## 📝 Test Results Template

```
Date: __________
Tester: __________

✅ PASS  |  ❌ FAIL  |  ⚠️ ISSUE

Navigation:
[ ] Sidebar links
[ ] Job detail actions
[ ] Dropdown menus

Routes:
[ ] Quote builder
[ ] Contracts list
[ ] Unified contract

UI/UX:
[ ] Mobile responsive
[ ] Modals work
[ ] Tabs switch

Issues Found:
1. _______________
2. _______________

Notes:
_______________
```

---

## 🎯 Priority Test Scenarios

### **Scenario 1: Create Quote for New Job**
1. Login
2. Sidebar → Jobs → New Job
3. Fill form → Save
4. Click "Create Quote"
5. Choose AI tab
6. Enter scope
7. Generate quote

**Expected:** Full flow works end-to-end

### **Scenario 2: View Existing Contract**
1. Login
2. Sidebar → Contracts
3. Click any contract "View" button
4. Review contract document
5. Click "Edit" tab
6. Add a task
7. Click "View" tab
8. Verify task appears in contract

**Expected:** Data persists, mode switching works

### **Scenario 3: Mobile Job Management**
1. Open on phone/tablet
2. Navigate to job detail
3. Click contract dropdown
4. Select "View Contract"
5. Scroll through contract
6. Return to job

**Expected:** Touch targets large enough, text readable

---

## 🚀 Next Steps After Testing

1. **If tests pass:**
   - Proceed to Phase 4 enhancements (Dashboard KPIs, Calendar improvements)
   - Deploy to staging environment
   - User acceptance testing

2. **If tests fail:**
   - Document failures
   - Fix issues one by one
   - Retest after each fix
   - Check [NAVIGATION_IMPROVEMENTS_SUMMARY.md](NAVIGATION_IMPROVEMENTS_SUMMARY.md) for implementation details

---

## 📞 Support

**Documentation:**
- `NAVIGATION_IMPROVEMENTS_SUMMARY.md` - What changed
- `CLAUDE.md` - Project overview
- `SETUP.md` - Installation guide

**Need Help?**
Check Flask logs:
```bash
# In terminal where app is running
# Errors will print to console
```

Check browser console:
```
F12 → Console tab
Look for red error messages
```

---

**Happy Testing!** 🎉
