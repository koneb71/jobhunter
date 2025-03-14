from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, validator

from app.schemas.base import TimestampSchema


class UserRole(str, Enum):
    ADMIN = "admin"
    EMPLOYER = "employer"
    JOBSEEKER = "jobseeker"


class AvailabilityStatus(str, Enum):
    AVAILABLE = "available"
    BUSY = "busy"
    NOT_AVAILABLE = "not_available"


class EmploymentType(str, Enum):
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    FREELANCE = "freelance"
    CONTRACT = "contract"
    INTERNSHIP = "internship"


class WorkSchedule(str, Enum):
    REMOTE = "remote"
    HYBRID = "hybrid"
    ON_SITE = "on_site"
    FLEXIBLE = "flexible"


class CompanySize(str, Enum):
    STARTUP = "startup"
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"
    ENTERPRISE = "enterprise"


class BenefitType(str, Enum):
    HEALTH_INSURANCE = "health_insurance"
    DENTAL_INSURANCE = "dental_insurance"
    VISION_INSURANCE = "vision_insurance"
    LIFE_INSURANCE = "life_insurance"
    RETIREMENT_401K = "401k"
    RETIREMENT_IRA = "ira"
    PAID_TIME_OFF = "paid_time_off"
    SICK_LEAVE = "sick_leave"
    MATERNITY_LEAVE = "maternity_leave"
    PATERNITY_LEAVE = "paternity_leave"
    FLEXIBLE_HOURS = "flexible_hours"
    REMOTE_WORK = "remote_work"
    PROFESSIONAL_DEVELOPMENT = "professional_development"
    GYM_MEMBERSHIP = "gym_membership"
    STOCK_OPTIONS = "stock_options"
    BONUS = "bonus"
    COMMISSION = "commission"
    OTHER = "other"


class EmploymentPreferences(BaseModel):
    preferred_employment_types: List[EmploymentType] = Field(default_factory=list)
    preferred_work_schedule: List[WorkSchedule] = Field(default_factory=list)
    preferred_work_hours: Optional[str] = None
    preferred_work_days: Optional[List[str]] = None
    preferred_contract_duration: Optional[str] = None
    preferred_remote_percentage: Optional[int] = Field(None, ge=0, le=100)
    preferred_commute_distance: Optional[int] = Field(
        None, ge=0, le=500
    )  # Max 500 km/miles
    preferred_industry: Optional[List[str]] = None
    preferred_company_size: Optional[List[CompanySize]] = None
    preferred_benefits: Optional[List[BenefitType]] = None
    preferred_salary_range: Optional[Dict[str, float]] = Field(
        None, description="{'min': 0, 'max': 1000000}"
    )
    preferred_currency: Optional[str] = Field(
        None, pattern="^[A-Z]{3}$"
    )  # ISO 4217 currency code
    preferred_work_permit: Optional[List[str]] = None
    preferred_work_location: Optional[List[str]] = None
    preferred_work_environment: Optional[List[str]] = (
        None  # e.g., ["fast-paced", "collaborative", "innovative"]
    )

    @validator("preferred_work_days")
    def validate_work_days(cls, v):
        if v:
            valid_days = [
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday",
                "Sunday",
            ]
            for day in v:
                if day not in valid_days:
                    raise ValueError(
                        f"Invalid work day: {day}. Must be one of {valid_days}"
                    )
        return v

    @validator("preferred_salary_range")
    def validate_salary_range(cls, v):
        if v:
            if "min" not in v or "max" not in v:
                raise ValueError("Salary range must include 'min' and 'max'")
            if v["min"] < 0:
                raise ValueError("Minimum salary cannot be negative")
            if v["max"] < v["min"]:
                raise ValueError("Maximum salary must be greater than minimum salary")
        return v

    @validator("preferred_contract_duration")
    def validate_contract_duration(cls, v):
        if v:
            valid_durations = [
                "1-3 months",
                "3-6 months",
                "6-12 months",
                "1-2 years",
                "2+ years",
            ]
            if v not in valid_durations:
                raise ValueError(
                    f"Invalid contract duration. Must be one of {valid_durations}"
                )
        return v


class Education(BaseModel):
    institution: str
    degree: str
    field_of_study: str
    start_date: datetime
    end_date: Optional[datetime] = None
    current: bool = False
    description: Optional[str] = None
    gpa: Optional[float] = Field(None, ge=0, le=4.0)
    achievements: Optional[List[str]] = None
    location: Optional[str] = None
    accreditation: Optional[str] = None
    honors: Optional[List[str]] = None

    @validator("end_date")
    def validate_dates(cls, v, values):
        if v and "start_date" in values and v < values["start_date"]:
            raise ValueError("End date must be after start date")
        return v


class WorkExperience(BaseModel):
    company: str
    position: str
    location: Optional[str] = None
    start_date: datetime
    end_date: Optional[datetime] = None
    current: bool = False
    description: Optional[str] = None
    achievements: Optional[List[str]] = None
    skills_used: Optional[List[str]] = None
    employment_type: Optional[EmploymentType] = None
    work_schedule: Optional[WorkSchedule] = None
    salary: Optional[Dict[str, float]] = None
    currency: Optional[str] = Field(None, pattern="^[A-Z]{3}$")
    team_size: Optional[int] = Field(None, ge=1)
    reporting_to: Optional[str] = None
    technologies: Optional[List[str]] = None
    industry: Optional[str] = None

    @validator("end_date")
    def validate_dates(cls, v, values):
        if v and "start_date" in values and v < values["start_date"]:
            raise ValueError("End date must be after start date")
        return v

    @validator("salary")
    def validate_salary(cls, v):
        if v:
            if "amount" not in v:
                raise ValueError("Salary must include 'amount'")
            if v["amount"] < 0:
                raise ValueError("Salary amount cannot be negative")
        return v


class Portfolio(BaseModel):
    title: str
    description: str
    url: Optional[str] = None
    technologies: List[str]
    images: Optional[List[str]] = None
    github_url: Optional[str] = None
    live_url: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    current: bool = False
    collaborators: Optional[List[str]] = None
    role: Optional[str] = None
    impact: Optional[str] = None
    metrics: Optional[Dict[str, Any]] = None

    @validator("end_date")
    def validate_dates(cls, v, values):
        if v and "start_date" in values and v < values["start_date"]:
            raise ValueError("End date must be after start date")
        return v

    @validator("url", "github_url", "live_url")
    def validate_urls(cls, v):
        if v and not v.startswith(("http://", "https://")):
            raise ValueError("URL must start with http:// or https://")
        return v


class ProfilePictureMetadata(BaseModel):
    original_size: int
    compressed_size: int
    compression_ratio: float
    dimensions: tuple[int, int]
    format: str
    thumbnail_dimensions: Dict[str, tuple[int, int]]
    local_path: Optional[str] = None
    local_thumb_path: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class UserType(str, Enum):
    JOB_SEEKER = "job_seeker"
    EMPLOYER = "employer"
    ADMIN = "admin"


class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    display_name: Optional[str] = None
    user_type: UserType
    is_active: bool = True
    is_superuser: bool = False


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    display_name: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None


class UserResponse(UserBase):
    id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserInDB(UserBase):
    id: str
    hashed_password: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
