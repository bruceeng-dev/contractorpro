# ContractorPro Configuration Documentation

## Overview

This document covers all configuration options available in ContractorPro, including environment variables, application settings, feature flags, and customization options.

## Environment Variables

### Core Application Settings

```bash
# Application Environment
FLASK_ENV=development|production|testing
DEBUG=True|False
SECRET_KEY=your-secret-key-here

# Server Configuration
HOST=0.0.0.0                    # Default: 127.0.0.1
PORT=5000                       # Default: 5000
WORKERS=2                       # Gunicorn worker processes (production)
```

### Database Configuration

```bash
# PostgreSQL (Recommended)
DATABASE_URL=postgresql://user:password@host:port/database

# MySQL Alternative
DATABASE_URL=mysql://user:password@host:port/database

# SQLite (Development only)
DATABASE_URL=sqlite:///contractorpro.db

# Connection Pool Settings
DB_POOL_SIZE=5                  # Maximum connections in pool
DB_POOL_TIMEOUT=30              # Connection timeout in seconds
DB_POOL_RECYCLE=3600            # Connection recycle time
```

### File Upload Settings

```bash
# Upload Configuration
UPLOAD_FOLDER=./uploads         # Directory for file uploads
MAX_CONTENT_LENGTH=52428800     # Max file size: 50MB
ALLOWED_EXTENSIONS=pdf,jpg,jpeg,png,gif,doc,docx,xls,xlsx,dwg

# Cloud Storage (Optional)
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_BUCKET_NAME=contractorpro-uploads
AWS_REGION=us-east-1

# Azure Blob Storage Alternative
AZURE_STORAGE_CONNECTION_STRING=your-connection-string
AZURE_CONTAINER_NAME=uploads
```

### Email Configuration

```bash
# SMTP Settings
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USE_SSL=False
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=noreply@contractorpro.com

# Email Templates
SEND_WELCOME_EMAIL=True
SEND_JOB_NOTIFICATIONS=True
SEND_INVOICE_REMINDERS=True
```

### Security Settings

```bash
# Authentication
SESSION_TIMEOUT=3600            # Session timeout in seconds
PASSWORD_MIN_LENGTH=8
REQUIRE_EMAIL_VERIFICATION=True
MAX_LOGIN_ATTEMPTS=5

# CSRF Protection
WTF_CSRF_ENABLED=True
WTF_CSRF_TIME_LIMIT=3600

# Rate Limiting
RATELIMIT_STORAGE_URL=redis://localhost:6379
RATELIMIT_ENABLED=True
API_RATE_LIMIT=100              # Requests per minute
```

### Third-Party Integrations

```bash
# Google Maps API
GOOGLE_MAPS_API_KEY=your-maps-api-key
ENABLE_MAPS=True

# Stripe Payment Processing
STRIPE_PUBLISHABLE_KEY=pk_live_or_test_key
STRIPE_SECRET_KEY=sk_live_or_test_key
STRIPE_WEBHOOK_SECRET=whsec_webhook_secret

# QuickBooks Integration
QB_CLIENT_ID=your-quickbooks-client-id
QB_CLIENT_SECRET=your-quickbooks-client-secret
QB_REDIRECT_URI=https://yourdomain.com/auth/quickbooks

# Sentry Error Monitoring
SENTRY_DSN=https://your-sentry-dsn@sentry.io/project-id
SENTRY_ENVIRONMENT=production
```

### Caching Configuration

```bash
# Redis Cache
CACHE_TYPE=redis
CACHE_REDIS_URL=redis://localhost:6379/0
CACHE_DEFAULT_TIMEOUT=300

# Simple Cache (Development)
CACHE_TYPE=simple
CACHE_DEFAULT_TIMEOUT=300

# Filesystem Cache
CACHE_TYPE=filesystem
CACHE_DIR=./cache
```

## Application Configuration

### Feature Flags

