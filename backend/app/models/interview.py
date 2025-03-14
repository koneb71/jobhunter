from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Enum as SQLAlchemyEnum, Integer
from sqlalchemy.orm import relationship
from app.db.base_class import Base
import uuid
from enum import Enum

class InterviewStatus(str, Enum):
    SCHEDULED = "scheduled"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    NO_SHOW = "no_show"

class InterviewType(str, Enum):
    PHONE = "phone"
    VIDEO = "video"
    IN_PERSON = "in_person"
    TECHNICAL = "technical"
    BEHAVIORAL = "behavioral"
    FINAL = "final"

class Interview(Base):
    __tablename__ = "interviews"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    application_id = Column(String, ForeignKey("job_applications.id"), nullable=False)
    scheduled_at = Column(DateTime, nullable=False)
    duration_minutes = Column(Integer, nullable=False, default=60)
    interview_type = Column(SQLAlchemyEnum(InterviewType), nullable=False)
    status = Column(SQLAlchemyEnum(InterviewStatus), nullable=False, default=InterviewStatus.SCHEDULED)
    meeting_link = Column(String, nullable=True)
    location = Column(String, nullable=True)
    notes = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    application = relationship("JobApplication", back_populates="interviews")

    def __repr__(self):
        return f"<Interview {self.id} - {self.status}>" 