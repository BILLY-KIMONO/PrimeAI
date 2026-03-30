# Quick Start: Payment Integration

## 🚀 Setup Steps (5 minutes)

### Step 1: Update Environment Variables
```bash
cd /home/bill-fardan/PrimeAI
nano .env
```

Update the following fields:

**PayPal:**
```
PAYPAL_CLIENT_ID=your-paypal-client-id
PAYPAL_CLIENT_SECRET=your-paypal-client-secret
```

**M-Pesa:**
```
MPESA_CONSUMER_KEY=your-mpesa-consumer-key
MPESA_CONSUMER_SECRET=your-mpesa-consumer-secret
```

Or for testing, leave the M-Pesa sandbox credentials as-is (they work for testing).

### Step 2: Install Python Dependencies
```bash
cd /home/bill-fardan/PrimeAI/backend
pip install -r requirements.txt
```

### Step 3: Initialize Database with Payment Table
```bash
cd /home/bill-fardan/PrimeAI/backend
python init_db.py
```

### Step 4: Start Backend Server
```bash
cd /home/bill-fardan/PrimeAI/backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Step 5: Test Payment Setup

#### Get your JWT token first:
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@primeai.com",
    "username": "testuser",
    "password": "Test@123456"
  }'

curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "Test@123456"
  }'
```

Save the token from the response as `TOKEN`

#### Test M-Pesa Payment (Kenyan):
```bash
curl -X POST http://localhost:8000/api/payments/mpesa/initiate \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+254758415360",
    "plan_type": "monthly",
    "amount": 1000
  }'
```

#### Test PayPal Payment (International):
```bash
curl -X POST http://localhost:8000/api/payments/paypal/initiate \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "plan_type": "monthly",
    "amount": 8.0,
    "return_url": "http://localhost:3000/success",
    "cancel_url": "http://localhost:3000/cancel"
  }'
```

#### Get Pricing:
```bash
curl http://localhost:8000/api/payments/pricing
```

## 📋 Configuration Summary

Your payment system is now configured with:

**PayPal (USD):**
- Email: billykimono@gmail.com
- Monthly: $8.00

**M-Pesa (KES):**
- Phone: +254758415360
- Monthly: KES 1,000

## 📕 Complete Documentation

See [PAYMENT_SETUP.md](./PAYMENT_SETUP.md) for detailed documentation including:
- Getting PayPal/M-Pesa credentials
- Production deployment
- All API endpoints
- Testing procedures
- Troubleshooting

## 🔗 API Base URL

Development: `http://localhost:8000/api`
Production: `https://api.primeai.com/api`

## 💳 Payment Endpoints

```
POST   /api/payments/paypal/initiate      - Start PayPal payment
POST   /api/payments/paypal/execute      - Complete PayPal payment
POST   /api/payments/mpesa/initiate      - Start M-Pesa payment
GET    /api/payments/mpesa/status/{id}   - Check M-Pesa status
GET    /api/payments/pricing             - Get current pricing
GET    /api/payments/history             - Get user payment history
POST   /api/payments/mpesa/callback      - M-Pesa webhook callback
```

## 💡 Pro Tips

1. **Test M-Pesa**: Use phone +254758415360 with test credentials
2. **Test PayPal**: Use the approval_url from the response
3. **Check Logs**: Watch server logs for payment errors
4. **Database**: Payment data is persisted in PostgreSQL

## ✅ Verification Checklist

- [ ] .env file updated with credentials
- [ ] Python dependencies installed
- [ ] Database tables created (init_db.py ran)
- [ ] Backend server started successfully
- [ ] User registration works
- [ ] Login returns JWT token
- [ ] Payment endpoints respond with 200 status
- [ ] Payment records appear in database

## 🆘 Common Issues

**"Not authenticated"** → Check that Authorization header is present and token is valid
**"Payment table not found"** → Run `python init_db.py`
**"Module not found"** → Run `pip install -r requirements.txt`
**M-Pesa fails** → Check phone number format (+254...)
**PayPal fails** → Verify CLIENT_ID and CLIENT_SECRET in .env

## 📞 Support Resources

- PayPal Developers: https://developer.paypal.com
- Safaricom Daraja: https://developer.safaricom.co.ke
- FastAPI Docs: http://localhost:8000/docs
- OpenAPI Schema: http://localhost:8000/openapi.json

---

**Next Steps:**
1. Deploy frontend dashboard
2. Add payment buttons to subscription page
3. Set up payment success/failure pages
4. Configure production credentials
5. Deploy to production server

