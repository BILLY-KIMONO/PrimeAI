from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime, timedelta
from app.models.subscription import Subscription
from app.config import settings

def create_trial_subscription(db: Session, user_id: int):
    """Create a 1-day free trial subscription"""
    end_date = datetime.utcnow() + timedelta(days=settings.TRIAL_DAYS)
    trial_end = datetime.utcnow() + timedelta(days=settings.TRIAL_DAYS)
    
    subscription = Subscription(
        user_id=user_id,
        plan_type="trial",
        start_date=datetime.utcnow(),
        end_date=end_date,
        trial_end_date=trial_end,
        is_active=True,
        api_calls_limit=1000
    )
    db.add(subscription)
    db.commit()
    db.refresh(subscription)
    return subscription

def is_subscription_active(db: Session, user_id: int) -> bool:
    """Check if user has active subscription"""
    subscription = db.query(Subscription).filter(
        and_(
            Subscription.user_id == user_id,
            Subscription.is_active == True,
            Subscription.is_cancelled == False,
            Subscription.end_date > datetime.utcnow()
        )
    ).first()
    return subscription is not None

def has_api_calls_remaining(db: Session, user_id: int) -> bool:
    """Check if user has API calls remaining"""
    subscription = db.query(Subscription).filter(
        Subscription.user_id == user_id,
        Subscription.is_active == True
    ).first()
    
    if not subscription:
        return False
    
    return subscription.api_calls_used < subscription.api_calls_limit

def increment_api_calls(db: Session, user_id: int):
    """Increment API call count"""
    subscription = db.query(Subscription).filter(
        Subscription.user_id == user_id,
        Subscription.is_active == True
    ).first()
    
    if subscription:
        subscription.api_calls_used += 1
        db.commit()
