# ContractorPro Database Schema Documentation

## Overview

This document outlines the database schema for ContractorPro, including tables, relationships, indexes, and constraints. The current implementation uses in-memory Python lists, but this schema is designed for production database deployment.

## Database Engine Recommendations

**Primary Recommendation: PostgreSQL**
- Excellent JSON support for flexible document storage
- Strong ACID compliance
- Advanced indexing capabilities
- Great performance for reporting queries

**Alternative: MySQL 8.0+**
- Wide hosting availability
- JSON column support
- Good performance
- Familiar to many developers

## Schema Overview

```sql
-- Core business entities
- contractors (business/user accounts)
- jobs (construction projects)
- leads (potential customers)
- documents (file attachments)
- invoices (billing records)
- tasks (project milestones)

-- Supporting entities
- job_status_history (audit trail)
- lead_interactions (communication log)
- project_photos (image gallery)
- financial_transactions (payment tracking)
```

## Table Definitions

### contractors
Primary business account table.

```sql
CREATE TABLE contractors (
    id SERIAL PRIMARY KEY,
    business_name VARCHAR(255) NOT NULL,
    contact_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20),
    address TEXT,
    license_number VARCHAR(100),
    insurance_info JSONB,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- Indexes
CREATE INDEX idx_contractors_email ON contractors(email);
CREATE INDEX idx_contractors_active ON contractors(is_active);
```

### jobs
Construction project records.

```sql
CREATE TABLE jobs (
    id SERIAL PRIMARY KEY,
    contractor_id INTEGER REFERENCES contractors(id) ON DELETE CASCADE,
    client_name VARCHAR(255) NOT NULL,
    client_email VARCHAR(255),
    client_phone VARCHAR(20),
    project_type VARCHAR(100) NOT NULL,
    project_address TEXT NOT NULL,
    project_description TEXT,
    start_date DATE,
    expected_end_date DATE,
    actual_end_date DATE,
    budget DECIMAL(12,2),
    actual_cost DECIMAL(12,2),
    status VARCHAR(20) DEFAULT 'pending',
    priority INTEGER DEFAULT 1,
    notes TEXT,
    metadata JSONB,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT check_job_status CHECK (status IN ('pending', 'active', 'completed', 'cancelled', 'on_hold')),
    CONSTRAINT check_priority CHECK (priority BETWEEN 1 AND 5)
);

-- Indexes
CREATE INDEX idx_jobs_contractor ON jobs(contractor_id);
CREATE INDEX idx_jobs_status ON jobs(status);
CREATE INDEX idx_jobs_start_date ON jobs(start_date);
CREATE INDEX idx_jobs_project_type ON jobs(project_type);
CREATE INDEX idx_jobs_created_date ON jobs(created_date);

-- Full-text search
CREATE INDEX idx_jobs_search ON jobs USING gin(to_tsvector('english', 
    client_name || ' ' || project_type || ' ' || COALESCE(project_description, '')));
```

### leads
Potential customer tracking.

```sql
CREATE TABLE leads (
    id SERIAL PRIMARY KEY,
    contractor_id INTEGER REFERENCES contractors(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    phone VARCHAR(20),
    project_type VARCHAR(100),
    project_address TEXT,
    budget_range VARCHAR(50),
    timeline VARCHAR(100),
    lead_source VARCHAR(100),
    status VARCHAR(20) DEFAULT 'new',
    priority INTEGER DEFAULT 1,
    notes TEXT,
    follow_up_date DATE,
    converted_job_id INTEGER REFERENCES jobs(id),
    metadata JSONB,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT check_lead_status CHECK (status IN ('new', 'contacted', 'qualified', 'quoted', 'won', 'lost', 'nurturing')),
    CONSTRAINT check_lead_priority CHECK (priority BETWEEN 1 AND 5)
);

-- Indexes
CREATE INDEX idx_leads_contractor ON leads(contractor_id);
CREATE INDEX idx_leads_status ON leads(status);
CREATE INDEX idx_leads_follow_up ON leads(follow_up_date);
CREATE INDEX idx_leads_source ON leads(lead_source);
CREATE INDEX idx_leads_created_date ON leads(created_date);
```

### documents
File attachment management.

```sql
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    contractor_id INTEGER REFERENCES contractors(id) ON DELETE CASCADE,
    job_id INTEGER REFERENCES jobs(id) ON DELETE CASCADE,
    document_type VARCHAR(50) NOT NULL,
    filename VARCHAR(255) NOT NULL,
    original_filename VARCHAR(255) NOT NULL,
    file_path TEXT NOT NULL,
    file_size INTEGER,
    mime_type VARCHAR(100),
    description TEXT,
    tags TEXT[],
    metadata JSONB,
    uploaded_by VARCHAR(255),
    uploaded_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT check_doc_type CHECK (document_type IN (
        'permit', 'contract', 'photo', 'invoice', 'plan', 'estimate', 'other'
    ))
);

-- Indexes
CREATE INDEX idx_documents_job ON documents(job_id);
CREATE INDEX idx_documents_type ON documents(document_type);
CREATE INDEX idx_documents_date ON documents(uploaded_date);
CREATE INDEX idx_documents_tags ON documents USING gin(tags);
```

