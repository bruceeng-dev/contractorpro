# ContractorPro Deployment Guide

## Overview

This guide covers deploying ContractorPro from development to production environments. It includes instructions for various hosting platforms, database setup, and configuration management.

## Prerequisites

- Python 3.8 or higher
- PostgreSQL 12+ (recommended) or MySQL 8.0+
- Git for version control
- Domain name and SSL certificate for production

## Environment Setup

### Development Environment

1. **Clone the Repository**
```bash
git clone https://github.com/yourorg/contractorpro.git
cd contractorpro
```

2. **Create Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Environment Configuration**
```bash
cp .env.example .env
# Edit .env with your settings
```

5. **Run Development Server**
```bash
python app.py
```

## Production Deployment Options

### Option 1: DigitalOcean App Platform

**1. Prepare Application**
```bash
# Add app.yaml to root directory
cat > app.yaml << 'EOF'
name: contractorpro
services:
- name: web
  source_dir: /
  github:
    repo: yourorg/contractorpro
    branch: main
  run_command: gunicorn --worker-tmp-dir /dev/shm app:app
  environment_slug: python
  instance_count: 1
  instance_size_slug: basic-xxs
  envs:
  - key: DATABASE_URL
    scope: RUN_AND_BUILD_TIME
    type: SECRET
  - key: SECRET_KEY
    scope: RUN_AND_BUILD_TIME
    type: SECRET
databases:
- name: contractorpro-db
  engine: PG
  version: "13"
  size: db-s-dev-database
EOF
```

**2. Deploy**
```bash
# Push to GitHub
git add .
git commit -m "Add DigitalOcean deployment config"
git push origin main

# Deploy via DigitalOcean dashboard
# Connect GitHub repository
# Set environment variables
# Deploy application
```

### Option 2: Heroku Deployment

**1. Heroku Setup**
```bash
# Install Heroku CLI
curl https://cli-assets.heroku.com/install.sh | sh

# Login to Heroku
heroku login

# Create Heroku app
heroku create contractorpro-your-name
```

**2. Add Procfile**
```bash
echo "web: gunicorn app:app" > Procfile
```

**3. Configure Environment**
```bash
heroku config:set SECRET_KEY="your-secret-key-here"
heroku config:set FLASK_ENV="production"
heroku config:set DATABASE_URL="postgresql://..."
```

**4. Add PostgreSQL**
```bash
heroku addons:create heroku-postgresql:hobby-dev
```

**5. Deploy**
```bash
git add .
git commit -m "Add Heroku deployment config"
git push heroku main
```

### Option 3: AWS EC2 with Docker

**1. Create Dockerfile**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash contractor
RUN chown -R contractor:contractor /app
USER contractor

# Expose port
EXPOSE 5000

# Run application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]
```

**2. Create docker-compose.yml**
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/contractorpro
      - SECRET_KEY=${SECRET_KEY}
      - FLASK_ENV=production
    depends_on:
      - db
    volumes:
      - ./uploads:/app/uploads

  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=contractorpro
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - web

volumes:
  postgres_data:
```

**3. Deploy to EC2**
```bash
# Launch EC2 instance (Ubuntu 20.04 LTS)
# SSH into instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Install Docker
sudo apt update
sudo apt install -y docker.io docker-compose
sudo usermod -aG docker ubuntu

# Clone and deploy
git clone https://github.com/yourorg/contractorpro.git
cd contractorpro
docker-compose up -d
```

### Option 4: Google Cloud Run

**1. Create cloudbuild.yaml**
```yaml
steps:
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/contractorpro', '.']
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/contractorpro']
  - name: 'gcr.io/cloud-builders/gcloud'
    args: [
      'run', 'deploy', 'contractorpro',
      '--image', 'gcr.io/$PROJECT_ID/contractorpro',
      '--region', 'us-central1',
      '--platform', 'managed',
      '--allow-unauthenticated'
    ]
```

