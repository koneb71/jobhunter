from datetime import datetime

from sqlalchemy import JSON, Column, DateTime, Float, ForeignKey, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.schemas.job_application import ApplicationStatus


class JobApplication(Base):
    __tablename__ = "job_applications"

    id = Column(String, primary_key=True, index=True)
    job_id = Column(String, ForeignKey("jobs.id"), nullable=False)
    applicant_id = Column(String, ForeignKey("users.id"), nullable=False)
    cover_letter = Column(String, nullable=True)
    resume_url = Column(String, nullable=True)
    status = Column(String, nullable=False, default=ApplicationStatus.PENDING)
    expected_salary = Column(Float, nullable=True)
    availability_date = Column(DateTime, nullable=True)
    additional_info = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relationships
    job = relationship("Job", back_populates="applications")
    applicant = relationship("User", back_populates="applications")
    interviews = relationship("Interview", back_populates="application")

    def __repr__(self):
        return f"<JobApplication {self.id} - {self.status}>"
