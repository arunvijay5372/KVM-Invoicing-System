# KVM Enterprises - Complete Deployment Guide

## Table of Contents
1. [Local Development Setup](#local-development-setup)
2. [GitHub Repository Setup](#github-repository-setup)
3. [Render Deployment](#render-deployment)
4. [Post-Deployment Configuration](#post-deployment-configuration)
5. [Troubleshooting](#troubleshooting)

---

## Local Development Setup

### Step 1: Clone Repository
```bash
cd c:\Users\server\Downloads\KVM
```

### Step 2: Create Virtual Environment

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Create Environment File
```bash
copy .env.example .env
# Edit .env with your settings
```

### Step 5: Initialize Database
```bash
python init_db.py
```

Output should show:
```
✓ Database tables created
✓ Added default brands
✓ Added default variants
✓ Added default sizes (4" to 12")
✓ Database initialization complete!
```

### Step 6: Run Development Server
```bash
python run.py
```

Visit: `http://localhost:5000`

### Step 7: Add Initial Data

#### Option A: Using Web Interface
1. Go to `http://localhost:5000/brands`
2. Add brands (Finolex, Star, Trubore, K-Star)
3. Go to `http://localhost:5000/customers`
4. Add sample customers

#### Option B: Using API
```bash
# Add a brand
curl -X POST http://localhost:5000/api/brands \
  -H "Content-Type: application/json" \
  -d '{"name": "Finolex", "code": "FIN"}'

# Add a customer
curl -X POST http://localhost:5000/api/customers \
  -H "Content-Type: application/json" \
  -d '{"name": "John Customer", "phone": "9876543210", "city": "Chennai"}'
```

---

## GitHub Repository Setup

### Step 1: Create GitHub Repository

1. Go to github.com and log in
2. Click "+" → "New repository"
3. **Repository name**: `kvm-pipe-invoicing`
4. **Description**: `Pipe Inventory & Tax Invoice System for KVM Enterprises`
5. **Private**: Select based on preference
6. **Initialize**: Check "Add .gitignore" and select "Python"
7. Click "Create repository"

### Step 2: Initialize Local Git

```bash
cd c:\Users\server\Downloads\KVM

# Initialize git (if not already)
git init

# Add remote
git remote add origin https://github.com/YOUR-USERNAME/kvm-pipe-invoicing.git

# Set main branch
git branch -M main
```

### Step 3: Commit and Push

```bash
# Stage all files
git add .

# Create initial commit
git commit -m "Initial commit: KVM Pipe Invoicing System"

# Push to GitHub
git push -u origin main
```

### Step 4: Verify on GitHub

Visit: `https://github.com/YOUR-USERNAME/kvm-pipe-invoicing`

You should see all project files.

---

## Render Deployment

### Prerequisites
- Active GitHub account with repository
- Free Render account (render.com)

### Step 1: Create Render Account

1. Go to render.com
2. Click "Sign Up"
3. Choose "Sign up with GitHub"
4. Authorize Render to access your GitHub
5. Complete signup

### Step 2: Create Web Service

1. In Render Dashboard, click "New +"
2. Select "Web Service"
3. Select your `kvm-pipe-invoicing` repository
4. Click "Connect"

### Step 3: Configure Web Service

Fill in the form:

| Field | Value |
|-------|-------|
| **Name** | `kvm-pipe-invoicing` |
| **Environment** | `Python 3` |
| **Region** | Select closest to you |
| **Branch** | `main` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn run:app` |
| **Instance Type** | Free (or Starter) |

Click "Create Web Service"

### Step 4: Add Environment Variables

While the app is building:

1. Go to "Environment" tab
2. Click "Add Environment Variable"
3. Add these variables:

```
FLASK_ENV=production
SECRET_KEY=generate-random-string-here
DATABASE_URL=postgresql://user:pass@localhost/dbname
```

**For SECRET_KEY**, generate using:
```python
import secrets
secrets.token_hex(32)
```

### Step 5: Add PostgreSQL Database (Recommended)

For persistent data storage:

1. In Render Dashboard, click "New +"
2. Select "PostgreSQL"
3. Fill in:
   - **Name**: `kvm-pipe-invoicing-db`
   - **Database**: `kvm_db`
   - **User**: `kvm_user`
   - **Region**: Same as Web Service
4. Click "Create Database"

5. Copy the **Database URL** from the database dashboard
6. Add it as `DATABASE_URL` environment variable in Web Service

### Step 6: Monitor Deployment

1. Go to Web Service page
2. Click "Logs" to see build progress
3. Wait for message: "Deployed successfully"
4. Service URL: `https://kvm-pipe-invoicing.onrender.com`

### Step 7: Initialize Database on Render

Connect to Render console and run:

```bash
# Click "Shell" in Render dashboard
python
>>> from app import create_app, db
>>> from app.models import *
>>> app = create_app('production')
>>> with app.app_context():
...     db.create_all()
...     # Add initial brands
...     brands = [Brand(name='Finolex', code='FIN'),
...               Brand(name='Star', code='STR'),
...               Brand(name='Trubore', code='TRU'),
...               Brand(name='K-Star', code='KST')]
...     db.session.add_all(brands)
...     
...     # Add variants
...     variants = [Variant(name='4kg', weight_kg=4.0),
...                 Variant(name='6kg', weight_kg=6.0)]
...     db.session.add_all(variants)
...     
...     # Add sizes
...     sizes = [Size(size_inches=float(i)) for i in range(4, 13)]
...     db.session.add_all(sizes)
...     
...     db.session.commit()
>>> exit()
```

---

## Post-Deployment Configuration

### 1. Update DNS (Optional)

If you have a custom domain:

1. In Render, go to Web Service → Settings
2. Scroll to "Custom Domains"
3. Add your domain: `kvm-invoicing.com`
4. Add CNAME record to your domain DNS:
   - **Host**: `www`
   - **Value**: `kvm-pipe-invoicing.onrender.com`

### 2. Set Up SSL/TLS

Render automatically provides free SSL certificate.

### 3. Add Users to Authorized Access (Future)

When implementing authentication:
1. Create admin user
2. Set strong password
3. Add team members

### 4. Configure Email (Future)

For sending invoices via email:
1. Set up email service integration
2. Add SMTP credentials to environment variables

---

## Usage After Deployment

### Access Your Application

1. Visit: `https://kvm-pipe-invoicing.onrender.com`
2. Dashboard with statistics
3. Add brands, customers, products
4. Create invoices
5. Download PDFs

### First Time Setup

1. **Add Brands** → `/brands` → Click "Add Brand"
2. **Add Customers** → `/customers` → Click "Add Customer"
3. **Update Inventory** → `/inventory` → Click "Edit" for products
4. **Create Invoice** → Click "Create New Invoice" button
5. **Generate PDF** → After invoice creation, click "Download PDF"

---

## Troubleshooting

### Issue: Build fails with dependency errors

**Solution:**
```bash
# Local fix
pip install --upgrade pip
pip install -r requirements.txt

# Push fix
git add requirements.txt
git commit -m "Fix: Update dependencies"
git push origin main
# Render auto-redeploys
```

### Issue: Database not found on Render

**Solution:**
- Ensure PostgreSQL database is created
- Check `DATABASE_URL` is correct in environment variables
- Run initialization commands again

### Issue: PDF generation fails

**Solution:**
- Ensure reportlab is in requirements.txt
- Check file permissions in /tmp directory

### Issue: Invoice template not rendering

**Solution:**
- Clear browser cache (Ctrl+Shift+Delete)
- Check browser console for errors (F12)
- Verify all template files exist

### Issue: Static files not loading (CSS/JS)

**Solution:**
- Run: `flask --app run:app --static-folder=app/static`
- For Render, update Start Command if using static files

### Getting Help

For issues:
1. Check Render dashboard logs
2. Review Flask error messages
3. Contact support with error details

---

## Maintenance

### Regular Tasks

**Weekly:**
- Monitor low stock alerts on dashboard
- Review new invoices

**Monthly:**
- Backup database (if using PostgreSQL)
- Review application logs

**As Needed:**
- Add new brands/products
- Update inventory
- Export invoices

### Updating Application

```bash
# Make changes locally
git add .
git commit -m "Feature: Add new functionality"
git push origin main

# Render auto-redeploys within 1-2 minutes
```

### Backup Strategy

For PostgreSQL on Render:
1. Render provides automatic daily backups
2. Store backups separately for compliance
3. Keep invoice PDFs in secure location

---

## Production Checklist

- [x] Repository on GitHub
- [x] Environment variables configured
- [x] PostgreSQL database connected
- [x] SSL certificate active
- [x] Database initialized with brands/variants/sizes
- [x] Test invoice creation and PDF generation
- [x] Test inventory management
- [x] Mobile responsive design verified
- [x] Backup strategy in place

---

## Support & Contact

**Company**: KVM Enterprises
**Phone**: 9884243950
**Business Hours**: Mon-Fri, 10 AM - 6 PM IST

For technical support, include:
- Error message/screenshot
- What action caused the issue
- Browser and OS information

---

**Last Updated**: February 2026
**Version**: 1.0.0
