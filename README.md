# ContractorPro 🏗️

> **Intelligent Construction Business Automation Platform**

A comprehensive web application designed for general contractors to automate and streamline their business operations. Features advanced workflow automation, photo-based progress tracking, POS quote system, template-driven estimating, and intelligent contract generation.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/flask-3.0+-green.svg)](https://flask.palletsprojects.com/)

## 🚀 Quick Deploy

Deploy ContractorPro to the cloud in one click:

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/contractorpro?referralCode=bruceeng-dev)

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/bruceeng-dev/contractorpro)

---

## ✨ Features

### 📊 Smart Estimating & Quoting
- **Multi-layer POS Quote System** with hierarchical categories, activities, and line items
- **Template-based estimates** with pre-built calculations for Kitchen, Bathroom, Addition, Roofing projects
- **Real-time cost calculations** with automatic overhead and profit margin calculations
- **Professional quote delivery** via automated email system
- **Detailed line item management** for comprehensive project breakdowns

### 📝 Intelligent Contract Generation
- **AI-powered contract creation** with OpenAI integration (optional)
- **Verbose contract templates** with detailed POS quote breakdown
- **Automatic scope generation** from quote line items
- **Contract versioning** with edit and view modes
- **Professional formatting** with materials, specifications, and exclusions

### 📷 Photo-Based Progress Tracking
- **Automated milestone notifications** to clients when progress photos are uploaded
- **Visual project timeline** with before/during/after photo categorization
- **Location-based photo organization** for easy project documentation
- **Percentage completion tracking** with client update automation

### 📧 Automated Client Communication
- **Automated milestone emails** when project phases are completed
- **Professional estimate delivery** with tracking and status updates
- **Email notification logging** for complete communication audit trail
- **Template-based messaging** for consistent professional communication

### 📅 Advanced Project Management
- **Interactive Gantt charts** with drag-and-drop task scheduling
- **Calendar view** with task dependencies and critical path analysis
- **Task templates** for common project types
- **Real-time progress tracking** with KPI dashboard

### 🔐 Enterprise Authentication
- **Secure user management** with password hashing and session control
- **Multi-user support** with user-specific data isolation
- **Registration system** for team member access

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/bruceeng-dev/contractorpro.git
   cd contractorpro
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv

   # On Windows
   venv\Scripts\activate

   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Copy the example file
   cp .env.example .env

   # Edit .env and update the values
   # Minimum required: SECRET_KEY
   ```

5. **Initialize the database**
   ```bash
   python migrate.py init
   ```

6. **Run the application**
   ```bash
   python app.py
   ```

7. **Access the application**
   - Open your browser to `http://localhost:5000`
   - Login with default credentials:
     - Username: `admin`
     - Password: `admin123`

---

## 📖 Usage

### Creating a Quote

1. Navigate to **Jobs** → **New Job**
2. Fill in client and project details
3. Click **Create Quote** → **Build Quote**
4. Select categories, activities, and line items
5. Review totals and click **Create Quote**
6. Accept quote to automatically generate contract

### Generating a Contract

1. From a job detail page, click **Create Quote**
2. Build and save your quote
3. Click **Accept Quote & Generate Contract**
4. Contract is automatically created with:
   - Project overview
   - Detailed scope from POS quote
   - Payment terms
   - Terms & conditions
   - Exclusions

### Managing Tasks

1. Navigate to job detail page
2. View **Calendar** or **Gantt Chart**
3. Add tasks manually or auto-generate from contract
4. Track progress with percentage completion
5. Upload progress photos to update clients automatically

---

## 🔧 Configuration

### Environment Variables

```bash
# Core Settings
SECRET_KEY=your-secret-key-here
FLASK_ENV=development
DEBUG=True

# Database (SQLite for dev, PostgreSQL for production)
DATABASE_URL=sqlite:///contractorpro.db

# Email Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# OpenAI Integration (optional)
OPENAI_API_KEY=your-openai-api-key
```

### Database Migrations

```bash
# Initialize fresh database
python migrate.py init

# Add sample data for testing
python migrate.py seed

# Run migrations (for schema updates)
python migrate.py migrate

# Reset database (WARNING: deletes all data)
python migrate.py reset
```

---

## 🌐 Deployment

### Deploy to Render (Recommended)

1. **Create account** at [render.com](https://render.com)

2. **Create New Web Service**
   - Connect your GitHub repository
   - Select `Python 3` environment

3. **Configure Settings**
   ```
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn app:app
   ```

4. **Add Environment Variables**
   - `SECRET_KEY`: Generate a secure random key
   - `DATABASE_URL`: Use Render's PostgreSQL add-on
   - `FLASK_ENV`: production
   - Add email and OpenAI keys as needed

5. **Deploy** - Render will automatically deploy on push to main branch

### Deploy to Railway

1. **Create account** at [railway.app](https://railway.app)
2. **New Project** → **Deploy from GitHub repo**
3. **Add PostgreSQL** database from Railway marketplace
4. **Add environment variables** (same as above)
5. **Deploy**

### Deploy to Heroku

```bash
# Install Heroku CLI
# Login to Heroku
heroku login

# Create new app
heroku create your-app-name

# Add PostgreSQL
heroku addons:create heroku-postgresql:mini

# Set environment variables
heroku config:set SECRET_KEY=your-secret-key
heroku config:set FLASK_ENV=production

# Deploy
git push heroku main

# Initialize database
heroku run python migrate.py init
```

---

## 📂 Project Structure

```
contractorpro/
├── app.py                          # Main Flask application
├── models.py                       # SQLAlchemy database models
├── config.py                       # Application configuration
├── migrate.py                      # Database migration utility
├── llm_contract_service.py         # AI contract generation service
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
├── static/
│   └── css/
│       └── styles.css              # Application styling
├── templates/                      # Jinja2 HTML templates
│   ├── base.html
│   ├── dashboard.html
│   ├── jobs.html
│   ├── pos_multilayer.html         # POS quote builder
│   ├── unified_contract.html       # Contract interface
│   └── ...
├── uploads/                        # User-uploaded files (gitignored)
│   ├── photos/
│   └── documents/
└── docs/                           # Comprehensive documentation
    ├── USER_MANUAL.md
    ├── API_DOCUMENTATION.md
    └── ...
```

---

## 🛠️ Tech Stack

- **Backend**: Flask 3.0, Python 3.8+
- **Database**: SQLAlchemy ORM (SQLite/PostgreSQL)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Authentication**: Flask-Login
- **Email**: Flask-Mail
- **AI Integration**: OpenAI API (optional)
- **Charts**: Chart.js, FullCalendar

---

## 📚 Documentation

- [User Manual](docs/USER_MANUAL.md) - Complete guide for contractors
- [API Documentation](docs/API_DOCUMENTATION.md) - REST API reference
- [Database Schema](docs/DATABASE_SCHEMA.md) - Database design
- [Deployment Guide](docs/DEPLOYMENT_GUIDE.md) - Production setup
- [Docker Setup](DOCKER_SETUP.md) - Containerized deployment

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Built with [Flask](https://flask.palletsprojects.com/)
- UI inspired by modern construction management tools
- Contract templates based on industry standards

---

## 📞 Support

- 📧 Email: support@contractorpro.com
- 🐛 Issues: [GitHub Issues](https://github.com/bruceeng-dev/contractorpro/issues)
- 📖 Documentation: [GitHub Wiki](https://github.com/bruceeng-dev/contractorpro/wiki)

---

## 🔮 Roadmap

- [ ] Mobile app (iOS/Android)
- [ ] Advanced reporting and analytics
- [ ] Integration with QuickBooks
- [ ] Customer portal for real-time updates
- [ ] Multi-language support
- [ ] AI-powered bid optimization

---

**Made with ❤️ for contractors, by contractors**
