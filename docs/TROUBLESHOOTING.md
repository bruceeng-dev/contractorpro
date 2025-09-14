# ContractorPro Troubleshooting Guide

## Overview

This guide helps you diagnose and resolve common issues with ContractorPro. It covers installation problems, runtime errors, performance issues, and integration failures.

## Quick Diagnostics

### System Health Check

Run this command to check system status:

```bash
# Check if ContractorPro is running
curl -f http://localhost:5000/health || echo "Service not responding"

# Check database connection
python -c "import psycopg2; conn = psycopg2.connect('postgresql://user:pass@localhost/contractorpro'); print('DB OK')"

# Check disk space
df -h

# Check memory usage
free -h

# Check process status
ps aux | grep -E "(gunicorn|python|contractorpro)"
```

## Installation Issues

### 1. Python Version Conflicts

**Problem**: "Python version not supported" or module import errors

**Solution**:
```bash
# Check Python version
python --version
python3 --version

# Install correct version (3.8+)
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-dev

# Use specific Python version
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Virtual Environment Issues

**Problem**: "Module not found" errors after installation

**Solution**:
```bash
# Verify virtual environment is active
which python
which pip

# If not active, activate it
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Reinstall packages
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Database Connection Errors

**Problem**: "Could not connect to database" or "authentication failed"

**Solution**:
```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Test connection manually
psql -h localhost -U contractor_user -d contractorpro

# Reset password if needed
sudo -u postgres psql
ALTER USER contractor_user PASSWORD 'new_password';

# Update DATABASE_URL in .env
DATABASE_URL=postgresql://contractor_user:new_password@localhost:5432/contractorpro
```

### 4. Permission Errors

**Problem**: "Permission denied" when accessing files or directories

**Solution**:
```bash
# Fix ownership
sudo chown -R $USER:$USER /path/to/contractorpro

# Fix upload directory permissions
mkdir -p uploads
chmod 755 uploads

# Fix log directory permissions  
mkdir -p logs
chmod 755 logs
```

## Runtime Errors

### 1. Application Won't Start

**Problem**: Flask app crashes on startup

**Diagnostic Steps**:
```bash
# Check for syntax errors
python -m py_compile app.py

# Run in debug mode to see detailed errors
FLASK_ENV=development python app.py

# Check environment variables
env | grep -E "(DATABASE_URL|SECRET_KEY|FLASK_ENV)"

# Verify all dependencies
pip check
```

**Common Fixes**:
- Ensure all environment variables are set
- Check database is running and accessible
- Verify SECRET_KEY is defined
- Ensure upload directories exist

### 2. 500 Internal Server Error

**Problem**: Web pages show "500 Internal Server Error"

**Diagnostic Steps**:
```bash
# Check application logs
tail -f logs/contractorpro.log

# Check web server logs
sudo tail -f /var/log/nginx/error.log

# Test app directly (bypass web server)
curl -v http://127.0.0.1:5000/
```

**Common Causes**:
- Database connection lost
- Missing environment variables
- File permission issues
- Memory/disk space exhausted

### 3. Database Migration Errors

**Problem**: Database schema out of sync or migration failures

**Solution**:
```bash
# Backup database first
pg_dump contractorpro > backup_before_migration.sql

# Check migration status
python manage.py db current

# Run migrations
python manage.py db upgrade

# If migrations fail, reset (CAUTION: data loss)
python manage.py db downgrade base
python manage.py db upgrade
```

### 4. File Upload Failures

**Problem**: Document uploads fail or timeout

**Diagnostic Steps**:
```bash
# Check upload directory permissions
ls -la uploads/

# Check disk space
df -h

# Verify file size limits
grep MAX_CONTENT_LENGTH .env
```

**Solutions**:
```bash
# Fix permissions
chmod 755 uploads/
chown -R www-data:www-data uploads/

# Increase limits in nginx.conf
client_max_body_size 100M;

# Increase limits in app
MAX_CONTENT_LENGTH=104857600  # 100MB
```

## Performance Issues

### 1. Slow Page Loading

**Problem**: Web pages load very slowly

**Diagnostic Steps**:
```bash
# Check database performance
SELECT * FROM pg_stat_activity WHERE state = 'active';

# Check system resources
top
iotop

# Profile Flask app
pip install flask-profiler
# Add to app.py: app.config["flask_profiler"] = {"enabled": True}
```

