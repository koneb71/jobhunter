from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ApplicationStatus(str, Enum):
    PENDING = "pending"
    REVIEWING = "reviewing"
    SHORTLISTED = "shortlisted"
    INTERVIEWING = "interviewing"
    OFFERED = "offered"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"


class JobApplicationBase(BaseModel):
    cover_letter: Optional[str] = None
    resume_url: Optional[str] = None
    status: ApplicationStatus = ApplicationStatus.PENDING
    expected_salary: Optional[float] = None
    availability_date: Optional[datetime] = None
    additional_info: Optional[dict] = None


class JobApplicationCreate(JobApplicationBase):
    job_id: str


class JobApplicationUpdate(JobApplicationBase):
    pass


class JobApplicationResponse(JobApplicationBase):
    id: str
    job_id: str
    applicant_id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
