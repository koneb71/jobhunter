import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import JSON, Column, DateTime
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy import Float, ForeignKey, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class PaymentStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"
    CANCELLED = "cancelled"


class PaymentType(str, Enum):
    JOB_POSTING = "job_posting"
    FEATURED_JOB = "featured_job"
    SUBSCRIPTION = "subscription"
    OTHER = "other"


class PaymentMethod(str, Enum):
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    BANK_TRANSFER = "bank_transfer"
    PAYPAL = "paypal"
    OTHER = "other"


class Payment(Base):
    __tablename__ = "payments"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    amount = Column(Float, nullable=False)
    payment_type = Column(
        SQLAlchemyEnum(PaymentType, name="payment_type_enum"), nullable=False
    )
    payment_method = Column(
        SQLAlchemyEnum(PaymentMethod, name="payment_method_enum"), nullable=False
    )
    status = Column(
        SQLAlchemyEnum(PaymentStatus, name="payment_status_enum"),
        default=PaymentStatus.PENDING,
    )
    description = Column(String, nullable=True)
    payment_metadata = Column(JSON, default=dict)
    job_id = Column(String, ForeignKey("jobs.id"), nullable=True)
    subscription_id = Column(String, nullable=True)
    transaction_id = Column(String, nullable=True)
    payment_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="payments")
    job = relationship("Job", back_populates="payments")

    def __repr__(self):
        return f"<Payment {self.id} - {self.status}>"
