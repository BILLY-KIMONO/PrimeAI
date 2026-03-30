from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from app.models.base import Base, TimestampMixin
from datetime import datetime
import enum

class PaymentStatus(str, enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class PaymentMethod(str, enum.Enum):
    PAYPAL = "paypal"
    MPESA = "mpesa"
    STRIPE = "stripe"

class Payment(Base, TimestampMixin):
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # Payment details
    amount = Column(Float, nullable=False)
    currency = Column(String(3), default="KES", nullable=False)  # KES for M-Pesa, USD for PayPal
    plan_type = Column(String(20), nullable=False)  # "daily", "monthly"
    payment_method = Column(String(20), nullable=False)  # "paypal", "mpesa", "stripe"
    status = Column(String(20), default="pending", nullable=False)
    
    # External payment processor IDs
    paypal_transaction_id = Column(String(255), unique=True, nullable=True)
    mpesa_receipt_number = Column(String(255), unique=True, nullable=True)
    stripe_payment_intent_id = Column(String(255), unique=True, nullable=True)
    
    # M-Pesa specific
    mpesa_phone_number = Column(String(20), nullable=True)
    mpesa_checkout_request_id = Column(String(255), nullable=True)
    
    # PayPal specific
    paypal_payer_email = Column(String(255), nullable=True)
    paypal_payer_id = Column(String(255), nullable=True)
    
    # Metadata
    description = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    
    # Dates
    payment_date = Column(DateTime, nullable=True)
    completion_date = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="payments")
    
    class Config:
        from_attributes = True