Create `config/features.py`:
```python
class FeatureFlags:
    # Core Features
    ENABLE_JOB_MANAGEMENT = True
    ENABLE_LEAD_MANAGEMENT = True
    ENABLE_DOCUMENT_MANAGEMENT = True
    ENABLE_REPORTING = True
    
    # Advanced Features
    ENABLE_MOBILE_APP = False
    ENABLE_CUSTOMER_PORTAL = False
    ENABLE_SUBCONTRACTOR_MANAGEMENT = False
    ENABLE_INVENTORY_TRACKING = False
    
    # Integrations
    ENABLE_QUICKBOOKS_SYNC = False
    ENABLE_STRIPE_PAYMENTS = False
    ENABLE_SMS_NOTIFICATIONS = False
    ENABLE_CALENDAR_SYNC = False
    
    # Beta Features
    ENABLE_AI_ESTIMATES = False
    ENABLE_3D_MODELS = False
    ENABLE_DRONE_INTEGRATION = False
```

### Business Logic Configuration

Create `config/business.py`:
```python
class BusinessConfig:
    # Job Management
    DEFAULT_JOB_STATUS = 'pending'
    JOB_STATUSES = ['pending', 'active', 'completed', 'cancelled', 'on_hold']
    AUTO_ARCHIVE_COMPLETED_JOBS = True
    ARCHIVE_AFTER_DAYS = 365
    
    # Lead Management
    DEFAULT_LEAD_STATUS = 'new'
    LEAD_STATUSES = ['new', 'contacted', 'qualified', 'quoted', 'won', 'lost', 'nurturing']
    AUTO_FOLLOW_UP_DAYS = 7
    LEAD_EXPIRY_DAYS = 90
    
    # Financial Settings
    DEFAULT_TAX_RATE = 0.08  # 8%
    INVOICE_PAYMENT_TERMS = 30  # NET 30
    LATE_FEE_PERCENTAGE = 0.015  # 1.5% per month
    
    # Project Types
    PROJECT_TYPES = [
        'Kitchen Remodel',
        'Bathroom Renovation', 
        'Home Addition',
        'Commercial Build-out',
        'Roofing',
        'Siding',
        'New Construction',
        'Repair Work',
        'Custom'
    ]
    
    # Budget Ranges for Leads
    BUDGET_RANGES = [
        'Under $10,000',
        '$10,000 - $25,000',
        '$25,000 - $50,000', 
        '$50,000 - $100,000',
        '$100,000 - $250,000',
        'Over $250,000'
    ]
```

### UI Customization

Create `config/ui.py`:
```python
class UIConfig:
    # Branding
    COMPANY_NAME = "Your Company Name"
    COMPANY_LOGO_URL = "/static/images/logo.png"
    FAVICON_URL = "/static/images/favicon.ico"
    
    # Theme Colors
    PRIMARY_COLOR = "#6ee7b7"      # Accent green
    SECONDARY_COLOR = "#0b0d10"    # Dark background
    SUCCESS_COLOR = "#10b981"      # Success green
    WARNING_COLOR = "#fbbf24"      # Warning yellow
    DANGER_COLOR = "#ef4444"       # Error red
    
    # Layout Settings
    SIDEBAR_COLLAPSED_DEFAULT = False
    ITEMS_PER_PAGE = 25
    MAX_RECENT_ITEMS = 10
    ENABLE_DARK_MODE = True
    
    # Dashboard Widgets
    SHOW_WEATHER_WIDGET = True
    SHOW_CALENDAR_WIDGET = True
    SHOW_NOTIFICATIONS_WIDGET = True
    DASHBOARD_REFRESH_INTERVAL = 300000  # 5 minutes in milliseconds
```

## Database Configuration

### Connection Settings

Create `config/database.py`:
```python
import os

class DatabaseConfig:
    # Connection Settings
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': int(os.environ.get('DB_POOL_SIZE', 5)),
        'pool_timeout': int(os.environ.get('DB_POOL_TIMEOUT', 30)),
        'pool_recycle': int(os.environ.get('DB_POOL_RECYCLE', 3600)),
        'pool_pre_ping': True
    }
    
    # Migration Settings
    SQLALCHEMY_MIGRATE_REPO = './migrations'
    
    # Backup Settings
    BACKUP_SCHEDULE = 'daily'  # daily, weekly, monthly
    BACKUP_RETENTION_DAYS = 30
    BACKUP_COMPRESSION = True
```