**Solutions**:
- Add database indexes for slow queries
- Enable caching (Redis/Memcached)
- Optimize images and static files
- Increase server resources

### 2. High Memory Usage

**Problem**: Application consumes too much memory

**Diagnostic Steps**:
```bash
# Monitor memory usage
watch -n 1 'ps aux | grep python'

# Check for memory leaks
python -m memory_profiler app.py
```

**Solutions**:
```python
# Add to app.py - limit SQLAlchemy pool size
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': 5,
    'pool_recycle': 3600,
    'pool_pre_ping': True
}

# Use pagination for large datasets
jobs = Job.query.paginate(page=1, per_page=20)
```

### 3. Database Performance

**Problem**: Slow database queries

**Diagnostic Steps**:
```sql
-- Enable query logging in postgresql.conf
log_statement = 'all'
log_min_duration_statement = 1000

-- Check slow queries
SELECT query, mean_time, calls FROM pg_stat_statements 
ORDER BY mean_time DESC LIMIT 10;
```

**Solutions**:
```sql
-- Add missing indexes
CREATE INDEX CONCURRENTLY idx_jobs_contractor_status ON jobs(contractor_id, status);
CREATE INDEX CONCURRENTLY idx_jobs_created_date ON jobs(created_date);

-- Update table statistics
ANALYZE jobs;
ANALYZE leads;

-- Consider partitioning large tables
```

## Integration Issues

### 1. Email Not Sending

**Problem**: Email notifications not working

**Diagnostic Steps**:
```bash
# Test SMTP connection
python -c "
import smtplib
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login('your-email@gmail.com', 'your-password')
print('SMTP connection successful')
server.quit()
"

# Check email configuration
env | grep MAIL_
```

**Solutions**:
- Enable "Less secure apps" or use App Passwords for Gmail
- Check firewall blocking port 587/465
- Verify SMTP credentials
- Check email service provider settings

### 2. File Upload to Cloud Storage Failing

**Problem**: Files not uploading to AWS S3/Azure

**Diagnostic Steps**:
```bash
# Test AWS credentials
aws s3 ls s3://your-bucket-name/

# Check AWS configuration
env | grep AWS_

# Test Azure connection
az storage blob list --container-name uploads --account-name youraccount
```

**Solutions**:
- Verify cloud storage credentials
- Check bucket permissions
- Ensure correct region settings
- Test network connectivity

### 3. Payment Integration Issues

**Problem**: Stripe payments not working

**Diagnostic Steps**:
```bash
# Check Stripe keys
env | grep STRIPE_

# Test API connection
curl -X GET https://api.stripe.com/v1/customers \
  -H "Authorization: Bearer sk_test_your_secret_key"
```

**Solutions**:
- Use correct Stripe keys (test vs live)
- Check webhook endpoint configuration
- Verify SSL certificate validity
- Review Stripe dashboard for errors

## Browser-Specific Issues

### 1. JavaScript Errors

**Problem**: Interactive features not working

**Diagnostic Steps**:
- Open browser developer tools (F12)
- Check Console tab for JavaScript errors
- Verify static files are loading properly

**Solutions**:
```nginx
# Ensure static files are served correctly
location /static/ {
    alias /path/to/contractorpro/static/;
    expires 1y;
    add_header Cache-Control public;
}
```

### 2. CSS Not Loading

**Problem**: Page looks unstyled

**Solutions**:
- Check browser cache (Ctrl+F5 to force refresh)
- Verify CSS file paths in templates
- Check web server static file configuration

### 3. Session/Cookie Issues

**Problem**: Users getting logged out frequently

**Solutions**:
```python
# Increase session timeout in app.py
app.permanent_session_lifetime = timedelta(hours=24)

# Check secure cookie settings
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax'
)
```

## Mobile App Issues

### 1. API Connection Failures

**Problem**: Mobile app can't connect to server

**Diagnostic Steps**:
```bash
# Test API endpoints
curl -H "Content-Type: application/json" \
     -X GET http://your-domain.com/api/v1/jobs

# Check CORS settings
curl -H "Origin: http://localhost:3000" \
     -H "Access-Control-Request-Method: POST" \
     -X OPTIONS http://your-domain.com/api/v1/jobs
```

**Solutions**:
```python
# Add CORS support
from flask_cors import CORS
CORS(app, origins=['http://localhost:3000', 'https://your-domain.com'])
```

