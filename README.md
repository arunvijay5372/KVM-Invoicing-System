# KVM Enterprises - Pipe Inventory & Invoicing System

A Flask-based web application for managing pipe inventory and generating GST tax invoices for borewell pipe business.

## Features

- **Inventory Management**: Track stock levels for different pipe brands, variants, and sizes
- **Multi-Brand Support**: Support for Finolex, Star, Trubore, K-Star with extensibility for more brands
- **Product Variants**: Each brand has 4kg and 6kg variants with sizes from 4" to 12"
- **Tax Invoicing**: Generate professional GST-compliant tax invoices
- **Customer Management**: Maintain customer database with GSTIN
- **Bulk Inventory Upload**: CSV upload for batch inventory updates
- **PDF Generation**: Download invoices as professional PDFs
- **Dashboard**: Real-time statistics and insights

## Technology Stack

- **Backend**: Flask (Python web framework)
- **Database**: SQLAlchemy ORM with SQLite (dev) / PostgreSQL (production)
- **Frontend**: Bootstrap 5, HTML, CSS, JavaScript
- **PDF Generation**: ReportLab
- **Deployment**: Gunicorn + Render

## Installation

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd KVM
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   
   # On Windows
   .venv\Scripts\activate
   
   # On Linux/Mac
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables**
   ```bash
   # Create .env file
   cp .env.example .env
   
   # Edit .env and set:
   FLASK_ENV=development
   SECRET_KEY=your-secret-key-here
   DATABASE_URL=sqlite:///kvm_inventory.db
   ```

5. **Initialize database**
   ```bash
   python
   >>> from app import create_app, db
   >>> app = create_app()
   >>> with app.app_context():
   >>>     db.create_all()
   >>> exit()
   ```

6. **Load initial data** (optional)
   ```python
   # Run in Python shell to add initial brands and variants
   python
   >>> from app import create_app, db
   >>> from app.models import Brand, Variant, Size
   >>> app = create_app()
   >>> with app.app_context():
   ...     # Add brands
   ...     brands = [
   ...         Brand(name='Finolex', code='FIN'),
   ...         Brand(name='Star', code='STR'),
   ...         Brand(name='Trubore', code='TRU'),
   ...         Brand(name='K-Star', code='KST')
   ...     ]
   ...     db.session.add_all(brands)
   ...     
   ...     # Add variants
   ...     variants = [
   ...         Variant(name='4kg', weight_kg=4.0),
   ...         Variant(name='6kg', weight_kg=6.0)
   ...     ]
   ...     db.session.add_all(variants)
   ...     
   ...     # Add sizes
   ...     sizes = [Size(size_inches=float(i)) for i in range(4, 13)]
   ...     db.session.add_all(sizes)
   ...     
   ...     db.session.commit()
   ...     print('Initial data loaded')
   >>> exit()
   ```

7. **Run development server**
   ```bash
   python run.py
   ```
   Access at `http://localhost:5000`

## API Endpoints

### Brands
- `GET /api/brands` - Get all brands
- `POST /api/brands` - Create brand
- `GET /api/brands/<id>` - Get specific brand
- `PUT /api/brands/<id>` - Update brand
- `DELETE /api/brands/<id>` - Delete brand

### Products
- `GET /api/products` - Get all products
- `POST /api/products` - Create product
- `GET /api/products/<id>` - Get specific product
- `PUT /api/products/<id>` - Update product

### Inventory
- `GET /api/inventory` - Get all inventory
- `PUT /api/inventory/<product_id>` - Update inventory
- `POST /api/inventory/upload` - Bulk upload inventory (CSV)

### Customers
- `GET /api/customers` - Get all customers
- `POST /api/customers` - Create customer
- `PUT /api/customers/<id>` - Update customer

### Invoices
- `GET /api/invoices` - Get all invoices
- `POST /api/invoices` - Create invoice
- `GET /api/invoices/<id>` - Get invoice details
- `GET /api/invoices/<id>/pdf` - Download invoice PDF
- `PUT /api/invoices/<id>` - Update invoice status