### invoices
Billing and payment tracking.

```sql
CREATE TABLE invoices (
    id SERIAL PRIMARY KEY,
    contractor_id INTEGER REFERENCES contractors(id) ON DELETE CASCADE,
    job_id INTEGER REFERENCES jobs(id) ON DELETE CASCADE,
    invoice_number VARCHAR(100) UNIQUE NOT NULL,
    client_name VARCHAR(255) NOT NULL,
    client_address TEXT,
    amount DECIMAL(12,2) NOT NULL,
    tax_amount DECIMAL(12,2) DEFAULT 0,
    total_amount DECIMAL(12,2) NOT NULL,
    status VARCHAR(20) DEFAULT 'draft',
    issue_date DATE NOT NULL,
    due_date DATE NOT NULL,
    paid_date DATE,
    payment_method VARCHAR(50),
    notes TEXT,
    line_items JSONB,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT check_invoice_status CHECK (status IN ('draft', 'sent', 'paid', 'overdue', 'cancelled')),
    CONSTRAINT check_amounts CHECK (total_amount >= 0 AND tax_amount >= 0)
);

-- Indexes
CREATE INDEX idx_invoices_contractor ON invoices(contractor_id);
CREATE INDEX idx_invoices_job ON invoices(job_id);
CREATE INDEX idx_invoices_number ON invoices(invoice_number);
CREATE INDEX idx_invoices_status ON invoices(status);
CREATE INDEX idx_invoices_due_date ON invoices(due_date);
```

### tasks
Project milestone and task tracking.

```sql
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    job_id INTEGER REFERENCES jobs(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    assigned_to VARCHAR(255),
    status VARCHAR(20) DEFAULT 'pending',
    priority INTEGER DEFAULT 1,
    start_date DATE,
    due_date DATE,
    completed_date DATE,
    estimated_hours DECIMAL(5,2),
    actual_hours DECIMAL(5,2),
    dependencies INTEGER[],
    notes TEXT,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT check_task_status CHECK (status IN ('pending', 'in_progress', 'completed', 'cancelled', 'blocked')),
    CONSTRAINT check_task_priority CHECK (priority BETWEEN 1 AND 5)
);

-- Indexes
CREATE INDEX idx_tasks_job ON tasks(job_id);
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_assigned ON tasks(assigned_to);
CREATE INDEX idx_tasks_due_date ON tasks(due_date);
```

### job_status_history
Audit trail for job changes.

```sql
CREATE TABLE job_status_history (
    id SERIAL PRIMARY KEY,
    job_id INTEGER REFERENCES jobs(id) ON DELETE CASCADE,
    previous_status VARCHAR(20),
    new_status VARCHAR(20) NOT NULL,
    changed_by VARCHAR(255),
    change_reason TEXT,
    changed_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_job_history_job ON job_status_history(job_id);
CREATE INDEX idx_job_history_date ON job_status_history(changed_date);
```

### lead_interactions
Communication log for leads.

```sql
CREATE TABLE lead_interactions (
    id SERIAL PRIMARY KEY,
    lead_id INTEGER REFERENCES leads(id) ON DELETE CASCADE,
    interaction_type VARCHAR(50) NOT NULL,
    interaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    subject VARCHAR(255),
    notes TEXT,
    outcome VARCHAR(100),
    next_action VARCHAR(255),
    next_action_date DATE,
    created_by VARCHAR(255),
    
    CONSTRAINT check_interaction_type CHECK (interaction_type IN (
        'phone_call', 'email', 'meeting', 'site_visit', 'quote_sent', 'follow_up'
    ))
);

-- Indexes
CREATE INDEX idx_interactions_lead ON lead_interactions(lead_id);
CREATE INDEX idx_interactions_type ON lead_interactions(interaction_type);
CREATE INDEX idx_interactions_date ON lead_interactions(interaction_date);
```

### project_photos
Image gallery for projects.

```sql
CREATE TABLE project_photos (
    id SERIAL PRIMARY KEY,
    job_id INTEGER REFERENCES jobs(id) ON DELETE CASCADE,
    document_id INTEGER REFERENCES documents(id) ON DELETE CASCADE,
    photo_type VARCHAR(50),
    caption TEXT,
    taken_date DATE,
    location_description TEXT,
    metadata JSONB,
    display_order INTEGER DEFAULT 0,
    is_featured BOOLEAN DEFAULT FALSE,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT check_photo_type CHECK (photo_type IN (
        'before', 'progress', 'after', 'materials', 'team', 'problem', 'solution'
    ))
);

-- Indexes
CREATE INDEX idx_photos_job ON project_photos(job_id);
CREATE INDEX idx_photos_type ON project_photos(photo_type);
CREATE INDEX idx_photos_order ON project_photos(display_order);
CREATE INDEX idx_photos_featured ON project_photos(is_featured);
```

## Relationships

