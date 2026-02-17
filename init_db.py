#!/usr/bin/env python
"""
Initialize database with default brands and variants
Run this after first deployment
"""

from app import create_app, db
from app.models import Brand, Variant, Size, User
import os

def init_db():
    """Initialize database with sample data"""
    app = create_app(os.getenv('FLASK_ENV', 'development'))
    
    with app.app_context():
        # Create all tables
        db.create_all()
        print("✓ Database tables created")
        
        # Create default admin user if not exists
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            print("Creating default admin user...")
            admin = User(
                username='admin',
                email='admin@kvmenterprises.com'
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("✓ Admin user created (username: admin, password: admin123)")
            print("  WARNING: Change this password immediately after first login!")
        else:
            print("✓ Admin user already exists")
        
        # Check if brands already exist
        if Brand.query.first() is None:
            # Add default brands
            brands = [
                Brand(name='Finolex', code='FIN', description='Finolex Pipes'),
                Brand(name='Star', code='STR', description='Star Pipes'),
                Brand(name='Trubore', code='TRU', description='Trubore Pipes'),
                Brand(name='K-Star', code='KST', description='K-Star Pipes')
            ]
            db.session.add_all(brands)
            print("✓ Added default brands")
        
        # Check if variants already exist
        if Variant.query.first() is None:
            variants = [
                Variant(name='4kg', weight_kg=4.0),
                Variant(name='6kg', weight_kg=6.0)
            ]
            db.session.add_all(variants)
            print("✓ Added default variants")
        
        # Check if sizes already exist
        if Size.query.first() is None:
            sizes = [Size(size_inches=float(i)) for i in range(4, 13)]
            db.session.add_all(sizes)
            print("✓ Added default sizes (4\" to 12\")")
        
        db.session.commit()
        print("\n✓ Database initialization complete!")
        print("You can now:")
        print("  1. Add brands at /brands")
        print("  2. Add customers at /customers")
        print("  3. Update inventory at /inventory")
        print("  4. Create invoices at /invoices/new")

if __name__ == '__main__':
    init_db()
