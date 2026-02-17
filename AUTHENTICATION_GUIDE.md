# KVM Invoicing System - Authentication & Setup Guide

## Overview

The KVM Invoicing system now includes a complete user authentication system using Flask-Login. All users must log in to access the application, and customer data is now properly persisted.

## Initial Login Credentials

After setup, use these credentials to log in:

- **Username:** `admin`
- **Password:** `admin123`

⚠️ **IMPORTANT:** Change this password immediately after your first login!

## Features Implemented

### 1. User Authentication
- ✅ Login screen with form validation
- ✅ User registration with password confirmation
- ✅ Password hashing using Werkzeug (secure bcrypt)
- ✅ Session management with Flask-Login
- ✅ Automatic redirect to login for unauthenticated users
- ✅ Logout functionality

### 2. Protected Routes
All web routes now require authentication:
- Dashboard `/`
- Invoices `/invoices`
- Create Invoice `/invoices/new`
- View Invoice `/invoices/<id>`
- Inventory `/inventory`
- Brands `/brands`
- Customers `/customers`

### 3. Customer Management
- ✅ Fixed customer creation and persistence
- ✅ Added validation for customer names
- ✅ Proper error handling with user feedback
- ✅ Customers saved in database with all details:
  - Name (required)
  - GSTIN/Tax ID
  - Phone
  - Email
  - Address
  - City
  - State
  - Pincode

## Getting Started

### Step 1: Start the Application

```bash
cd c:\Users\server\Downloads\KVM
.venv\Scripts\python.exe run.py
```

The app will start at: `http://127.0.0.1:5000`

### Step 2: Access the Login Screen

Navigate to `http://127.0.0.1:5000` in your browser. You will be redirected to the login page.

### Step 3: Log In

Enter the credentials:
- Username: `admin`
- Password: `admin123`

### Step 4: Change Your Password

After logging in, it's recommended to register a new account with your preferred credentials and use that for future logins.

## Using the System

### Creating a Customer

1. Navigate to "Create Invoice" page (`/invoices/new`)
2. Click "Add New Customer" link below the customer selector
3. Fill in the customer details:
   - **Name** (required)
   - GSTIN (optional but recommended)
   - Phone
   - Email
   - Address
   - City
   - State
   - Pincode
4. Click "Save Customer"
5. The customer will be added to the database and appear in the customer dropdown

### Creating an Invoice

1. Navigate to "Create Invoice" (`/invoices/new`)
2. Select a customer from the dropdown
3. Add invoice items:
   - Select product
   - Specify quantity
   - Unit price
   - Discount percentage
4. System automatically calculates:
   - CGST (Central GST)
   - SGST (State GST)
   - Line totals
   - Grand total
5. Add optional notes
6. Click "Generate Invoice"

### Viewing Invoices

- Navigate to "Invoices" to see all invoices
- Click an invoice to view details
- Download or print invoices as needed

## API Endpoints Protected by Authentication

All API endpoints require the user to be logged in:

### Customers API
- `GET /api/customers` - Get all customers
- `POST /api/customers` - Create new customer (requires login)
- `PUT /api/customers/<id>` - Update customer (requires login)
- `DELETE /api/customers/<id>` - Delete customer (requires login)

### Invoices API
- `GET /api/invoices` - Get all invoices
- `POST /api/invoices` - Create new invoice (requires login)
- `PUT /api/invoices/<id>` - Update invoice (requires login)
- `DELETE /api/invoices/<id>` - Delete invoice (requires login)

### Products, Brands, Inventory APIs
- All protected with `@login_required` decorator
- Prevents unauthorized access to business data

## Files Modified/Created

### New Files
- **app/routes/auth.py** - Authentication routes (login, register, logout)
- **app/templates/login.html** - Login form page
- **app/templates/register.html** - User registration form
- **init_db.py** - Database initialization with admin user

### Modified Files
- **app/__init__.py** - Added LoginManager initialization
- **app/models.py** - Added User model with password hashing
- **app/routes/web.py** - Added @login_required to all routes
- **app/routes/api.py** - Added @login_required to protected endpoints
- **app/templates/base.html** - Added user dropdown menu with logout
- **app/templates/new_invoice.html** - Improved customer creation error handling
- **requirements.txt** - Added Flask-Login==0.6.3

## Technical Details

### User Model

The User model includes:
- UUID primary key
- Username (unique)
- Email (unique)
- Password hash (using Werkzeug's werkzeug.security)
- is_active flag
- Created timestamp

### Password Security

Passwords are hashed using Werkzeug's `generate_password_hash()` function, which uses industry-standard bcrypt hashing. Raw passwords are never stored in the database.

### Session Management

Flask-Login manages user sessions:
- Sessions are maintained via secure cookies
- Automatic timeout after inactivity
- Proper session cleanup on logout
- Next URL redirect after login (returns user to intended page)

## Troubleshooting

### "Invalid username or password"
- Check caps lock
- Ensure you're using the correct credentials
- If you forgot the admin password, delete `kvm_inventory.db` and re-run `init_db.py`

### Customer not saving
- Check browser console (F12) for JavaScript errors
- Verify you're logged in
- Ensure customer name is not empty
- Check if the customer name already exists

### "Unauthorized" or 401 error
- Your session may have expired
- Log out and log back in
- Clear browser cookies if issues persist

### "ModuleNotFoundError: No module named 'flask_login'"
- Install dependencies: `.venv\Scripts\python.exe -m pip install -r requirements.txt`
- Or install Flask-Login: `.venv\Scripts\python.exe -m pip install Flask-Login==0.6.3`

## Default Company Information

When creating invoices, the system uses these company details:

- **Company Name:** KVM Enterprises
- **Phone:** 9884243950
- **GSTIN:** 33EFMPS7293G1ZT
- **Address:** Hyderabad, India

These are configured in the templates and can be modified in `app/templates/` files.

## Security Recommendations

1. **Change Default Password**
   - Always change the admin password after first setup
   
2. **Use HTTPS in Production**
   - Flask default is HTTP only
   - Use a production WSGI server (Gunicorn) with HTTPS
   
3. **Database Security**
   - Backup `kvm_inventory.db` regularly
   - Store in secure location
   - Use PostgreSQL for production instead of SQLite

4. **User Management**
   - Create individual accounts for team members
   - Use strong passwords (8+ characters, mix of types)
   - Regularly review active users

## Deployment to Production

For production deployment:

```bash
# Install production dependencies
.venv\Scripts\python.exe -m pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 wsgi:app

# Or use the included run_production.sh script
bash run_production.sh
```

## Support

For issues or questions:
1. Check the browser console (F12) for JavaScript errors
2. Review Flask logs in the terminal
3. Verify all dependencies are installed: `pip list`
4. Ensure database is initialized: `python init_db.py`

## Next Steps

1. ✅ Log in with admin/admin123
2. ✅ Create a new customer
3. ✅ Create an invoice
4. ✅ Generate a PDF invoice
5. Change your password to something secure
6. Invite team members to register accounts

---

**Version:** 2.0 (with Authentication)
**Last Updated:** February 2026
**Company:** KVM Enterprises
