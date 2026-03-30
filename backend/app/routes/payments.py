from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime, timedelta
from app.database import get_db
from app.models.user import User
from app.models.payment import Payment
from app.models.subscription import Subscription
from app.services import verify_token
from app.services.payment import PaymentService
from app.config import settings
import logging

logger = logging.getLogger(__name__)
router = APIRouter()
payment_service = PaymentService()

# ============= Pydantic Models =============

class PayPalPaymentRequest(BaseModel):
    """Request to initiate PayPal payment"""
    plan_type: str  # "daily", "monthly"
    amount: float
    return_url: str
    cancel_url: str

class MPesaPaymentRequest(BaseModel):
    """Request to initiate M-Pesa payment"""
    phone_number: str
    plan_type: str  # "daily", "monthly"
    amount: float

class PaymentResponse(BaseModel):
    id: int
    user_id: int
    amount: float
    currency: str
    plan_type: str
    payment_method: str
    status: str
    paypal_transaction_id: str = None
    mpesa_receipt_number: str = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class PaymentStatusResponse(BaseModel):
    status: str
    success: bool
    message: str
    data: dict = {}

# ============= Helper Functions =============

def get_current_user(authorization: str = Header(None), db: Session = Depends(get_db)):
    """Extract and validate user from token"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    token = authorization.split(" ")[1]
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user_id = int(payload.get("sub"))
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

def get_plan_pricing(plan_type: str, currency: str = "USD") -> dict:
    """Get pricing for plan type"""
    if currency == "KES":
        pricing = {
            "daily": {"amount": 600, "currency": "KES", "duration_days": 1},  # ~$5
            "monthly": {"amount": 8400, "currency": "KES", "duration_days": 30}  # ~$70, promo
        }
    else:  # USD
        pricing = {
            "daily": {"amount": 5.0, "currency": "USD", "duration_days": 1},
            "monthly": {"amount": 8.0, "currency": "USD", "duration_days": 30}
        }
    
    return pricing.get(plan_type, {})

# ============= PayPal Routes =============

@router.post("/paypal/initiate")
def initiate_paypal_payment(
    request: PayPalPaymentRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Initiate PayPal payment"""
    try:
        # Get pricing
        pricing = get_plan_pricing(request.plan_type, "USD")
        if not pricing:
            raise HTTPException(status_code=400, detail="Invalid plan type")
        
        # Create payment in database
        payment = Payment(
            user_id=current_user.id,
            amount=pricing["amount"],
            currency="USD",
            plan_type=request.plan_type,
            payment_method="paypal",
            status="pending",
            paypal_payer_email=current_user.email,
            description=f"PrimeAI {request.plan_type.title()} Subscription"
        )
        db.add(payment)
        db.commit()
        db.refresh(payment)
        
        # Create PayPal payment
        paypal_result = payment_service.paypal.create_payment(
            amount=pricing["amount"],
            description=f"PrimeAI {request.plan_type.title()} Subscription",
            return_url=request.return_url,
            cancel_url=request.cancel_url
        )
        
        if not paypal_result.get("success"):
            raise HTTPException(status_code=400, detail=paypal_result.get("error"))
        
        # Update payment with PayPal transaction ID
        payment.paypal_transaction_id = paypal_result.get("payment_id")
        db.commit()
        
        return {
            "success": True,
            "payment_id": payment.id,
            "paypal_payment_id": paypal_result.get("payment_id"),
            "approval_url": paypal_result.get("approval_url"),
            "amount": pricing["amount"],
            "currency": "USD"
        }
    except Exception as e:
        logger.error(f"PayPal initiation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/paypal/execute")
