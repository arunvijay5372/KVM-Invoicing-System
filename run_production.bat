@echo off
REM Production startup script for KVM Invoicing System (Windows)

setlocal enabledelayedexpansion

REM Set environment variables
set FLASK_ENV=production
set FLASK_APP=run.py

echo Starting KVM Invoicing System in Production Mode...
echo.

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Initialize database
echo Initializing database...
python -c "from app import db, create_app; app = create_app(); app.app_context().push(); db.create_all(); print('Database initialized successfully')"

echo.
echo Starting Gunicorn server on http://0.0.0.0:5000
echo Press Ctrl+C to stop the server
echo.

REM Start Gunicorn server
gunicorn --workers 4 --bind 0.0.0.0:5000 --timeout 120 --access-logfile - --error-logfile - run:app

pause
