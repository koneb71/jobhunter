from typing import Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime

from app.schemas.payment import PaymentStatus, PaymentType, PaymentMethod

class Payment(BaseModel):
    id: str
    user_id: str
    amount: float
    payment_type: PaymentType
    payment_method: PaymentMethod
    status: PaymentStatus
    description: Optional[str] = None
    metadata: Dict[str, Any]
    job_id: Optional[str] = None
    subscription_id: Optional[str] = None
    transaction_id: Optional[str] = None
    payment_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime 