from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class ProfileStrength(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


class ProfileVerificationStatus(str, Enum):
    UNVERIFIED = "unverified"
    PENDING = "pending"
    VERIFIED = "verified"
    REJECTED = "rejected"


class SkillLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


class ProfileScore(BaseModel):
    completion_percentage: float = Field(ge=0, le=100)
    strength: ProfileStrength
    missing_fields: List[str] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)
    last_updated: Optional[str] = None


class SkillEndorsement(BaseModel):
    skill: str
    endorser_id: str
    endorser_name: str
    endorsement_date: str
    comment: Optional[str] = None


class SkillRating(BaseModel):
    skill: str
    level: SkillLevel
    years_of_experience: Optional[float] = None
    endorsements: List[SkillEndorsement] = Field(default_factory=list)
    last_used: Optional[str] = None
    verified: bool = False


class ProfileVerification(BaseModel):
    status: ProfileVerificationStatus = ProfileVerificationStatus.UNVERIFIED
    verified_fields: List[str] = Field(default_factory=list)
    verification_date: Optional[str] = None
    verified_by: Optional[str] = None
    notes: Optional[str] = None


class ProfileAnalytics(BaseModel):
    views: int = 0
    unique_views: int = 0
    last_viewed: Optional[str] = None
    search_appearances: int = 0
    profile_completion_history: List[Dict[str, Any]] = Field(default_factory=list)
    skill_trends: List[Dict[str, Any]] = Field(default_factory=list)
    preference_changes: List[Dict[str, Any]] = Field(default_factory=list)


class SearchCriteria(BaseModel):
    skills: Optional[List[str]] = None
    experience_years: Optional[float] = None
    education_level: Optional[str] = None
    location: Optional[str] = None
    employment_type: Optional[List[str]] = None
    work_schedule: Optional[List[str]] = None
    salary_range: Optional[Dict[str, float]] = None
    company_size: Optional[List[str]] = None
    benefits: Optional[List[str]] = None
    availability: Optional[str] = None
    languages: Optional[List[str]] = None
    certifications: Optional[List[str]] = None
    keywords: Optional[str] = None
    sort_by: Optional[str] = None
    sort_order: Optional[str] = "desc"
    page: int = 1
    per_page: int = 20


class SearchResult(BaseModel):
    total_count: int
    page: int
    per_page: int
    total_pages: int
    results: List[Dict[str, Any]]
    facets: Optional[Dict[str, Any]] = None
    suggestions: Optional[List[str]] = None
