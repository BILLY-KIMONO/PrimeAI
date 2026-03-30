# Quick Reference: Render Deployment Steps

## 🎯 Immediate Next Steps (Right Now)

1. **Commit new files:**
   ```bash
   cd /home/bill-fardan/PrimeAI
   git add render.yaml backend/Procfile RENDER_DEPLOY_STEPS.md
   git commit -m "Add Render deployment configuration"
   git push
   ```

2. **Go to Render Dashboard:**
   - URL: https://render.com/dashboard
   - Click **"New +"** button (top right)
   - Select **"Web Service"**

3. **Connect GitHub:**
   - Select **BILLY-KIMONO/PrimeAI** repo
   - Click **"Connect"**

---

## 📋 On Render Configuration Page

Fill in these exact values:

```
Name: primeai-backend
Environment: Python 3
Region: Oregon
Branch: main
Build Command: pip install -r backend/requirements.txt
Start Command: cd backend && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
Plan: Free
```

---

## 🔐 Environment Variables (Copy-Paste)

Add these one by one in Render dashboard:

```
DATABASE_URL = postgresql://primeai:password@localhost/primeai
JWT_SECRET_KEY = your-super-secret-key-minimum-32-chars-long
PAYPAL_CLIENT_ID = your-paypal-client-id
PAYPAL_CLIENT_SECRET = your-paypal-client-secret
PAYPAL_MERCHANT_EMAIL = billykimono@gmail.com
MPESA_CONSUMER_KEY = your-mpesa-key
MPESA_CONSUMER_SECRET = your-mpesa-secret
FRONTEND_URL = http://localhost:3000
API_URL = https://primeai-backend.render.com
ENVIRONMENT = production
```

(Render will provide DATABASE_URL automatically after you create the PostgreSQL DB)

---

## 📊 What Happens Next

1. Click **"Create Web Service"** → Build starts (2-3 min)
2. You get a live URL: `https://primeai-backend.render.com`
3. Test: `curl https://primeai-backend.render.com/health`
4. Should return: `{"status":"ok"}`

---

## ✅ Detailed Step-by-Step

Full detailed guide in: **RENDER_DEPLOY_STEPS.md**

---

## 🆘 Issues?

**Build failed?**
- Check Events tab for error
- Verify render.yaml syntax

**Can't connect to database?**
- Create PostgreSQL database first in Render
- Update DATABASE_URL with the connection string

**502 Bad Gateway?**
- Wait 2 minutes for service to fully start
- Check Logs tab for errors

---

## 📝 Commands to Run Now

```bash
cd /home/bill-fardan/PrimeAI

# 1. Prepare files
bash setup-render.sh

# 2. Push to GitHub
git push

# 3. Then go to https://render.com and deploy!
```

---

## 🎉 After Deployment

1. Get backend URL from Render
2. Deploy frontend to Netlify/Vercel
3. Update frontend API_URL to backend URL
4. Test the full app
5. Configure payments
6. You're live! 🚀

