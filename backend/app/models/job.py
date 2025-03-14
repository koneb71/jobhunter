import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import JSON, Boolean, Column, DateTime
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy import Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class JobType(str, Enum):
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"
    INTERNSHIP = "internship"
    FREELANCE = "freelance"


class ExperienceLevel(str, Enum):
    ENTRY = "entry"
    JUNIOR = "junior"
    MID = "mid"
    SENIOR = "senior"
    LEAD = "lead"
    EXECUTIVE = "executive"


class Job(Base):
    __tablename__ = "jobs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    location = Column(String, nullable=False)
    salary_min = Column(Float)
    salary_max = Column(Float)
    job_type = Column(SQLAlchemyEnum(JobType), nullable=False)
    experience_level = Column(SQLAlchemyEnum(ExperienceLevel))
    required_skills = Column(JSON, default=list)
    preferred_skills = Column(JSON, default=list)
    benefits = Column(JSON, default=list)
    is_featured = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    expires_at = Column(DateTime)
    employer_id = Column(String, ForeignKey("users.id"), nullable=False)
    department = Column(String)
    remote_work = Column(Boolean, default=False)
    visa_sponsorship = Column(Boolean, default=False)
    relocation_assistance = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    view_count = Column(Integer, default=0)

    # Relationships
    employer = relationship("User", back_populates="jobs")
    applications = relationship("JobApplication", back_populates="job")
    payments = relationship("Payment", back_populates="job")

    def __repr__(self):
        return f"<Job {self.title}>"
