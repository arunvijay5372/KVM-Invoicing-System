import os
import sys

# Get the directory where this file is located
base_dir = os.path.dirname(os.path.abspath(__file__))

# Add to Python path
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

# Import and create the app
from app import create_app, db

# Create the Flask app
app = create_app(os.getenv('FLASK_ENV', 'production'))

if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
