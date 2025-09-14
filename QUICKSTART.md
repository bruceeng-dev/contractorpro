# ContractorPro Quick Start

Get ContractorPro running in under 5 minutes with the automated installer.

## One-Command Installation

```bash
python install.py
```

This installer will:
- ✅ Check Python version (3.8+ required)
- 📁 Create necessary directories
- 📦 Install all dependencies
- 🗄️ Initialize the database
- 📊 Optionally add sample data

## Manual Installation

If you prefer manual setup:

```bash
# Install dependencies
pip install -r requirements.txt

# Create directories
mkdir uploads uploads/photos uploads/documents logs

# Initialize database
python migrate.py init

# Add sample data (optional)
python migrate.py seed

# Run application
python app.py
```

## First Login

1. Open http://localhost:5000
2. Click "Register" to create your account
3. Or use sample account: `admin` / `admin123`

## Core Workflows

### 1. Create Your First Job
- Dashboard → "New Job"
- Fill in client details and project info
- Set budget and timeline

### 2. Upload Progress Photos
- Open any job → "Photos" tab
- Upload photos with milestone percentages
- Clients get automatic email notifications

### 3. Generate Estimates
- "Estimates" → "New Estimate"
- Use templates for common project types
- Add line items with automatic calculations
- Email directly to clients

### 4. Manage Leads
- "Leads" → "New Lead"
- Track prospects and follow-up dates
- Convert leads to jobs when won

## Key Features Ready to Use

- 🔐 **Secure Login** - Your data is protected
- 📊 **Smart Estimates** - Templates with auto-calculations
- 📷 **Photo Progress** - Visual milestone tracking
- 📧 **Email Automation** - Client notifications
- 💰 **Budget Tracking** - Real-time cost monitoring

## Configuration

Edit `.env` file for:
- Email settings (for notifications)
- Database configuration
- Upload limits

## Need Help?

- Full documentation: `SETUP.md`
- User guide: `docs/USER_MANUAL.md`
- Troubleshooting: Check logs in `/logs` folder

---

**You're ready to start managing projects like a pro!** 🚀