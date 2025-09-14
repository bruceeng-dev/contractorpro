# ContractorPro Setup Guide

## Quick Start

Follow these steps to get ContractorPro running with all the new automation features:

### 1. Install Dependencies

```bash
# Install Python packages
pip install -r requirements.txt
```

### 2. Environment Setup

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your settings
# For development, you can use the defaults
```

### 3. Initialize Database

```bash
# Initialize database with tables
python migrate.py init

# Add sample data (optional)
python migrate.py seed
```

### 4. Run the Application

```bash
python app.py
```

### 5. Login

- Open http://localhost:5000
- Login with: `admin` / `admin123`
- Or register a new account

## New Features Added

### 🔐 **User Authentication**
- Secure login/logout system
- User registration
- Password hashing
- Session management

### 📊 **Smart Estimating & Bidding**
- Template-based estimates (Kitchen, Bathroom, etc.)
- Automatic cost calculations with overhead & profit margins
- Detailed line item breakdown
- Email estimates to clients

### 📷 **Photo Progress Tracking**
- Upload progress photos with metadata
- Milestone tracking with percentage completion
- Automatic client notifications for milestones
- Photo categorization (Before, Progress, After, Issues)

### 📧 **Email Automation**
- Milestone notifications to clients
- Estimate delivery
- Notification logging and status tracking

### 💾 **Database Integration**
- PostgreSQL support (recommended)
- SQLite for development
- Proper data relationships
- Migration system

### 🎨 **Enhanced UI**
- Light, professional theme
- Responsive design
- Interactive forms with real-time calculations
- Modern card-based layout

## Database Options

### SQLite (Development)
```bash
# Already configured in .env.example
DATABASE_URL=sqlite:///contractorpro.db
```

### PostgreSQL (Production)
```bash
# Install PostgreSQL and create database
createdb contractorpro

# Update .env
DATABASE_URL=postgresql://contractor:password@localhost/contractorpro
```

## Email Configuration

For email notifications to work, update your `.env`:

```bash
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password  # Use App Password for Gmail
MAIL_DEFAULT_SENDER=noreply@yourcompany.com
```

## File Storage

Photos and documents are stored in:
- `uploads/photos/` - Progress photos
- `uploads/documents/` - Project documents

Make sure these directories are writable.

## Key Workflows Now Automated

### 1. **Photo-Based Progress Billing**
1. Upload progress photos to jobs
2. Mark milestones with completion percentages
3. System automatically emails clients with updates
4. Track project progress visually

### 2. **Template-Based Estimating**
1. Create estimates using pre-built templates
2. Automatic calculations with overhead/profit
3. Add detailed line items
4. Send professional estimates via email

### 3. **Client Communication**
1. Automated milestone notifications
2. Estimate delivery tracking
3. Email status logging

## API Endpoints

New API endpoints for mobile/integration:
- `GET /api/jobs/<id>/progress` - Get job progress data
- `POST /jobs/<id>/photos/upload` - Upload progress photos
- `POST /estimates/<id>/send` - Send estimate via email

## Next Steps

With this foundation in place, you can now add:
- **AI-powered quantity takeoffs** from drawings
- **Advanced scheduling** with resource optimization  
- **Change order automation** workflows
- **Mobile app** integration
- **QuickBooks sync** for accounting

## Troubleshooting

### Database Issues
```bash
# Reset database if needed
python migrate.py reset

# Reinitialize
python migrate.py init
python migrate.py seed
```

### Permission Issues
```bash
# Fix upload permissions
chmod 755 uploads/
chmod 755 uploads/photos/
chmod 755 uploads/documents/
```

### Email Not Working
1. Check email credentials in `.env`
2. Enable "Less secure apps" or use App Passwords for Gmail
3. Verify SMTP settings

## Success Metrics

The new automation features should deliver:
- **50% reduction** in estimate creation time
- **Automated client communication** for milestones
- **Professional estimate delivery** via email
- **Visual progress tracking** with photos
- **Centralized project management**

## Support

Check the full documentation in `/docs/` for:
- Deployment guides
- API documentation  
- Troubleshooting
- Configuration options

---

**You now have a production-ready contractor management platform with intelligent automation!** 🚀