### 2. Photo Upload Issues

**Problem**: Photo uploads fail from mobile devices

**Solutions**:
- Increase file size limits
- Add proper image compression
- Check mobile data/WiFi connectivity
- Verify HTTPS configuration

## Backup and Recovery

### 1. Database Recovery

**Problem**: Database corruption or data loss

**Recovery Steps**:
```bash
# Stop application
sudo systemctl stop contractorpro

# Restore from backup
pg_restore -h localhost -U contractor_user -d contractorpro backup.dump

# Restart application
sudo systemctl start contractorpro
```

### 2. File Recovery

**Problem**: Uploaded files missing or corrupted

**Recovery Steps**:
```bash
# Restore from backup
rsync -av backup/uploads/ /path/to/contractorpro/uploads/

# Fix permissions
chown -R www-data:www-data /path/to/contractorpro/uploads/
chmod -R 755 /path/to/contractorpro/uploads/
```

## Monitoring and Alerting

### Set Up Basic Monitoring

```bash
# Install monitoring tools
sudo apt install htop iotop nethogs

# Monitor logs in real-time
tail -f logs/contractorpro.log | grep ERROR

# Set up disk space alerts
crontab -e
# Add: 0 * * * * /path/to/check_disk_space.sh
```

### Health Check Endpoint

Add to `app.py`:
```python
@app.route('/health')
def health_check():
    try:
        # Check database
        db.session.execute('SELECT 1')
        
        # Check disk space
        import shutil
        free_space = shutil.disk_usage('.').free
        
        return {
            'status': 'healthy',
            'database': 'connected',
            'disk_space_mb': free_space // 1024 // 1024
        }
    except Exception as e:
        return {'status': 'unhealthy', 'error': str(e)}, 500
```

## Getting Help

### Before Contacting Support

1. **Check this troubleshooting guide**
2. **Review application logs**: `tail -100 logs/contractorpro.log`
3. **Test basic functionality**: Login, create job, upload document
4. **Check system resources**: CPU, memory, disk space
5. **Verify configuration**: Environment variables, database settings

### Information to Include in Support Requests

- ContractorPro version
- Operating system and version
- Python version
- Database type and version
- Error messages (full stack traces)
- Steps to reproduce the issue
- Recent changes to configuration

### Log Collection Script

Create `collect_logs.sh`:
```bash
#!/bin/bash

LOG_DIR="support_logs_$(date +%Y%m%d_%H%M%S)"
mkdir -p $LOG_DIR

# Application logs
cp logs/*.log $LOG_DIR/ 2>/dev/null || true

# System info
uname -a > $LOG_DIR/system_info.txt
python --version > $LOG_DIR/python_version.txt
pip list > $LOG_DIR/installed_packages.txt

# Configuration (remove sensitive data)
env | grep -E "(FLASK|DB|MAIL)" | sed 's/=.*/=***/' > $LOG_DIR/env_vars.txt

# Database info
psql -c "\l" > $LOG_DIR/db_info.txt 2>/dev/null || true

# Create archive
tar -czf $LOG_DIR.tar.gz $LOG_DIR/
rm -rf $LOG_DIR

echo "Support logs collected: $LOG_DIR.tar.gz"
```

## Emergency Procedures

### Complete System Failure

1. **Stop all services**:
   ```bash
   sudo systemctl stop contractorpro
   sudo systemctl stop nginx
   sudo systemctl stop postgresql
   ```

2. **Check system health**:
   ```bash
   df -h
   free -h
   dmesg | tail -50
   ```

3. **Restore from backup** (if needed):
   ```bash
   # Database
   pg_restore -C -d postgres backup.dump
   
   # Files
   rsync -av backup/uploads/ uploads/
   ```

4. **Start services**:
   ```bash
   sudo systemctl start postgresql
   sudo systemctl start contractorpro
   sudo systemctl start nginx
   ```

### Security Incident Response

1. **Immediate actions**:
   - Change all passwords and API keys
   - Check logs for suspicious activity
   - Temporary block suspicious IP addresses

2. **Investigation**:
   - Review access logs
   - Check file integrity
   - Scan for malware

3. **Recovery**:
   - Apply security patches
   - Restore from clean backup if needed
   - Update security configurations

---

*Troubleshooting Guide Version: 1.0 | Last Updated: January 2025*