### Dashboard
- `GET /api/dashboard` - Get dashboard statistics

## File Structure

```
KVM/
├── app/
│   ├── __init__.py           # App factory
│   ├── models.py             # Database models
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── api.py            # REST API endpoints
│   │   └── web.py            # Web routes
│   ├── templates/            # HTML templates
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── inventory.html
│   │   ├── invoices.html
│   │   ├── new_invoice.html
│   │   ├── view_invoice.html
│   │   ├── brands.html
│   │   └── customers.html
│   └── utils/
│       ├── __init__.py
│       └── pdf_generator.py  # PDF invoice generation
├── config.py                 # Configuration
├── run.py                    # Application entry point
├── requirements.txt          # Python dependencies
├── Procfile                  # Render deployment config
├── runtime.txt              # Python version for Render
├── .env.example             # Environment variables template
└── README.md                # This file
```

## Deployment on Render

### Prerequisites
- GitHub account with repository
- Render account (render.com)

### Steps

1. **Push code to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Create Render Web Service**
   - Go to render.com and sign in
   - Click "New +"
   - Select "Web Service"
   - Connect your GitHub repository
   - Select the repository and branch

3. **Configure Service**
   - **Name**: `kvm-pipe-invoicing` (or your preferred name)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn run:app`

4. **Set Environment Variables**
   - Click "Environment" tab
   - Add the following variables:
     ```
     FLASK_ENV=production
     SECRET_KEY=<generate-a-strong-random-key>
     DATABASE_URL=<postgresql-url-from-render>
     ```

5. **Add PostgreSQL Database (Optional but Recommended)**
   - Click "New +"
   - Select "PostgreSQL"
   - Connect to your web service
   - The `DATABASE_URL` will be automatically set

6. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment to complete
   - Your app will be live at `https://kvm-pipe-invoicing.onrender.com`

### Important Notes for Render Deployment

- The app uses SQLite by default, which won't persist data on Render (serverless)
- **Recommended**: Use PostgreSQL for production
- Environment variables must be set in Render dashboard
- The app automatically creates tables on first run using SQLAlchemy

### Post-Deployment

After deployment, initialize the database:

1. Use Render's shell or create an initialization script
2. Or add initial brands/variants/sizes through the API

## Usage Guide

### Creating Your First Invoice

1. **Add Brands** (if not already added)
   - Go to Brands page
   - Click "Add Brand"
   - Enter name, code, description
   - Save

2. **Add Customers**
   - Go to Customers page
   - Click "Add Customer"
   - Fill in customer details
   - Save

3. **Update Inventory**
   - Go to Inventory page
   - Click "Edit" for each product
   - Update quantity and reorder level
   - Or use "Bulk Upload" with CSV

4. **Create Invoice**
   - Click "Create New Invoice" from dashboard
   - Select customer
   - Add items (select product, quantity, price)
   - Review totals
   - Click "Generate Invoice"

5. **Download PDF**
   - On invoice view, click "Download PDF"
   - Professional invoice PDF ready for sending

## CSV Format for Bulk Inventory Upload

```csv
product_id,quantity
550e8400-e29b-41d4-a716-446655440000,100
550e8400-e29b-41d4-a716-446655440001,75
```

## Troubleshooting

### Port 5000 already in use
```bash
python run.py --port 5001
```

### Database not initializing
```bash
rm kvm_inventory.db  # Delete the database file
python run.py        # Run to recreate
```

### Import errors
```bash
pip install -r requirements.txt --upgrade
```

### PDF generation issues
Ensure reportlab is installed:
```bash
pip install reportlab==4.0.4
```

## Future Enhancements

- [ ] User authentication & authorization
- [ ] Email invoice delivery
- [ ] Payment gateway integration
- [ ] Advance inventory analytics
- [ ] Multi-warehouse support
- [ ] Automated reorder notifications
- [ ] Mobile app

## Support

For issues or questions, please contact:
- **Phone**: 9884243950
- **Email**: admin@kvmenterprises.com

## License

This project is proprietary software for KVM Enterprises.

## Version

Current Version: 1.0.0
Last Updated: 2026
