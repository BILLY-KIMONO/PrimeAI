from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.models.subscription import Subscription
from app.models.user import User
from app.services import verify_token
from datetime import datetime

router = APIRouter()

class SubscriptionResponse(BaseModel):
    id: int
    plan_type: str
    start_date: datetime
    end_date: datetime
    is_active: bool
    api_calls_used: int
    api_calls_limit: int
    
    class Config:
        from_attributes = True

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

@router.get("/active")
def get_active_subscription(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get active subscription"""
    subscription = db.query(Subscription).filter(
        Subscription.user_id == current_user.id,
        Subscription.is_active == True
    ).first()
    
    if not subscription:
        raise HTTPException(status_code=404, detail="No active subscription")
    
    return SubscriptionResponse.from_orm(subscription)

@router.get("/list")
def list_subscriptions(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """List all subscriptions for user"""
    subscriptions = db.query(Subscription).filter(
        Subscription.user_id == current_user.id
    ).all()
    
    return [SubscriptionResponse.from_orm(s) for s in subscriptions]

@router.post("/cancel")
def cancel_subscription(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Cancel active subscription"""
    subscription = db.query(Subscription).filter(
        Subscription.user_id == current_user.id,
        Subscription.is_active == True
    ).first()
    
    if not subscription:
        raise HTTPException(status_code=404, detail="No active subscription")
    
    subscription.is_cancelled = True
    subscription.is_active = False
    db.commit()
    
    return {"message": "Subscription cancelled"}
