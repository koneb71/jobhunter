from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field

from app.schemas.base import TimestampSchema

class JobBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1)
    location: str = Field(..., min_length=1, max_length=100)
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    job_type: str = Field(..., min_length=1, max_length=50)  # full-time, part-time, contract, etc.
    experience_level: Optional[str] = None
    required_skills: List[str] = Field(default_factory=list)
    preferred_skills: List[str] = Field(default_factory=list)
    benefits: List[str] = Field(default_factory=list)
    is_featured: bool = False
    is_active: bool = True
    expires_at: Optional[datetime] = None

class JobCreate(JobBase):
    company_id: str = Field(..., min_length=1)
    department: Optional[str] = None
    remote_work: bool = False
    visa_sponsorship: bool = False
    relocation_assistance: bool = False

class JobUpdate(JobBase):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, min_length=1)
    location: Optional[str] = Field(None, min_length=1, max_length=100)
    company_id: Optional[str] = Field(None, min_length=1)
    department: Optional[str] = None
    remote_work: Optional[bool] = None
    visa_sponsorship: Optional[bool] = None
    relocation_assistance: Optional[bool] = None

class Job(JobBase):
    id: str
    company_id: str
    department: Optional[str] = None
    remote_work: bool = False
    visa_sponsorship: bool = False
    relocation_assistance: bool = False
    created_at: datetime
    updated_at: Optional[datetime] = None
    created_by: str
    company_name: Optional[str] = None
    application_count: int = 0
    view_count: int = 0

    class Config:
        from_attributes = True

class JobResponse(Job):
    pass

class JobSearchParams(BaseModel):
    query: Optional[str] = None
    location: Optional[str] = None
    job_type: Optional[str] = None
    experience_level: Optional[str] = None
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    remote_work: Optional[bool] = None
    visa_sponsorship: Optional[bool] = None
    company_id: Optional[str] = None
    skip: int = 0
    limit: int = 10 