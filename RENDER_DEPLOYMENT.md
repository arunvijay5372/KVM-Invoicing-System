# Deployment Guide - Render

Follow these steps to deploy KVM Invoicing System on Render.

## Prerequisites
1. GitHub account (Render connects to GitHub repos)
2. Render account (signup at https://render.com)

## Step 1: Push Code to GitHub

```bash
# Initialize git (if not already done)
git init
git add .
git commit -m "Initial commit - KVM Invoicing System"

# Create new repo on GitHub, then:
git remote add origin https://github.com/YOUR-USERNAME/kvm-invoicing.git
git branch -M main
git push -u origin main
```

## Step 2: Create Render Account
1. Go to https://render.com
2. Sign up with GitHub
3. Click "New Web Service"

## Step 3: Connect GitHub Repository
1. Select "Connect a repository"
2. Choose your `kvm-invoicing` repository
3. Click "Connect"

## Step 4: Configure Render Settings

**Name:** kvm-invoicing  
**Environment:** Python 3  
**Region:** Choose closest to you (Singapore for India)  
**Build Command:** `pip install -r requirements.txt`  
**Start Command:** `gunicorn run:app`  

## Step 5: Add Environment Variables

Click "Advanced" and add:

| Key | Value |
|-----|-------|
| `FLASK_ENV` | `production` |
| `SECRET_KEY` | Generate a random string (Render can auto-generate) |
| `DATABASE_URL` | `sqlite:///kvm_inventory.db` |

## Step 6: Deploy
Click "Create Web Service"

Render will:
- Build the app
- Install dependencies
- Start the server
- Provide a live URL (e.g., `https://kvm-invoicing.onrender.com`)

## Step 7: Access Your App
- Your live website: `https://your-app-name.onrender.com`
- Default login: `admin` / `admin123`

## Important Notes

- **Free tier**: Service will sleep after 15 mins of inactivity. Upgrade to Paid for 24/7 uptime
- **Database**: Currently using SQLite (good for small usage). For production, upgrade to Render PostgreSQL
- **File Storage**: SQLite database resets on redeploy. Use Render PostgreSQL for production
- **Backups**: Download your database before major updates

## For Production Use (Recommended)

### Switch to PostgreSQL

1. In Render dashboard, create a new PostgreSQL database
2. Update environment variable:
   ```
   DATABASE_URL = postgresql://user:password@host:5432/dbname
   ```
3. Your data will persist across deploys

### Upgrade from Free Tier
- Free tier has limitations (15-min sleep, limited resources)
- Starter plan (~$7/month) for 24/7 uptime
- Better for production use

## Troubleshooting

**App won't start?**
- Check Build Logs in Render dashboard
- Ensure all dependencies in requirements.txt
- Check DATABASE_URL environment variable

**Database lost after deploy?**
- SQLite doesn't persist. Use PostgreSQL for data persistence
- Or add database backup before deploying

**Performance issues?**
- Upgrade to Paid tier for better resources
- Use PostgreSQL instead of SQLite

## File Structure Expected by Render

```
kvm-invoicing/
├── run.py (entry point)
├── Procfile
├── requirements.txt
├── config.py
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes/
│   ├── templates/
│   └── utils/
└── .gitignore
```

All set! Your app will be live within minutes on Render! 🚀
