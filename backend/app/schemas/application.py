from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime

from app.schemas.base import TimestampSchema

class ApplicationBase(BaseModel):
    job_id: str
    cover_letter: Optional[str] = None
    resume_url: Optional[str] = None
    status: str = Field(
        default="pending",
        description="Application status: pending, reviewed, shortlisted, rejected, accepted"
    )
    notes: Optional[str] = None

class ApplicationCreate(ApplicationBase):
    pass

class ApplicationUpdate(ApplicationBase):
    job_id: Optional[str] = None
    status: Optional[str] = None

class ApplicationResponse(TimestampSchema, ApplicationBase):
    id: str
    user_id: str
    user_name: str
    job_title: str
    company_name: str
    applied_at: datetime 