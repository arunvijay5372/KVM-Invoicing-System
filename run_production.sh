#!/bin/bash
# Production startup script for KVM Invoicing System

# Set environment variables
export FLASK_ENV=production
export FLASK_APP=run.py

# Install dependencies
pip install -r requirements.txt

# Initialize database
python -c "from app import db, create_app; app = create_app(); app.app_context().push(); db.create_all(); print('Database initialized')"

# Start Gunicorn server
gunicorn --workers 4 --bind 0.0.0.0:5000 --timeout 120 --access-logfile - --error-logfile - run:app
