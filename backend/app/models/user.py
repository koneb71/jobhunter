from typing import Optional, List, Dict, Any
from datetime import datetime
from sqlalchemy import Boolean, Column, Integer, String, DateTime, Enum as SQLAlchemyEnum, ForeignKey, Text, JSON, Float, Date, ARRAY
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum

from app.db.base_class import Base
from app.schemas.user import UserType, AvailabilityStatus, EmploymentType, WorkSchedule, CompanySize, BenefitType
from app.models.verification_request import VerificationRequest

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    display_name = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    user_type = Column(SQLAlchemyEnum(UserType), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    profile = relationship("Profile", back_populates="user", uselist=False)
    jobs = relationship("Job", back_populates="employer")
    applications = relationship("JobApplication", back_populates="applicant")
    notifications = relationship("Notification", back_populates="user")
    payments = relationship("Payment", back_populates="user")
    verification_requests = relationship("VerificationRequest", foreign_keys="VerificationRequest.user_id", back_populates="user")
    reviewed_verifications = relationship("VerificationRequest", foreign_keys="VerificationRequest.reviewed_by", back_populates="reviewer")

    def __repr__(self):
        return f"<User {self.display_name or f'{self.first_name} {self.last_name}'}>"

    def __str__(self):
        return self.display_name or f"{self.first_name} {self.last_name}" 