#!/usr/bin/env python
"""
Verify KVM Pipe Invoicing System Setup
Run this to ensure everything is configured correctly
"""

import os
import sys
from pathlib import Path

def check_python_version():
    """Check Python version"""
    print("📌 Checking Python Version...", end=" ")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"✗ Python 3.8+ required (found {version.major}.{version.minor})")
        return False

def check_virtual_env():
    """Check if virtual environment is active"""
    print("📌 Checking Virtual Environment...", end=" ")
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✓ Virtual environment active")
        return True
    else:
        print("⚠ Virtual environment not detected (recommended for production)")
        return True

def check_requirements():
    """Check if all required packages are installed"""
    print("📌 Checking Required Packages...")
    required = [
        'flask',
        'flask_sqlalchemy',
        'flask_migrate',
        'reportlab',
        'werkzeug',
        'gunicorn'
    ]
    
    missing = []
    for package in required:
        try:
            __import__(package.replace('-', '_'))
            print(f"  ✓ {package}")
        except ImportError:
            print(f"  ✗ {package} - MISSING")
            missing.append(package)
    
    return len(missing) == 0, missing

def check_env_file():
    """Check if .env file exists"""
    print("📌 Checking Environment File...", end=" ")
    if os.path.exists('.env'):
        print("✓ .env file found")
        return True
    elif os.path.exists('.env.example'):
        print("⚠ .env not found, but .env.example exists")
        print("   Run: copy .env.example .env")
        return False
    else:
        print("✗ .env file not found")
        return False

def check_database():
    """Check database connection"""
    print("📌 Checking Database...")
    try:
        from app import create_app, db
        app = create_app()
        with app.app_context():
            # Try to query
            from app.models import Brand
            Brand.query.first()
        print("  ✓ Database connection successful")
        return True
    except Exception as e:
        print(f"  ✗ Database error: {str(e)}")
        return False

def check_models():
    """Check if all models are defined"""
    print("📌 Checking Database Models...")
    try:
        from app.models import (
            Brand, Variant, Size, Product, Inventory,
            Customer, Invoice, InvoiceItem
        )
        models = ['Brand', 'Variant', 'Size', 'Product', 'Inventory',
                 'Customer', 'Invoice', 'InvoiceItem']
        for model in models:
            print(f"  ✓ {model}")
        return True
    except ImportError as e:
        print(f"  ✗ Model import error: {str(e)}")
        return False

def check_routes():
    """Check if routes are registered"""
    print("📌 Checking Routes...")
    try:
        from app import create_app
        app = create_app()
        
        routes = {
            '/ (Dashboard)': '/',
            'Inventory': '/inventory',
            'Invoices': '/invoices',
            'New Invoice': '/invoices/new',
            'Brands': '/brands',
            'Customers': '/customers',
            'API Brands': '/api/brands',
            'API Products': '/api/products',
            'API Invoices': '/api/invoices',
        }
        
        app_routes = [str(rule) for rule in app.url_map.iter_rules()]
        
        for name, route in routes.items():
            if route in app_routes:
                print(f"  ✓ {name}")
            else:
                print(f"  ✗ {name} - NOT FOUND")
        return True
    except Exception as e:
        print(f"  ✗ Route check error: {str(e)}")
        return False

def check_templates():
    """Check if all templates exist"""
    print("📌 Checking Templates...")
    templates = [
        'base.html',
        'index.html',
        'inventory.html',
        'invoices.html',
        'new_invoice.html',
        'view_invoice.html',
        'brands.html',
        'customers.html'
    ]
    
    missing = []
    for template in templates:
        path = f'app/templates/{template}'
        if os.path.exists(path):
            print(f"  ✓ {template}")
        else:
            print(f"  ✗ {template} - NOT FOUND")
            missing.append(template)
    
    return len(missing) == 0

def check_config_files():
    """Check if config files exist"""
    print("📌 Checking Configuration Files...")
    files = {
        'requirements.txt': 'Dependency list',
        'Procfile': 'Render deployment config',
        'runtime.txt': 'Python version',
        'config.py': 'Flask configuration',
        'run.py': 'Application entry point',
        'init_db.py': 'Database initialization',
        'README.md': 'Documentation',
        'DEPLOYMENT_GUIDE.md': 'Deployment instructions'
    }
    
    missing = []
    for filename, description in files.items():
        if os.path.exists(filename):
            print(f"  ✓ {filename} - {description}")
        else:
            print(f"  ✗ {filename} - NOT FOUND")
            missing.append(filename)
    
    return len(missing) == 0

def print_summary(results):
    """Print summary of checks"""
    print("\n" + "="*50)
    print("SETUP VERIFICATION SUMMARY")
    print("="*50)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for check, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {check}")
    
    print("="*50)
    print(f"Total: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n🎉 All checks passed! Ready to deploy!")
        print("\nNext steps:")
        print("1. Run: python run.py")
        print("2. Visit: http://localhost:5000")
        print("3. Add brands, customers, and products")
        print("4. Create your first invoice!")
    else:
        print("\n⚠️  Some checks failed. Fix the issues above before deploying.")
    
    return passed == total

def main():
    """Run all checks"""
    print("="*50)
    print("KVM PIPE INVOICING SYSTEM - SETUP VERIFICATION")
    print("="*50 + "\n")
    
    results = {}
    
    # Run checks
    results['Python Version'] = check_python_version()
    results['Virtual Environment'] = check_virtual_env()
    
    pkg_ok, missing = check_requirements()
    results['Required Packages'] = pkg_ok
    if missing:
        print(f"\n  Install missing packages with:")
        print(f"  pip install {' '.join(missing)}\n")
    
    results['.env File'] = check_env_file()
    results['Database'] = check_database()
    results['Models'] = check_models()
    results['Routes'] = check_routes()
    results['Templates'] = check_templates()
    results['Config Files'] = check_config_files()
    
    # Print summary
    return print_summary(results)

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