**2. Deploy**
```bash
gcloud builds submit --config cloudbuild.yaml
```

## Database Setup

### PostgreSQL Setup

**1. Install PostgreSQL**
```bash
# Ubuntu/Debian
sudo apt install postgresql postgresql-contrib

# CentOS/RHEL
sudo yum install postgresql-server postgresql-contrib

# macOS
brew install postgresql
```

**2. Create Database and User**
```sql
-- Connect as postgres user
sudo -u postgres psql

-- Create database and user
CREATE DATABASE contractorpro;
CREATE USER contractor_user WITH PASSWORD 'secure_password_here';
GRANT ALL PRIVILEGES ON DATABASE contractorpro TO contractor_user;

-- Exit psql
\q
```

**3. Run Database Migrations**
```bash
# Create tables (if using migration script)
python migrate.py

# Or import schema directly
psql -h localhost -U contractor_user -d contractorpro -f docs/schema.sql
```

### Database Migration Script

Create `migrate.py`:
```python
import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def create_database():
    # Read schema file
    with open('docs/schema.sql', 'r') as f:
        schema = f.read()
    
    # Connect to database
    conn = psycopg2.connect(os.environ['DATABASE_URL'])
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    
    # Execute schema
    cursor.execute(schema)
    
    cursor.close()
    conn.close()
    
    print("Database schema created successfully!")

if __name__ == '__main__':
    create_database()
```

## Web Server Configuration

### Nginx Configuration

Create `/etc/nginx/sites-available/contractorpro`:
```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    ssl_certificate /etc/ssl/certs/yourdomain.com.crt;
    ssl_certificate_key /etc/ssl/private/yourdomain.com.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    client_max_body_size 50M;  # For file uploads

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /path/to/contractorpro/static/;
        expires 1y;
        add_header Cache-Control public;
    }

    location /uploads/ {
        alias /path/to/contractorpro/uploads/;
        expires 1y;
        add_header Cache-Control public;
    }
}
```

Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/contractorpro /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### Systemd Service

Create `/etc/systemd/system/contractorpro.service`:
```ini
[Unit]
Description=ContractorPro Flask Application
After=network.target

[Service]
User=contractor
Group=contractor
WorkingDirectory=/home/contractor/contractorpro
Environment="PATH=/home/contractor/contractorpro/venv/bin"
Environment="DATABASE_URL=postgresql://contractor_user:password@localhost/contractorpro"
Environment="SECRET_KEY=your-secret-key-here"
Environment="FLASK_ENV=production"
ExecStart=/home/contractor/contractorpro/venv/bin/gunicorn --bind 127.0.0.1:5000 --workers 2 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable contractorpro
sudo systemctl start contractorpro
```

## SSL Certificate Setup

### Let's Encrypt (Recommended)

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal setup (already configured by default)
sudo crontab -l | grep certbot
```

## Environment Variables

### Production .env Template

```env
# Application Settings
FLASK_ENV=production
SECRET_KEY=your-super-secret-key-change-this-in-production
DEBUG=False

# Database Configuration
DATABASE_URL=postgresql://contractor_user:secure_password@localhost:5432/contractorpro

# File Upload Settings
UPLOAD_FOLDER=/var/www/contractorpro/uploads
MAX_CONTENT_LENGTH=52428800  # 50MB in bytes

# Email Configuration (for notifications)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# Backup Settings
BACKUP_BUCKET=s3://your-backup-bucket
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key

# Monitoring
SENTRY_DSN=https://your-sentry-dsn@sentry.io/project-id