## Logging Configuration

Create `config/logging.py`:
```python
import os
from logging.config import dictConfig

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        },
        'detailed': {
            'format': '[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s',
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'default',
            'stream': 'ext://sys.stdout'
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'INFO',
            'formatter': 'detailed',
            'filename': 'logs/contractorpro.log',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 5
        },
        'error_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'ERROR',
            'formatter': 'detailed',
            'filename': 'logs/errors.log',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 5
        }
    },
    'loggers': {
        'contractorpro': {
            'level': 'INFO',
            'handlers': ['console', 'file', 'error_file'],
            'propagate': False
        },
        'sqlalchemy': {
            'level': 'WARNING',
            'handlers': ['file'],
            'propagate': False
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['console']
    }
}

def configure_logging():
    if not os.path.exists('logs'):
        os.makedirs('logs')
    dictConfig(LOGGING_CONFIG)
```

## Performance Configuration

### Caching Strategies

```python
class CacheConfig:
    # Page Caching
    CACHE_PAGES = [
        ('/dashboard', 300),      # 5 minutes
        ('/reports', 600),        # 10 minutes
        ('/jobs', 120),           # 2 minutes
    ]
    
    # Query Caching
    CACHE_EXPENSIVE_QUERIES = True
    QUERY_CACHE_TIMEOUT = 300
    
    # Static Assets
    STATIC_CACHE_TIMEOUT = 31536000  # 1 year
    TEMPLATE_CACHE_SIZE = 400
```

### Background Tasks

```python
class TaskConfig:
    # Celery Configuration (if using background tasks)
    CELERY_BROKER_URL = 'redis://localhost:6379/1'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'
    
    # Task Schedules
    CLEANUP_TEMP_FILES_SCHEDULE = 3600  # 1 hour
    BACKUP_DATABASE_SCHEDULE = 86400    # 24 hours
    SEND_REMINDERS_SCHEDULE = 1800      # 30 minutes
    
    # Task Limits
    MAX_CONCURRENT_UPLOADS = 5
    MAX_BACKUP_SIZE_MB = 1000
```

## API Configuration

### REST API Settings

```python
class APIConfig:
    # Versioning
    API_VERSION = 'v1'
    API_PREFIX = '/api/v1'
    
    # Authentication
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    JWT_EXPIRATION_DELTA = 3600  # 1 hour
    
    # Rate Limiting
    API_RATE_LIMIT = '100/minute'
    API_RATE_LIMIT_BURST = '200/hour'
    
    # Pagination
    DEFAULT_PAGE_SIZE = 25
    MAX_PAGE_SIZE = 100
    
    # Response Format
    INCLUDE_METADATA = True
    PRETTY_JSON = True
```

## Mobile App Configuration

```python
class MobileConfig:
    # Push Notifications
    FIREBASE_SERVER_KEY = os.environ.get('FIREBASE_SERVER_KEY')
    ENABLE_PUSH_NOTIFICATIONS = True
    
    # Offline Sync
    ENABLE_OFFLINE_MODE = True
    SYNC_INTERVAL_MINUTES = 15
    
    # Photo Upload
    COMPRESS_PHOTOS = True
    MAX_PHOTO_SIZE_MB = 10
    PHOTO_QUALITY = 80  # JPEG quality 0-100
```

## Development Configuration

### Development-Specific Settings

```bash
# Development Environment
FLASK_ENV=development
DEBUG=True
TESTING=False

# Database
DATABASE_URL=sqlite:///dev_contractorpro.db

# Disable some features for faster development
MAIL_SUPPRESS_SEND=True
WTF_CSRF_ENABLED=False
RATELIMIT_ENABLED=False

# Debug Toolbar
DEBUG_TB_ENABLED=True
DEBUG_TB_INTERCEPT_REDIRECTS=False
```

### Testing Configuration

```bash
# Test Environment
FLASK_ENV=testing
TESTING=True
DEBUG=False

# Test Database
DATABASE_URL=sqlite:///:memory:
# or
DATABASE_URL=postgresql://test_user:test_pass@localhost/contractorpro_test

# Disable external services
MAIL_SUPPRESS_SEND=True
CELERY_ALWAYS_EAGER=True
CACHE_TYPE=simple
```

