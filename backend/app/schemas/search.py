from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

from app.schemas.job import JobResponse
from app.schemas.company import CompanyResponse

class JobType(str, Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"
    CONTRACT = "contract"
    INTERNSHIP = "internship"
    TEMPORARY = "temporary"

class ExperienceLevel(str, Enum):
    ENTRY = "entry"
    MID_LEVEL = "mid-level"
    SENIOR = "senior"
    LEAD = "lead"
    MANAGER = "manager"
    DIRECTOR = "director"
    EXECUTIVE = "executive"

class SortBy(str, Enum):
    RELEVANCE = "relevance"
    DATE = "date"
    SALARY = "salary"
    TITLE = "title"
    COMPANY = "company"

class SortOrder(str, Enum):
    ASC = "asc"
    DESC = "desc"

class SearchParams(BaseModel):
    query: Optional[str] = Field(None, description="Search query for jobs and companies")
    job_type: Optional[JobType] = Field(None, description="Filter by job type")
    experience_level: Optional[ExperienceLevel] = Field(None, description="Filter by experience level")
    location: Optional[str] = Field(None, description="Filter by location")
    industry: Optional[str] = Field(None, description="Filter by industry")
    salary_min: Optional[float] = Field(None, description="Minimum salary")
    salary_max: Optional[float] = Field(None, description="Maximum salary")
    remote_only: Optional[bool] = Field(False, description="Show only remote jobs")
    posted_within_days: Optional[int] = Field(None, description="Jobs posted within X days")
    company_size: Optional[str] = Field(None, description="Filter by company size")
    sort_by: Optional[SortBy] = Field(SortBy.RELEVANCE, description="Sort by field")
    sort_order: Optional[SortOrder] = Field(SortOrder.DESC, description="Sort order")
    page: Optional[int] = Field(1, description="Page number")
    page_size: Optional[int] = Field(20, description="Items per page")

class PaginationInfo(BaseModel):
    current_page: int
    total_pages: int
    total_items: int
    has_next: bool
    has_previous: bool
    page_size: int

class SearchResponse(BaseModel):
    jobs: List[JobResponse] = []
    companies: List[CompanyResponse] = []
    pagination: PaginationInfo
    took_ms: float = 0.0
    filters: dict = Field(default_factory=dict) 