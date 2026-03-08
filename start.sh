#!/bin/bash
# Railway startup script for ContractorPro

# Initialize database if it doesn't exist
python migrate.py init || true

# Start the application with gunicorn
gunicorn app:app --bind 0.0.0.0:${PORT:-8000} --workers 2 --timeout 120
