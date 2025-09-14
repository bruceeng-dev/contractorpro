# ContractorPro API Documentation

## Overview

ContractorPro provides a RESTful API for integrating with external systems, mobile applications, and third-party tools. This documentation covers all available endpoints and their usage.

## Base URL
```
http://localhost:5000/api/v1
```

## Authentication
Currently, the API uses session-based authentication. Future versions will implement JWT tokens for stateless authentication.

## Response Format
All API responses use JSON format:

```json
{
  "success": true,
  "data": {...},
  "message": "Operation completed successfully",
  "timestamp": "2025-01-15T10:30:00Z"
}
```

Error responses:
```json
{
  "success": false,
  "error": "Error description",
  "error_code": "ERROR_CODE",
  "timestamp": "2025-01-15T10:30:00Z"
}
```

## Jobs API

### Get All Jobs
```http
GET /api/v1/jobs
```

**Query Parameters:**
- `status` (optional) - Filter by status: `pending`, `active`, `completed`
- `client` (optional) - Filter by client name
- `limit` (optional) - Limit number of results (default: 50)
- `offset` (optional) - Pagination offset (default: 0)

**Response:**
```json
{
  "success": true,
  "data": {
    "jobs": [
      {
        "id": 1,
        "client_name": "John Smith",
        "project_type": "Kitchen Remodel",
        "address": "123 Main St, Anytown, ST 12345",
        "start_date": "2025-02-01",
        "budget": 45000,
        "status": "active",
        "created_date": "2025-01-15"
      }
    ],
    "total": 1,
    "limit": 50,
    "offset": 0
  }
}
```

### Get Job by ID
```http
GET /api/v1/jobs/{id}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "client_name": "John Smith",
    "project_type": "Kitchen Remodel",
    "address": "123 Main St, Anytown, ST 12345",
    "start_date": "2025-02-01",
    "budget": 45000,
    "status": "active",
    "created_date": "2025-01-15",
    "notes": "Custom cabinet installation required",
    "timeline": [
      {
        "date": "2025-01-15",
        "event": "Job created",
        "user": "system"
      }
    ]
  }
}
```

### Create New Job
```http
POST /api/v1/jobs
```

**Request Body:**
```json
{
  "client_name": "Jane Doe",
  "project_type": "Bathroom Renovation",
  "address": "456 Oak Ave, Somewhere, ST 67890",
  "start_date": "2025-03-01",
  "budget": 28000,
  "notes": "Complete bathroom overhaul"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 2,
    "client_name": "Jane Doe",
    "project_type": "Bathroom Renovation",
    "address": "456 Oak Ave, Somewhere, ST 67890",
    "start_date": "2025-03-01",
    "budget": 28000,
    "status": "pending",
    "created_date": "2025-01-15"
  },
  "message": "Job created successfully"
}
```

### Update Job
```http
PUT /api/v1/jobs/{id}
```

**Request Body:** (Include only fields to update)
```json
{
  "status": "active",
  "budget": 30000,
  "notes": "Budget increased due to additional work"
}
```

### Delete Job
```http
DELETE /api/v1/jobs/{id}
```

## Leads API

### Get All Leads
```http
GET /api/v1/leads
```

**Query Parameters:**
- `status` (optional) - Filter by status: `new`, `contacted`, `quoted`, `won`, `lost`
- `project_type` (optional) - Filter by project type
- `limit` (optional) - Limit number of results
- `offset` (optional) - Pagination offset

**Response:**
```json
{
  "success": true,
  "data": {
    "leads": [
      {
        "id": 1,
        "name": "Sarah Miller",
        "email": "sarah@email.com",
        "phone": "(555) 123-4567",
        "project_type": "Home Addition",
        "budget_range": "$50k-$100k",
        "status": "new",
        "notes": "Interested in adding second story",
        "created_date": "2025-01-14"
      }
    ],
    "total": 1
  }
}
```

### Create New Lead
```http
POST /api/v1/leads
```

**Request Body:**
```json
{
  "name": "Mike Johnson",
  "email": "mike@email.com",
  "phone": "(555) 987-6543",
  "project_type": "Kitchen Remodel",
  "budget_range": "$25k-$50k",
  "notes": "Looking to start in summer"
}
```

### Convert Lead to Job
```http
POST /api/v1/leads/{id}/convert
```

**Request Body:**
```json
{
  "address": "789 Pine St, Newtown, ST 11111",
  "start_date": "2025-04-01",
  "budget": 35000
}
```

