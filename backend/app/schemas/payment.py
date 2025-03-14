from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

from app.schemas.base import TimestampSchema

class PaymentStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"

class PaymentType(str, Enum):
    JOB_POSTING = "job_posting"
    SUBSCRIPTION = "subscription"
    REFUND = "refund"

class PaymentMethod(str, Enum):
    INTERNAL = "internal"
    CREDIT_CARD = "credit_card"
    BANK_TRANSFER = "bank_transfer"

class PaymentBase(BaseModel):
    amount: float = Field(..., description="Payment amount in USD")
    payment_type: PaymentType
    payment_method: PaymentMethod = PaymentMethod.INTERNAL
    status: PaymentStatus = PaymentStatus.PENDING
    description: Optional[str] = None
    metadata: dict = Field(default_factory=dict)

class PaymentCreate(PaymentBase):
    user_id: str
    job_id: Optional[str] = None
    subscription_id: Optional[str] = None

class PaymentUpdate(BaseModel):
    status: Optional[PaymentStatus] = None
    description: Optional[str] = None
    metadata: Optional[dict] = None

class PaymentResponse(TimestampSchema, PaymentBase):
    id: str
    user_id: str
    job_id: Optional[str] = None
    subscription_id: Optional[str] = None
    transaction_id: Optional[str] = None
    payment_date: Optional[datetime] = None 