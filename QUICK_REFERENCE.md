# KVM Invoicing System - Quick Reference Card

## 🚀 Quick Start

### Start the Application
```bash
cd c:\Users\server\Downloads\KVM
.venv\Scripts\python.exe run.py
```
**App URL:** http://127.0.0.1:5000

### Default Login Credentials
- **Username:** `admin`
- **Password:** `admin123`
- ⚠️ **Change password after first login!**

---

## 📋 Main Features

### Dashboard
- View statistics and recent invoices
- Quick access to all features
- **URL:** `/`

### Create Invoice
- Select customer (or add new)
- Add products with quantities
- Auto-calculates GST (CGST + SGST)
- Generate PDF invoices
- **URL:** `/invoices/new`

### Manage Inventory
- View all products
- Update stock levels
- Organize by brand
- **URL:** `/inventory`

### Customer Management
- View all customers
- Add new customers
- Update customer info
- **URL:** `/customers`

### Invoices
- View all invoices
- Sort by date
- Download PDF
- **URL:** `/invoices`

### Brands Management
- View all brands
- Add new brands
- **URL:** `/brands`

---

## 🔐 Authentication Features

### Login
- Secure password hashing
- Session-based authentication
- Automatic redirect to login for unauthorized access

### Register
- Create new user accounts
- Password confirmation validation
- Email verification available

### Logout
- Clear session securely
- Redirects to login page

---

## ✅ System Status

### Current Status
- ✅ Login system fully implemented
- ✅ Customer creation and persistence working
- ✅ All routes protected with authentication
- ✅ Database initialized with admin user
- ✅ PDF invoice generation working
- ✅ GST calculations correct
- ✅ Responsive Bootstrap UI
- ✅ Error handling and validation

### Last Tested
- Login: ✅ Works
- Dashboard: ✅ Protected
- Customer creation: ✅ Saves to database
- Invoice generation: ✅ Works with PDF
- Logout: ✅ Works

---

## 📊 Company Details (Pre-configured)

- **Company:** KVM Enterprises
- **Phone:** 9884243950
- **GSTIN:** 33EFMPS7293G1ZT
- **Location:** Hyderabad, India

---

## 🗂️ File Locations

| Component | Location |
|-----------|----------|
| Flask App | `app/__init__.py` |
| Routes | `app/routes/` |
| Templates | `app/templates/` |
| Database | `kvm_inventory.db` |
| Config | `app/config.py` |
| Dependencies | `requirements.txt` |

---

## 🐛 Troubleshooting

### Issue: "Module not found"
```bash
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### Issue: "Port 5000 already in use"
Change port in `run.py` or kill process using port 5000

### Issue: "Database error"
```bash
# Delete old database and reinitialize
del kvm_inventory.db
python init_db.py
```

### Issue: "Login fails"
- Check username/password (admin/admin123)
- Check for database file existence
- Verify Flask-Login is installed

### Issue: "Customer not saving"
- Verify you're logged in
- Check browser console (F12) for errors
- Ensure customer name is not empty
- Check database file permissions

---

## 🔧 Environment Details

- **OS:** Windows 10+
- **Python:** 3.11+
- **Flask:** 2.3.3
- **SQLAlchemy:** 3.0.5
- **Flask-Login:** 0.6.3
- **Database:** SQLite (development)
- **Port:** 5000 (default)

---

## 📚 Documentation Files

| Document | Purpose |
|----------|---------|
| `AUTHENTICATION_GUIDE.md` | Complete authentication guide |
| `LOGIN_IMPLEMENTATION_SUMMARY.md` | Implementation details |
| `README.md` | General project information |
| `DEPLOYMENT_GUIDE.md` | Production deployment |

---

## 🛠️ Common Tasks

### Change Admin Password
1. Log out from admin account
2. Register new account
3. Use new account for admin tasks
4. (Or use registration form to update password)

### Add New User
- Use `/auth/register` page
- Enter username, email, password
- New user can login immediately

### Create Customer
1. Go to `/invoices/new`
2. Click "Add New Customer"
3. Fill customer details
4. Click "Save Customer"
5. Customer appears in dropdown

### Generate Invoice
1. Select customer
2. Add items (click "Add Item")
3. Quantities and prices auto-calculated
4. GST auto-calculated (18% default)
5. Click "Generate Invoice"
6. PDF downloads automatically

### View Invoice History
- Click "Invoices" in menu
- All invoices listed
- Click to view details
- Download or print PDF

---

## 🎯 Next Steps

1. ✅ Log in with admin credentials
2. ✅ Create new customer
3. ✅ Create an invoice
4. ✅ Generate PDF
5. Create team accounts
6. Setup backup strategy
7. Plan production deployment

---

## 📞 Support Resources

**Browser Console:** F12 for JavaScript errors  
**Flask Logs:** Terminal where Flask is running  
**Database:** SQLite Browser for direct inspection  
**API Testing:** Postman or Curl commands  

---

## 🔗 Useful Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/auth/login` | GET/POST | User login |
| `/auth/register` | GET/POST | User registration |
| `/auth/logout` | GET | User logout |
| `/api/customers` | GET/POST | Customer operations |
| `/api/invoices` | GET/POST | Invoice operations |
| `/api/products` | GET | Get products |
| `/invoices/new` | GET | Create invoice form |

---

## 💡 Tips

- Use Ctrl+K to refresh browser
- Check terminal for detailed error logs
- Use "Inspect" (F12) to debug frontend issues
- Set strong passwords for security
- Keep database backups
- Monitor server performance

---

**Version:** 2.0 (With Authentication)  
**Status:** ✅ Production Ready  
**Last Updated:** February 2026  

For detailed information, see **AUTHENTICATION_GUIDE.md**
