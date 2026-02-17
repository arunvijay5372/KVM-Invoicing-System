# Quick Start Guide - KVM Pipe Invoicing System

## 🚀 Get Started in 5 Minutes

### Local Development

**Windows Users:**
```bash
# 1. Navigate to project
cd c:\Users\server\Downloads\KVM

# 2. Create & activate virtual environment
python -m venv .venv
.venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Initialize database
python init_db.py

# 5. Run application
python run.py
```

Visit: http://localhost:5000

---

## 📋 First Time Setup

After running the app:

1. **Add Brands** (if not auto-added)
   ```
   http://localhost:5000/brands → Click "Add Brand"
   ```

2. **Add a Customer**
   ```
   http://localhost:5000/customers → Click "Add Customer"
   ```

3. **Create First Invoice**
   ```
   http://localhost:5000/invoices/new → Select customer → Add items → Submit
   ```

4. **Download PDF**
   ```
   View invoice → Click "Download PDF"
   ```

---

## 🌐 Deploy to Render

### 1. Push to GitHub
```bash
git add .
git commit -m "Initial commit"
git push origin main
```

### 2. Create Render Account
Visit: https://render.com (Sign up with GitHub)

### 3. Create Web Service
- Click "New +" → "Web Service"
- Connect your GitHub repository
- Set Name: `kvm-pipe-invoicing`
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn run:app`

### 4. Add Environment Variables
- `FLASK_ENV=production`
- `SECRET_KEY=<random-secret>`
- `DATABASE_URL=<postgres-url>`

### 5. Add PostgreSQL Database (Recommended)
- Click "New +" → "PostgreSQL"
- Connect to Web Service

### 6. Deploy & Access
- Wait for build to complete
- Access: `https://kvm-pipe-invoicing.onrender.com`

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed steps.

---

## 🎯 Main Features

| Feature | Location |
|---------|----------|
| Dashboard | `/` |
| Manage Inventory | `/inventory` |
| Create Invoices | `/invoices/new` |
| View All Invoices | `/invoices` |
| Manage Brands | `/brands` |
| Manage Customers | `/customers` |

---

## 📊 API Endpoints

```bash
# Get all products
curl http://localhost:5000/api/products

# Create customer
curl -X POST http://localhost:5000/api/customers \
  -H "Content-Type: application/json" \
  -d '{"name": "ABC Company", "phone": "9876543210"}'

# Create invoice
curl -X POST http://localhost:5000/api/invoices \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "xxx",
    "items": [
      {"product_id": "yyy", "quantity": 10, "unit_price": 500}
    ]
  }'

# Download invoice PDF
curl http://localhost:5000/api/invoices/<invoice_id>/pdf -o invoice.pdf
```

---

## 🐛 Common Issues

**Database Error?**
```bash
rm kvm_inventory.db
python init_db.py
```

**Port already in use?**
```bash
python run.py --port 5001
```

**Missing dependencies?**
```bash
pip install -r requirements.txt --upgrade
```

---

## 📁 Project Structure

```
KVM/
├── app/
│   ├── models.py          → Database models
│   ├── routes/
│   │   ├── api.py         → REST API
│   │   └── web.py         → Web pages
│   ├── templates/         → HTML pages
│   └── utils/
│       └── pdf_generator.py → PDF creation
├── run.py                 → Start application
├── config.py              → Configuration
├── requirements.txt       → Dependencies
├── Procfile              → Render config
├── DEPLOYMENT_GUIDE.md   → Detailed deployment
└── README.md             → Full documentation
```

---

## 💡 Tips

- Use CSV import at `/inventory` for bulk uploads
- Invoice PDF template matches your original invoice
- All data is protected with automatic backups (Render PostgreSQL)
- System supports 4 brands × 2 variants × 9 sizes = up to 72 products per brand

---

## ❓ Need Help?

1. Check README.md for detailed documentation
2. Review DEPLOYMENT_GUIDE.md for deployment issues
3. Contact: 9884243950

---

**Version**: 1.0.0 | **Last Updated**: February 2026
