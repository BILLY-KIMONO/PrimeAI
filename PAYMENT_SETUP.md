# PrimeAI Payment Setup Guide

## Overview
PrimeAI now supports multiple payment methods:
- **PayPal** - For international payments (USD)
- **M-Pesa** - For Kenyan payments (KES)
- **Stripe** - For credit/debit cards (Optional)

## Configuration

### 1. PayPal Setup

#### Get Your Credentials:
1. Go to [PayPal Developer Dashboard](https://www.sandbox.paypal.com)
2. Sign in with your account: **billykimono@gmail.com**
3. Navigate to **Apps & Credentials**
4. Select **Sandbox** environment
5. Under **Rest API signature**, copy:
   - **Client ID**
   - **Secret**

#### Configure in .env:
```bash
PAYPAL_CLIENT_ID=your-client-id-here
PAYPAL_CLIENT_SECRET=your-client-secret-here
PAYPAL_MERCHANT_EMAIL=billykimono@gmail.com
PAYPAL_MODE=sandbox  # Use 'live' for production
```

#### Test PayPal Setup:
```bash
curl -X POST http://localhost:8000/api/payments/paypal/initiate \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "plan_type": "monthly",
    "amount": 8.0,
    "return_url": "http://localhost:3000/success",
    "cancel_url": "http://localhost:3000/cancel"
  }'
```

### 2. M-Pesa Setup (Safaricom Daraja)

#### Get Your Credentials:
1. Go to [Safaricom Daraja Portal](https://developer.safaricom.co.ke)
2. Sign up and create an app
3. In your app settings, you'll find:
   - **Consumer Key**
   - **Consumer Secret**
4. Use the provided test credentials initially:
   - Shortcode: `174379`
   - Passkey: `bfb279f9aa9bdbcf158e97dd1a2c6f95`

#### Test Phone Number:
- Use: **+254758415360** (provided)

#### Configure in .env:
```bash
MPESA_CONSUMER_KEY=your-consumer-key
MPESA_CONSUMER_SECRET=your-consumer-secret
MPESA_SHORTCODE=174379
MPESA_PASSKEY=bfb279f9aa9bdbcf158e97dd1a2c6f95
MPESA_CALLBACK_URL=https://api.primeai.com/api/payments/mpesa/callback
MPESA_PHONE_NUMBER=+254758415360
```

#### Test M-Pesa Setup:
```bash
curl -X POST http://localhost:8000/api/payments/mpesa/initiate \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+254758415360",
    "plan_type": "monthly",
    "amount": 8400
  }'
```

### 3. Database Migration

Add the Payment table to your database:

```bash
# Option 1: Using the Python script
python -c "
from sqlalchemy import create_engine
from app.models.base import Base
from app.models.payment import Payment
from app.config import settings

engine = create_engine(settings.DATABASE_URL)
Base.metadata.create_all(engine)
print('✅ Payment table created successfully')
"

# Option 2: Direct SQL
# Run this in your PostgreSQL database:
psql -U primeai -d primeai << 'EOF'
CREATE TABLE payments (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    amount FLOAT NOT NULL,
    currency VARCHAR(3) NOT NULL DEFAULT 'KES',
    plan_type VARCHAR(20) NOT NULL,
    payment_method VARCHAR(20) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    paypal_transaction_id VARCHAR(255) UNIQUE,
    mpesa_receipt_number VARCHAR(255) UNIQUE,
    stripe_payment_intent_id VARCHAR(255) UNIQUE,
    mpesa_phone_number VARCHAR(20),
    mpesa_checkout_request_id VARCHAR(255),
    paypal_payer_email VARCHAR(255),
    paypal_payer_id VARCHAR(255),
    description TEXT,
    notes TEXT,
    payment_date TIMESTAMP WITH TIME ZONE,
    completion_date TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_payments_user_id ON payments(user_id);
CREATE INDEX idx_payments_status ON payments(status);
CREATE INDEX idx_payments_payment_method ON payments(payment_method);
EOF
```

## API Endpoints

### PayPal Endpoints

#### Initiate Payment
```bash
POST /api/payments/paypal/initiate
Authorization: Bearer {token}

{
  "plan_type": "monthly",  # daily, monthly
  "amount": 8.0,
  "return_url": "https://yourapp.com/success",
  "cancel_url": "https://yourapp.com/cancel"
}
```

Response:
```json
{
  "success": true,
  "payment_id": 1,
  "paypal_payment_id": "PAYID-123456",
  "approval_url": "https://www.sandbox.paypal.com/...",
  "amount": 8.0,
  "currency": "USD"
}
```

#### Execute Payment
```bash
POST /api/payments/paypal/execute
Authorization: Bearer {token}

{
  "payment_id": 1,
  "paypal_payment_id": "PAYID-123456",
  "payer_id": "EBBNJ37SQBSAA"
}
```

### M-Pesa Endpoints

#### Initiate Payment
```bash
POST /api/payments/mpesa/initiate
Authorization: Bearer {token}

{
  "phone_number": "+254758415360",
  "plan_type": "monthly",
  "amount": 8400
}
```

Response:
```json
{
  "success": true,
  "payment_id": 2,
  "checkout_request_id": "ws_CO_DMZ_...",
  "message": "Check your phone for M-Pesa prompt",
  "amount": 8400,
  "currency": "KES"
}
```

#### Check Payment Status
```bash
GET /api/payments/mpesa/status/2
Authorization: Bearer {token}
```

Response:
```json
{
  "payment_id": 2,
  "status": "completed",
  "amount": 8400,
  "currency": "KES",
  "created_at": "2026-03-30T10:30:00"
}
```

### General Endpoints

#### Get Pricing
```bash
GET /api/payments/pricing
```

Response:
```json
{
  "paypal": {
    "daily": {"amount": 5.0, "currency": "USD"},
    "monthly": {"amount": 8.0, "currency": "USD"}
  },
  "mpesa": {
    "daily": {"amount": 600, "currency": "KES"},
    "monthly": {"amount": 8400, "currency": "KES"}
  }
}
```

#### Get Payment History
```bash
GET /api/payments/history
Authorization: Bearer {token}
```

## Pricing Structure

### PayPal (USD)
- **Daily**: $5.00 (1 day access)
- **Monthly**: $8.00 (30 days access, with 100 API calls/month for daily, 1000 for monthly)

### M-Pesa (KES)
- **Daily**: KES 600 (~$5 USD)
- **Monthly**: KES 8,400 (~$70 USD, promotional pricing)

## Testing Payment Methods

### Test PayPal Credentials:
- Email: `sb-xxxxxx@personal.example.com` (from PayPal sandbox)
- Password: `personal_account_password`

### Test M-Pesa:
- Use test phone: **+254758415360** (your number)
- The system will show a prompt on the phone
- Enter the PIN to complete the payment

### Testing Flow:

```bash
# 1. Create test user account (if not exists)
POST /api/auth/register
{
  "email": "test@primeai.com",
  "username": "testuser",
  "password": "Test@123456"
}

# 2. Login to get JWT token
POST /api/auth/login
{
  "username": "testuser",
  "password": "Test@123456"
}

# 3. Initiate M-Pesa payment
POST /api/payments/mpesa/initiate
Authorization: Bearer {token_from_step_2}
{
  "phone_number": "+254758415360",
  "plan_type": "monthly",
  "amount": 8400
}

# 4. Check payment status
GET /api/payments/mpesa/status/1
Authorization: Bearer {token_from_step_2}
```

## Production Deployment

### PayPal Production Setup:
1. Change `PAYPAL_MODE` from `sandbox` to `live`
2. Use production credentials from PayPal
3. Update callback URLs to production domain

### M-Pesa Production Setup:
1. Register for production certificates
2. Update Safaricom Daraja app to production
3. Get production Consumer Key and Secret
4. Update shortcode and passkey
5. Update callback URL to production domain

## Troubleshooting

### M-Pesa Issues:
1. **"Invalid phone number"**: Ensure format is `+254...` or `254...`
2. **"Authentication failed"**: Check Consumer Key and Secret
3. **No callback received**: Verify callback URL is publicly accessible
4. **Transaction pending**: Check M-Pesa account balance and network

### PayPal Issues:
1. **"Payment creation failed"**: Verify Client ID and Secret
2. **"Approval URL not found"**: Check sandbox/live mode setting
3. **"Execution failed"**: Ensure payer_id is correct

## Support

For issues or questions:
- M-Pesa: Check Safaricom Daraja documentation
- PayPal: Visit PayPal Developer docs
- Local issues: Check application logs

## Files Modified

1. `/backend/app/models/payment.py` - Payment database model
2. `/backend/app/services/payment.py` - Payment service implementations
3. `/backend/app/routes/payments.py` - Payment API endpoints
4. `/backend/app/models/user.py` - Added payments relationship
5. `/backend/app/main.py` - Added payment routes
6. `/backend/requirements.txt` - Added payment libraries
7. `/.env` - Payment configuration

