import os
import sys

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Brand, Variant, Size, Product, Inventory, Customer, Invoice, InvoiceItem

app = create_app(os.getenv('FLASK_ENV', 'development'))

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'Brand': Brand,
        'Variant': Variant,
        'Size': Size,
        'Product': Product,
        'Inventory': Inventory,
        'Customer': Customer,
        'Invoice': Invoice,
        'InvoiceItem': InvoiceItem
    }

@app.before_request
def initialize_db():
    """Initialize database on first request"""
    try:
        db.create_all()
    except Exception as e:
        print(f"Database initialization error: {e}")

if __name__ == '__main__':
    # For local development
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)
