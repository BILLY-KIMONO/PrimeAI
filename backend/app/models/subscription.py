from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.models.base import Base, TimestampMixin
from datetime import datetime, timedelta

class Subscription(Base, TimestampMixin):
    __tablename__ = "subscriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # Subscription details
    plan_type = Column(String(20), nullable=False)  # "trial", "daily", "monthly"
    stripe_subscription_id = Column(String(255), unique=True, nullable=True)
    stripe_customer_id = Column(String(255), unique=True, nullable=True)
    
    # Dates
    start_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    end_date = Column(DateTime, nullable=False)
    trial_end_date = Column(DateTime, nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True, nullable=False)
    is_cancelled = Column(Boolean, default=False, nullable=False)
    
    # Usage tracking
    api_calls_used = Column(Integer, default=0, nullable=False)
    api_calls_limit = Column(Integer, default=1000, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="subscriptions")
    
    class Config:
        from_attributes = True
