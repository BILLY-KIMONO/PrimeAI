# 🚀 Render.com Deployment - Step by Step Guide

## ✅ STEP 1: Prepare Your Code

```bash
cd /home/bill-fardan/PrimeAI

# Run setup script
bash setup-render.sh

# Commit and push
git commit -m "Add Render deployment configuration"
git push
```

---

## 🌐 STEP 2: Sign Up on Render (if not done)

1. Go to **https://render.com**
2. Click **"Sign up"** (top right)
3. Choose **"Sign up with GitHub"**
4. Authorize Render to access your GitHub account
5. You'll be redirected to your dashboard

---

## 📦 STEP 3: Create Web Service

1. On Render dashboard, click **"New +"** (top right)
   
   ![Dashboard Home](https://render.com/images/docs/dashboard.jpg)

2. Select **"Web Service"**

3. You'll see "Create a new Web Service" page

---

## 📋 STEP 4: Connect GitHub Repository

1. Under **"GitHub"** section, click **"Connect account"** if not connected
   - Or it will show your repositories if already connected

2. Find and click on **`BILLY-KIMONO/PrimeAI`** repository

3. Click **"Connect"** next to it

   ![Connect Repo](https://api.render.com/docs/images/web-service-settings.png)

---

## ⚙️ STEP 5: Configure Service Settings

**On the next page, fill in these fields:**

### **Name**
```
primeai-backend
```

### **Environment**
```
Python 3
```

### **Region**
```
Oregon (US West) [or your preferred region]
```

### **Branch**
```
main
```

### **Build Command**
```
pip install -r backend/requirements.txt
```

### **Start Command**
```
cd backend && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### **Instance Type**
```
Free (at bottom, select Free tier)
```

---

## 🔐 STEP 6: Add Environment Variables

Scroll down to **"Environment Variables"** section

Click **"Add Environment Variable"** for each:

| Variable | Value |
|----------|-------|
| `DATABASE_URL` | `postgresql://primeai:YOUR_DB_PASS@localhost/primeai` |
| `JWT_SECRET_KEY` | `your-super-secret-key-minimum-32-chars-long` |
| `PAYPAL_CLIENT_ID` | `your-paypal-client-id` |
| `PAYPAL_CLIENT_SECRET` | `your-paypal-secret` |
| `PAYPAL_MERCHANT_EMAIL` | `billykimono@gmail.com` |
| `MPESA_CONSUMER_KEY` | `your-mpesa-key` |
| `MPESA_CONSUMER_SECRET` | `your-mpesa-secret` |
| `FRONTEND_URL` | `https://your-frontend-url.vercel.app` |
| `API_URL` | `https://primeai-backend.render.com` |
| `ENVIRONMENT` | `production` |

**Important: For DATABASE_URL, Render will provide it automatically. Keep it for now.**

---

## 💾 STEP 7: Create Database

1. Scroll to bottom, look for **"Database"** section
2. You might need a different approach - Render has separate database management

**Instead, do this:**

1. Click **"Create"** button at bottom to create the service first
2. After service is created, click **"Dashboard"**
3. Click the **"PostgreSQL"** icon on left sidebar
4. Click **"New Database"** / **"New PostgreSQL"**
5. Configure:
   - **Name**: `primeai-postgres`
   - **Region**: `Oregon` (same as backend)
   - **Plan**: `Free`
6. Click **"Create"**
7. After creation, copy the **"Internal Database URL"**
8. Go back to Web Service settings
9. Update `DATABASE_URL` with this new URL

---

## ✅ STEP 8: Review and Deploy

1. Review all settings
2. Click **"Create Web Service"** button (blue button at bottom right)
3. Render will show a **"Building..."** message
4. Wait for build to complete (usually 2-3 minutes)
5. Check **"Events"** tab to see build logs

---

## 🎯 STEP 9: Get Your Live URL

After deployment completes:

1. At the top of service page, you'll see a URL like:
   ```
   https://primeai-backend.render.com
   ```

2. Test it:
   ```bash
   curl https://primeai-backend.render.com/health
   # Should return: {"status":"ok"}
   ```

3. Save this URL - you'll need it for your frontend

---

## 🗄️ STEP 10: Initialize Database

1. SSH into your service (click **"Shell"** tab in Render dashboard)

2. Run:
   ```bash
   python backend/init_db.py
   ```

3. You should see:
   ```
   ✅ Database initialized successfully!
   Tables created:
     - users
     - subscriptions
     - device_profiles
     - payments
   ```

---

## 🧪 STEP 11: Test Your API

Once deployed, test these endpoints:

### Health Check:
```bash
curl https://primeai-backend.render.com/health
```

### Register User:
```bash
curl -X POST https://primeai-backend.render.com/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@primeai.com",
    "username": "testuser",
    "password": "Test@123456"
  }'
```

### Login:
```bash
curl -X POST https://primeai-backend.render.com/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "Test@123456"
  }'
```

### Get Pricing:
```bash
curl https://primeai-backend.render.com/api/payments/pricing
```

---

## 📱 STEP 12: Deploy Frontend

Now deploy your frontend to Netlify or Vercel:

### Option A: Netlify
```bash
npm install -g netlify-cli
cd /home/bill-fardan/PrimeAI/frontend
netlify deploy --prod --dir=.
```

### Option B: Vercel
```bash
npm install -g vercel
cd /home/bill-fardan/PrimeAI/frontend
vercel --prod
```

---

## 🔗 STEP 13: Connect Frontend to Backend

In your frontend code (HTML/JS), update the API base URL:

```javascript
// Change from:
const API_URL = 'http://localhost:8000/api';

// To:
const API_URL = 'https://primeai-backend.render.com/api';
```

Then update environment variables in frontend deployment platform.

---

## ✨ Final Checklist

- [ ] Render account created
- [ ] Web Service deployed
- [ ] PostgreSQL database created
- [ ] Environment variables added
- [ ] Database tables initialized
- [ ] Backend health check passes
- [ ] User registration works
- [ ] Frontend deployed
- [ ] Frontend connected to backend
- [ ] Can login and access dashboard

---

## 🆘 Troubleshooting

### "Build Failed"
- Check **Events** tab for error messages
- Verify `render.yaml` is correctly formatted
- Ensure `requirements.txt` is in backend folder

### "Database Connection Error"
- Verify DATABASE_URL is correct
- Check database is created and running
- Run `init_db.py` in Shell tab

### "502 Bad Gateway"
- Wait 1-2 minutes for service to start
- Check **Logs** tab for errors
- Restart service: Click "Manual Deploy" button

### "Module Not Found"
- Verify `requirements.txt` has all dependencies
- Redeploy by clicking "Manual Deploy"

### "Cannot connect to frontend"
- Update API URL in frontend code
- Redeploy frontend
- Check browser console for CORS errors

---

## 💡 Pro Tips

1. **Auto-deploy**: Everytime you push to GitHub, Render auto-deploys
   ```bash
   git commit -m "Update feature"
   git push  # Auto-deploys!
   ```

2. **View logs**: Click **"Logs"** tab to see real-time logs

3. **Database backup**: Go to PostgreSQL settings and enable auto-backup

4. **Add domain**: In **"Settings"**→**"Custom Domain"**, add your own domain

5. **Monitor**: Click **"Metrics"** to see CPU, memory, requests

---

## 📊 Your Deployed Stack

```
┌─────────────────────────────────────┐
│   Frontend (Netlify/Vercel)         │
│   primeai.vercel.app               │
└──────────────┬──────────────────────┘
               │ HTTP
               ▼
┌─────────────────────────────────────┐
│   Backend API (Render)              │
│   primeai-backend.render.com        │
└──────────────┬──────────────────────┘
               │ Connection
               ▼
┌─────────────────────────────────────┐
│   PostgreSQL (Render)               │
│   primeai-postgres.render.com       │
└─────────────────────────────────────┘
```

---

## 🎉 You're Live!

Your PrimeAI backend is now live on the internet!

**Next Steps:**
1. Deploy frontend
2. Test full user flow
3. Configure payment credentials
4. Submit browser extension to stores
5. Celebrate! 🚀

---

**Questions?** Check:
- Render Docs: https://render.com/docs
- FastAPI Docs: https://fastapi.tiangolo.com
- Our API: https://your-backend.render.com/docs

