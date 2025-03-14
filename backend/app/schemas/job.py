from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.base import TimestampSchema


class JobBase(BaseModel):
    title: str
    description: str
    company_id: str
    location: str
    salary_range: str | None = None
    employment_type: str | None = None
    experience_level: str | None = None
    skills_required: list[str] | None = None
    benefits: list[str] | None = None
    is_remote: bool | None = None
    is_featured: bool | None = None
    status: str | None = None

    model_config = ConfigDict(from_attributes=True)


class JobCreate(JobBase):
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
    updated_at: datetime
    created_by: str
    company_name: Optional[str] = None
    application_count: int = 0
    view_count: int = 0

    model_config = ConfigDict(from_attributes=True)


class JobResponse(Job):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


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


class PaginatedJobResponse(BaseModel):
    items: List[JobResponse]
    total: int
    page: int
    size: int
    pages: int

    class Config:
        from_attributes = True