# Rate Limiting
RATELIMIT_STORAGE_URL=redis://localhost:6379
```

## Monitoring and Logging

### Application Logging

Add to `app.py`:
```python
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    
    file_handler = RotatingFileHandler('logs/contractorpro.log', 
                                       maxBytes=10240000, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    
    app.logger.setLevel(logging.INFO)
    app.logger.info('ContractorPro startup')
```

### System Monitoring

**1. Install monitoring tools**
```bash
# Install htop, ncdu, and other utilities
sudo apt install htop ncdu iotop nethogs

# Install New Relic (optional)
wget -O - https://download.newrelic.com/548C16BF.gpg | sudo apt-key add -
echo "deb http://apt.newrelic.com/debian/ newrelic non-free" | sudo tee /etc/apt/sources.list.d/newrelic.list
sudo apt update
sudo apt install newrelic-sysmond
```

**2. Database monitoring**
```sql
-- Enable logging in postgresql.conf
log_statement = 'all'
log_duration = on
log_min_duration_statement = 1000  # Log slow queries
```

## Backup Strategy

### Database Backups

Create `/home/contractor/backup_db.sh`:
```bash
#!/bin/bash

BACKUP_DIR="/home/contractor/backups"
DB_NAME="contractorpro"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Create backup
pg_dump -h localhost -U contractor_user $DB_NAME | gzip > "$BACKUP_DIR/contractorpro_$DATE.sql.gz"

# Remove backups older than 30 days
find $BACKUP_DIR -name "contractorpro_*.sql.gz" -mtime +30 -delete

# Upload to S3 (optional)
# aws s3 cp "$BACKUP_DIR/contractorpro_$DATE.sql.gz" s3://your-backup-bucket/db/
```

Add to crontab:
```bash
# Daily backup at 2 AM
0 2 * * * /home/contractor/backup_db.sh
```

### File Backups

```bash
#!/bin/bash
# backup_files.sh

tar -czf /home/contractor/backups/uploads_$(date +%Y%m%d).tar.gz /var/www/contractorpro/uploads/
# aws s3 cp /home/contractor/backups/uploads_$(date +%Y%m%d).tar.gz s3://your-backup-bucket/files/
```

## Performance Optimization

### Application Optimization

1. **Enable Gzip Compression**
```python
from flask_compress import Compress
compress = Compress(app)
```

2. **Configure Redis for Caching**
```python
import redis
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'redis'})
```

### Database Optimization

```sql
-- Create indexes for common queries
CREATE INDEX CONCURRENTLY idx_jobs_contractor_status ON jobs(contractor_id, status);
CREATE INDEX CONCURRENTLY idx_leads_contractor_date ON leads(contractor_id, created_date);

-- Configure PostgreSQL
shared_buffers = 256MB
effective_cache_size = 1GB
maintenance_work_mem = 64MB
checkpoint_completion_target = 0.9
```

## Security Checklist

- [ ] Use strong, unique SECRET_KEY
- [ ] Enable HTTPS with valid SSL certificate
- [ ] Configure firewall to allow only necessary ports
- [ ] Set up regular security updates
- [ ] Use environment variables for sensitive data
- [ ] Enable database connection encryption
- [ ] Implement rate limiting
- [ ] Set up monitoring and alerting
- [ ] Configure regular backups
- [ ] Review and rotate credentials regularly

## Troubleshooting

### Common Issues

**1. Database Connection Error**
```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Test connection
psql -h localhost -U contractor_user -d contractorpro -c "\l"
```

**2. Permission Errors**
```bash
# Fix file permissions
sudo chown -R contractor:contractor /home/contractor/contractorpro
chmod +x /home/contractor/contractorpro/venv/bin/gunicorn
```

**3. High Memory Usage**
```bash
# Monitor processes
htop
# Check for memory leaks in application logs
tail -f logs/contractorpro.log
```

## Maintenance

### Regular Tasks

- **Weekly**: Review application logs
- **Monthly**: Update dependencies and security patches
- **Quarterly**: Review and optimize database performance
- **Annually**: Renew SSL certificates and review security settings

### Update Process

```bash
# Backup before updates
./backup_db.sh

# Update code
git pull origin main
pip install -r requirements.txt

# Run migrations
python migrate.py

# Restart services
sudo systemctl restart contractorpro
sudo systemctl reload nginx
```

---

*Deployment Guide Version: 1.0 | Last Updated: January 2025*