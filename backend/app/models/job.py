from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel

class Job(BaseModel):
    id: str
    title: str
    description: str
    location: str
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    job_type: str
    experience_level: Optional[str] = None
    required_skills: List[str] = []
    preferred_skills: List[str] = []
    benefits: List[str] = []
    is_featured: bool = False
    is_active: bool = True
    expires_at: Optional[datetime] = None
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