## Production Configuration Examples

### Small Business Setup

```bash
# Basic production setup for small contractor business
FLASK_ENV=production
DEBUG=False
DATABASE_URL=postgresql://contractor:secure_pass@localhost/contractorpro
SECRET_KEY=very-long-random-secret-key-change-this
UPLOAD_FOLDER=/var/www/contractorpro/uploads
MAX_CONTENT_LENGTH=104857600  # 100MB
MAIL_SERVER=smtp.gmail.com
MAIL_USERNAME=your-business@gmail.com
CACHE_TYPE=simple
WORKERS=2
```

### Enterprise Setup

```bash
# High-availability enterprise setup
FLASK_ENV=production
DEBUG=False
DATABASE_URL=postgresql://contractor:secure_pass@db-cluster.internal:5432/contractorpro
SECRET_KEY=enterprise-grade-secret-key
UPLOAD_FOLDER=/shared/storage/uploads
AWS_BUCKET_NAME=company-contractorpro-uploads
MAIL_SERVER=smtp.company.com
CACHE_TYPE=redis
CACHE_REDIS_URL=redis://redis-cluster.internal:6379/0
SENTRY_DSN=https://sentry-dsn@company.sentry.io/project
WORKERS=4
ENABLE_QUICKBOOKS_SYNC=True
ENABLE_STRIPE_PAYMENTS=True
```

## Configuration Validation

Create `config/validator.py`:
```python
import os
import sys

def validate_config():
    """Validate required configuration settings"""
    required_vars = [
        'SECRET_KEY',
        'DATABASE_URL'
    ]
    
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    
    if missing_vars:
        print(f"Error: Missing required environment variables: {', '.join(missing_vars)}")
        sys.exit(1)
    
    # Validate SECRET_KEY strength
    secret_key = os.environ.get('SECRET_KEY')
    if len(secret_key) < 32:
        print("Warning: SECRET_KEY should be at least 32 characters long")
    
    # Validate database connection
    try:
        from sqlalchemy import create_engine
        engine = create_engine(os.environ.get('DATABASE_URL'))
        engine.connect()
        print("✓ Database connection successful")
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        sys.exit(1)
    
    print("✓ Configuration validation passed")

if __name__ == '__main__':
    validate_config()
```

## Configuration Templates

### .env.example
```bash
# Copy this file to .env and update the values

# Core Settings
FLASK_ENV=development
DEBUG=True
SECRET_KEY=change-this-to-a-random-secret-key

# Database
DATABASE_URL=postgresql://contractor:password@localhost:5432/contractorpro

# Email
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# File Uploads
UPLOAD_FOLDER=./uploads
MAX_CONTENT_LENGTH=52428800

# Optional Integrations
GOOGLE_MAPS_API_KEY=
STRIPE_PUBLISHABLE_KEY=
STRIPE_SECRET_KEY=
SENTRY_DSN=
```

### docker-compose.override.yml (for development)
```yaml
version: '3.8'

services:
  web:
    environment:
      - FLASK_ENV=development
      - DEBUG=True
    volumes:
      - .:/app
      - ./uploads:/app/uploads
    ports:
      - "5000:5000"
    
  db:
    ports:
      - "5432:5432"
    volumes:
      - ./dev-data:/var/lib/postgresql/data
```

## Configuration Best Practices

1. **Security**
   - Never commit secrets to version control
   - Use strong, unique SECRET_KEY for each environment
   - Rotate secrets regularly
   - Use environment-specific configuration files

2. **Performance**
   - Enable caching in production
   - Configure appropriate worker counts
   - Set reasonable timeouts
   - Monitor resource usage

3. **Maintainability**
   - Document all configuration options
   - Use consistent naming conventions
   - Validate configuration on startup
   - Provide sensible defaults

4. **Monitoring**
   - Enable logging in production
   - Configure error tracking
   - Set up health checks
   - Monitor key metrics

---

*Configuration Documentation Version: 1.0 | Last Updated: January 2025*