def execute_paypal_payment(
    payment_id: int,
    paypal_payment_id: str,
    payer_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Execute PayPal payment"""
    try:
        # Get payment
        payment = db.query(Payment).filter(
            Payment.id == payment_id,
            Payment.user_id == current_user.id
        ).first()
        
        if not payment:
            raise HTTPException(status_code=404, detail="Payment not found")
        
        # Execute PayPal payment
        paypal_result = payment_service.paypal.execute_payment(paypal_payment_id, payer_id)
        
        if not paypal_result.get("success"):
            payment.status = "failed"
            db.commit()
            raise HTTPException(status_code=400, detail="PayPal execution failed")
        
        # Update payment status
        payment.status = "completed"
        payment.payment_date = datetime.utcnow()
        payment.completion_date = datetime.utcnow()
        db.commit()
        
        # Create/Update subscription
        pricing = get_plan_pricing(payment.plan_type, "USD")
        end_date = datetime.utcnow() + timedelta(days=pricing["duration_days"])
        
        # Check if user has active subscription
        active_sub = db.query(Subscription).filter(
            Subscription.user_id == current_user.id,
            Subscription.is_active == True
        ).first()
        
        if active_sub:
            active_sub.end_date = end_date
            active_sub.is_cancelled = False
        else:
            subscription = Subscription(
                user_id=current_user.id,
                plan_type=payment.plan_type,
                start_date=datetime.utcnow(),
                end_date=end_date,
                is_active=True,
                api_calls_limit=1000 if payment.plan_type == "monthly" else 100
            )
            db.add(subscription)
        
        db.commit()
        
        return {
            "success": True,
            "message": "Payment completed successfully",
            "payment_id": payment.id,
            "subscription_end_date": end_date.isoformat()
        }
    except Exception as e:
        logger.error(f"PayPal execution failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# ============= M-Pesa Routes =============

@router.post("/mpesa/initiate")
def initiate_mpesa_payment(
    request: MPesaPaymentRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Initiate M-Pesa payment"""
    try:
        # Get pricing
        pricing = get_plan_pricing(request.plan_type, "KES")
        if not pricing:
            raise HTTPException(status_code=400, detail="Invalid plan type")
        
        # Create payment in database
        payment = Payment(
            user_id=current_user.id,
            amount=pricing["amount"],
            currency="KES",
            plan_type=request.plan_type,
            payment_method="mpesa",
            status="pending",
            mpesa_phone_number=request.phone_number,
            description=f"PrimeAI {request.plan_type.title()} Subscription"
        )
        db.add(payment)
        db.commit()
        db.refresh(payment)
        
        # Initiate M-Pesa STK push
        mpesa_result = payment_service.mpesa.stk_push(
            phone_number=request.phone_number,
            amount=pricing["amount"],
            account_ref=f"USER{current_user.id}",
            description=f"PrimeAI {request.plan_type.title()}"
        )
        
        if not mpesa_result.get("success"):
            payment.status = "failed"
            db.commit()
            raise HTTPException(status_code=400, detail=mpesa_result.get("error"))
        
        # Update payment with checkout request ID
        payment.mpesa_checkout_request_id = mpesa_result.get("checkout_request_id")
        db.commit()
        
        return {
            "success": True,
            "payment_id": payment.id,
            "checkout_request_id": mpesa_result.get("checkout_request_id"),
            "message": "Check your phone for M-Pesa prompt",
            "amount": pricing["amount"],
            "currency": "KES"
        }
    except Exception as e:
        logger.error(f"M-Pesa initiation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/mpesa/status/{payment_id}")
def check_mpesa_payment_status(
    payment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Check M-Pesa payment status"""
    try:
        # Get payment
        payment = db.query(Payment).filter(
            Payment.id == payment_id,
            Payment.user_id == current_user.id,
            Payment.payment_method == "mpesa"
        ).first()
        
        if not payment:
            raise HTTPException(status_code=404, detail="Payment not found")
        
        # Query M-Pesa transaction
        if payment.mpesa_checkout_request_id:
            mpesa_result = payment_service.mpesa.query_transaction(
                payment.mpesa_checkout_request_id
            )
            
            # Update payment status if completed
            if mpesa_result.get("result_code") == "0":
                payment.status = "completed"
                payment.payment_date = datetime.utcnow()
                payment.completion_date = datetime.utcnow()
                db.commit()
                
                # Create subscription
                pricing = get_plan_pricing(payment.plan_type, "KES")
                end_date = datetime.utcnow() + timedelta(days=pricing["duration_days"])
                
                subscription = Subscription(
                    user_id=current_user.id,
                    plan_type=payment.plan_type,
                    start_date=datetime.utcnow(),
                    end_date=end_date,
                    is_active=True,
                    api_calls_limit=1000 if payment.plan_type == "monthly" else 100
                )
                db.add(subscription)
                db.commit()
        
        return {
            "payment_id": payment.id,
            "status": payment.status,
            "amount": payment.amount,
            "currency": payment.currency,
            "created_at": payment.created_at.isoformat()
        }
    except Exception as e:
        logger.error(f"M-Pesa status check failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/mpesa/callback")
def mpesa_callback(request: dict, db: Session = Depends(get_db)):
    """M-Pesa callback endpoint"""
    try:
        logger.info(f"M-Pesa callback received: {request}")
        
        # Extract callback data
        result = request.get("Result", {})
        result_code = result.get("ResultCode")
        checkout_id = result.get("CheckoutRequestID")
        receipt = result.get("Items", [{}])[0].get("Value") if result.get("Items") else None
        
        # Find payment by checkout request ID
        payment = db.query(Payment).filter(
            Payment.mpesa_checkout_request_id == checkout_id
        ).first()
        
        if payment:
            if result_code == 0:  # Success
                payment.status = "completed"
                payment.mpesa_receipt_number = receipt
                payment.completion_date = datetime.utcnow()
                
                # Create subscription
                pricing = get_plan_pricing(payment.plan_type, "KES")
                end_date = datetime.utcnow() + timedelta(days=pricing["duration_days"])
                
                subscription = Subscription(
                    user_id=payment.user_id,
                    plan_type=payment.plan_type,
                    start_date=datetime.utcnow(),
                    end_date=end_date,
                    is_active=True,
                    api_calls_limit=1000 if payment.plan_type == "monthly" else 100
                )
                db.add(subscription)
                logger.info(f"Payment {payment.id} marked as completed")
            else:
                payment.status = "failed"
                logger.warning(f"Payment {payment.id} failed with code {result_code}")
            
            db.commit()
        
        return {"ResultCode": 0, "ResultDesc": "Callback processed"}
    except Exception as e:
        logger.error(f"M-Pesa callback processing failed: {str(e)}")
        return {"ResultCode": 1, "ResultDesc": "Callback processing failed"}

# ============= Payment History Routes =============

@router.get("/history")
def get_payment_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user payment history"""
    payments = db.query(Payment).filter(
        Payment.user_id == current_user.id
    ).order_by(Payment.created_at.desc()).all()
    
    return [PaymentResponse.from_orm(p) for p in payments]

@router.get("/pricing")
def get_pricing():
    """Get pricing for all plans"""
    return {
        "paypal": {
            "daily": {"amount": 5.0, "currency": "USD"},
            "monthly": {"amount": 8.0, "currency": "USD"}
        },
        "mpesa": {
            "daily": {"amount": 600, "currency": "KES"},
            "monthly": {"amount": 8400, "currency": "KES"}
        }
    }
