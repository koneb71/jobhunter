from sqlalchemy import Column, String, DateTime, JSON, ForeignKey, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base
import uuid
from enum import Enum

class VerificationRequestStatus(str, Enum):
    PENDING = "pending"
    IN_REVIEW = "in_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    CANCELLED = "cancelled"

class VerificationType(str, Enum):
    IDENTITY = "identity"
    EDUCATION = "education"
    EMPLOYMENT = "employment"
    SKILLS = "skills"
    CERTIFICATIONS = "certifications"
    PORTFOLIO = "portfolio"

class VerificationRequest(Base):
    __tablename__ = "verification_requests"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    verification_type = Column(SQLAlchemyEnum(VerificationType, name="verification_type_enum"), nullable=False)
    status = Column(SQLAlchemyEnum(VerificationRequestStatus, name="verification_status_enum"), default=VerificationRequestStatus.PENDING)
    submitted_at = Column(DateTime, default=datetime.utcnow)
    reviewed_at = Column(DateTime, nullable=True)
    reviewed_by = Column(String, ForeignKey("users.id"), nullable=True)
    notes = Column(String, nullable=True)
    evidence = Column(JSON, default=dict)
    rejection_reason = Column(String, nullable=True)

    # Relationships
    user = relationship("User", foreign_keys=[user_id], back_populates="verification_requests")
    reviewer = relationship("User", foreign_keys=[reviewed_by], back_populates="reviewed_verifications") 