```
contractors (1) ←→ (M) jobs
contractors (1) ←→ (M) leads  
contractors (1) ←→ (M) documents
contractors (1) ←→ (M) invoices

jobs (1) ←→ (M) documents
jobs (1) ←→ (M) invoices
jobs (1) ←→ (M) tasks
jobs (1) ←→ (M) project_photos
jobs (1) ←→ (M) job_status_history

leads (1) ←→ (M) lead_interactions
leads (1) ←→ (1) jobs (converted)

documents (1) ←→ (1) project_photos
```

## Views

### Active Projects Summary
```sql
CREATE VIEW active_projects_summary AS
SELECT 
    j.id,
    j.client_name,
    j.project_type,
    j.budget,
    j.start_date,
    j.expected_end_date,
    COUNT(t.id) as total_tasks,
    COUNT(CASE WHEN t.status = 'completed' THEN 1 END) as completed_tasks,
    COALESCE(SUM(i.total_amount), 0) as invoiced_amount
FROM jobs j
LEFT JOIN tasks t ON j.id = t.job_id
LEFT JOIN invoices i ON j.id = i.job_id AND i.status != 'cancelled'
WHERE j.status = 'active'
GROUP BY j.id, j.client_name, j.project_type, j.budget, j.start_date, j.expected_end_date;
```

### Lead Conversion Metrics
```sql
CREATE VIEW lead_conversion_metrics AS
SELECT 
    DATE_TRUNC('month', created_date) as month,
    COUNT(*) as total_leads,
    COUNT(CASE WHEN status = 'won' THEN 1 END) as converted_leads,
    ROUND(
        COUNT(CASE WHEN status = 'won' THEN 1 END)::DECIMAL / 
        NULLIF(COUNT(*), 0) * 100, 2
    ) as conversion_rate
FROM leads
WHERE created_date >= CURRENT_DATE - INTERVAL '12 months'
GROUP BY DATE_TRUNC('month', created_date)
ORDER BY month DESC;
```

## Triggers

### Update Timestamps
```sql
CREATE OR REPLACE FUNCTION update_updated_date()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_date = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_jobs_updated_date 
    BEFORE UPDATE ON jobs 
    FOR EACH ROW EXECUTE FUNCTION update_updated_date();

CREATE TRIGGER update_leads_updated_date 
    BEFORE UPDATE ON leads 
    FOR EACH ROW EXECUTE FUNCTION update_updated_date();
```

### Job Status History Trigger
```sql
CREATE OR REPLACE FUNCTION log_job_status_change()
RETURNS TRIGGER AS $$
BEGIN
    IF OLD.status != NEW.status THEN
        INSERT INTO job_status_history (job_id, previous_status, new_status, changed_by)
        VALUES (NEW.id, OLD.status, NEW.status, current_user);
    END IF;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER job_status_change_trigger
    AFTER UPDATE ON jobs
    FOR EACH ROW EXECUTE FUNCTION log_job_status_change();
```

## Indexes for Performance

### Composite Indexes
```sql
-- Job searching and filtering
CREATE INDEX idx_jobs_contractor_status ON jobs(contractor_id, status);
CREATE INDEX idx_jobs_type_date ON jobs(project_type, created_date);

-- Lead management
CREATE INDEX idx_leads_contractor_status ON leads(contractor_id, status);
CREATE INDEX idx_leads_source_date ON leads(lead_source, created_date);

-- Financial reporting
CREATE INDEX idx_invoices_contractor_date ON invoices(contractor_id, issue_date);
CREATE INDEX idx_invoices_status_due ON invoices(status, due_date);
```

## Data Migration Scripts

### From In-Memory to PostgreSQL
```sql
-- Example migration for existing data
INSERT INTO jobs (client_name, project_type, address, start_date, budget, status, created_date)
SELECT 
    client_name,
    project_type,
    address,
    start_date::date,
    budget::decimal,
    status,
    created_date::timestamp
FROM temp_jobs_import;
```

## Backup Strategy

### Daily Backups
```bash
pg_dump -h localhost -U contractor_user -d contractorpro \
    --format=custom --compress=9 \
    --file=backup_$(date +%Y%m%d).dump
```

### Point-in-Time Recovery
```sql
-- Enable WAL archiving
archive_mode = on
archive_command = 'cp %p /backup/archive/%f'
wal_level = replica
```

## Performance Considerations

1. **Indexing Strategy**
   - Primary indexes on foreign keys
   - Composite indexes for common query patterns
   - Full-text search indexes for content

2. **Partitioning**
   - Consider partitioning large tables by date
   - Partition job_status_history by month
   - Partition documents by year

3. **Query Optimization**
   - Use EXPLAIN ANALYZE for slow queries
   - Monitor index usage with pg_stat_user_indexes
   - Consider materialized views for complex reports

## Security Considerations

1. **Access Control**
   - Row-level security for multi-tenant data
   - Role-based permissions
   - Audit logging for sensitive operations

2. **Data Encryption**
   - Encrypt sensitive fields (SSN, credit cards)
   - Use application-level encryption for PII
   - SSL/TLS for all connections

---

*Database Schema Version: 1.0 | Last Updated: January 2025*