## Documentation API

### Get Documents for Job
```http
GET /api/v1/jobs/{job_id}/documents
```

**Response:**
```json
{
  "success": true,
  "data": {
    "documents": [
      {
        "id": 1,
        "job_id": 1,
        "filename": "building_permit.pdf",
        "document_type": "permit",
        "upload_date": "2025-01-15",
        "file_size": 2048576,
        "url": "/api/v1/documents/1/download"
      }
    ]
  }
}
```

### Upload Document
```http
POST /api/v1/jobs/{job_id}/documents
```

**Request:** Multipart form data
- `file` - Document file
- `document_type` - Type: `permit`, `contract`, `photo`, `invoice`
- `description` - Optional description

### Download Document
```http
GET /api/v1/documents/{document_id}/download
```

## Reports API

### Get Dashboard Metrics
```http
GET /api/v1/reports/dashboard
```

**Query Parameters:**
- `period` (optional) - Time period: `30d`, `90d`, `1y` (default: 30d)

**Response:**
```json
{
  "success": true,
  "data": {
    "total_jobs": 23,
    "active_jobs": 8,
    "total_leads": 15,
    "revenue_ytd": 485250,
    "on_time_rate": 0.85,
    "conversion_rate": 0.20
  }
}
```

### Get Revenue Report
```http
GET /api/v1/reports/revenue
```

**Query Parameters:**
- `period` - Required: `monthly`, `quarterly`, `yearly`
- `year` (optional) - Specific year (default: current year)

**Response:**
```json
{
  "success": true,
  "data": {
    "period": "monthly",
    "year": 2025,
    "revenue": [
      {"month": "January", "amount": 78500},
      {"month": "February", "amount": 65200},
      {"month": "March", "amount": 82100}
    ],
    "total": 225800
  }
}
```

### Get Lead Conversion Report
```http
GET /api/v1/reports/conversion
```

**Response:**
```json
{
  "success": true,
  "data": {
    "funnel": {
      "total_leads": 45,
      "contacted": 28,
      "quoted": 15,
      "won": 9
    },
    "conversion_rate": 0.20,
    "avg_response_time": "4.2 hours"
  }
}
```

## Webhook Support

### Register Webhook
```http
POST /api/v1/webhooks
```

**Request Body:**
```json
{
  "url": "https://your-app.com/webhook",
  "events": ["job.created", "job.updated", "lead.created"],
  "secret": "your_webhook_secret"
}
```

### Webhook Events
- `job.created` - New job created
- `job.updated` - Job status or details changed
- `job.completed` - Job marked as completed
- `lead.created` - New lead added
- `lead.converted` - Lead converted to job
- `document.uploaded` - New document uploaded

## Rate Limits
- 100 requests per minute per API key
- 1000 requests per hour per API key
- Bulk operations limited to 50 items per request

## Error Codes

| Code | Description |
|------|-------------|
| 400 | Bad Request - Invalid input data |
| 401 | Unauthorized - Authentication required |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource doesn't exist |
| 409 | Conflict - Resource already exists |
| 422 | Unprocessable Entity - Validation failed |
| 429 | Too Many Requests - Rate limit exceeded |
| 500 | Internal Server Error - Server error |

## SDKs and Libraries

### Python SDK Example
```python
import contractorpro

client = contractorpro.Client(api_key='your_api_key')

# Create a new job
job = client.jobs.create({
    'client_name': 'John Doe',
    'project_type': 'Kitchen Remodel',
    'address': '123 Main St',
    'budget': 45000
})

# Get all leads
leads = client.leads.list(status='new')
```

### JavaScript SDK Example
```javascript
const ContractorPro = require('contractorpro-js');

const client = new ContractorPro({
  apiKey: 'your_api_key',
  baseUrl: 'http://localhost:5000/api/v1'
});

// Get jobs
const jobs = await client.jobs.list({ status: 'active' });

// Create lead
const lead = await client.leads.create({
  name: 'Jane Smith',
  email: 'jane@email.com',
  project_type: 'Bathroom Renovation'
});
```

## Testing

Use the provided Postman collection for API testing:
```
docs/ContractorPro_API.postman_collection.json
```

## Support

For API support:
- Email: api-support@contractorpro.com
- Documentation: https://docs.contractorpro.com
- Status Page: https://status.contractorpro.com

---

*API Version: 1.0 | Last Updated: January 2025*