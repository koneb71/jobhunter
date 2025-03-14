from typing import Optional, List, Dict, Any
from pydantic import BaseModel, EmailStr
from datetime import datetime

from app.schemas.user import (
    UserRole, AvailabilityStatus, EmploymentType,
    WorkSchedule, EmploymentPreferences, ProfilePictureMetadata
)

class Education(BaseModel):
    institution: str
    degree: str
    field_of_study: str
    start_date: datetime
    end_date: Optional[datetime] = None
    current: bool = False
    description: Optional[str] = None
    gpa: Optional[float] = None
    achievements: Optional[List[str]] = None

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

class Portfolio(BaseModel):
    title: str
    description: str
    url: Optional[str] = None
    technologies: List[str]
    images: Optional[List[str]] = None
    github_url: Optional[str] = None
    live_url: Optional[str] = None

class User(BaseModel):
    id: str
    email: str
    is_active: bool = True
    is_superuser: bool = False
    role: str  # "employer" or "job_seeker"
    full_name: Optional[str] = None
    company_id: Optional[str] = None
    profile_picture: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True

    def __init__(self, **data):
        super().__init__(**data)
        self.first_name, self.last_name = self.full_name.split(' ', 1) if self.full_name else (None, None)
        self.phone = None  # Assuming phone is not provided in the input
        self.tagline = None
        self.profile_overview = None
        self.location = None
        self.availability_status = AvailabilityStatus.AVAILABLE
        self.expected_salary = None
        self.skills = []
        self.education = []
        self.work_experience = []
        self.portfolio = []
        self.languages = []
        self.certifications = []
        self.social_links = {}
        self.employment_preferences = EmploymentPreferences()
        self.preferences = {}
        self.hashed_password = None
        self.profile_picture_thumb = None
        self.profile_picture_updated_at = None
        self.profile_picture_metadata = None

    def __str__(self):
        return f"{self.first_name} {self.last_name}" if self.first_name and self.last_name else self.email

    def __repr__(self):
        return f"<User {self.email}>"

    def __eq__(self, other):
        if isinstance(other, User):
            return self.email == other.email
        return False

    def __hash__(self):
        return hash(self.email)

    def update(self, **data):
        for key, value in data.items():
            if key in self.__fields__:
                setattr(self, key, value)
        self.full_name = f"{self.first_name} {self.last_name}" if self.first_name and self.last_name else None
        return self

    def is_employer(self):
        return self.role == "employer"

    def is_job_seeker(self):
        return self.role == "job_seeker"

    def update_profile_picture(self, picture_url):
        self.profile_picture = picture_url
        self.profile_picture_thumb = picture_url.split('/')[-1] if picture_url else None
        self.profile_picture_updated_at = datetime.now().isoformat()
        self.profile_picture_metadata = ProfilePictureMetadata(
            original_url=picture_url,
            thumbnail_url=self.profile_picture_thumb
        )
        return self

    def update_profile_overview(self, tagline, overview):
        self.tagline = tagline
        self.profile_overview = overview
        return self

    def update_location(self, location):
        self.location = location
        return self

    def update_availability_status(self, status):
        self.availability_status = status
        return self

    def update_expected_salary(self, salary):
        self.expected_salary = salary
        return self

    def add_skill(self, skill):
        if skill not in self.skills:
            self.skills.append(skill)
        return self

    def remove_skill(self, skill):
        self.skills.remove(skill)
        return self

    def add_education(self, education):
        self.education.append(education)
        return self

    def remove_education(self, education):
        self.education.remove(education)
        return self

    def add_work_experience(self, work_experience):
        self.work_experience.append(work_experience)
        return self

    def remove_work_experience(self, work_experience):
        self.work_experience.remove(work_experience)
        return self

    def add_portfolio(self, portfolio):
        self.portfolio.append(portfolio)
        return self

    def remove_portfolio(self, portfolio):
        self.portfolio.remove(portfolio)
        return self

    def add_language(self, language):
        self.languages.append(language)
        return self

    def remove_language(self, language):
        self.languages.remove(language)
        return self

    def add_certification(self, certification):
        self.certifications.append(certification)
        return self

    def remove_certification(self, certification):
        self.certifications.remove(certification)
        return self

    def add_social_link(self, platform, link):
        self.social_links[platform] = link
        return self

    def remove_social_link(self, platform):
        self.social_links.pop(platform, None)
        return self

    def update_employment_preferences(self, preferences):
        self.employment_preferences = preferences
        return self

    def update_preferences(self, preferences):
        self.preferences = preferences
        return self

    def update_password(self, hashed_password):
        self.hashed_password = hashed_password
        return self

    def update_company_id(self, company_id):
        self.company_id = company_id
        return self

    def update_created_at(self, created_at):
        self.created_at = created_at
        return self

    def update_updated_at(self, updated_at):
        self.updated_at = updated_at
        return self

    def update_full_name(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name
        self.full_name = f"{first_name} {last_name}" if first_name and last_name else None
        return self

    def update_phone(self, phone):
        self.phone = phone
        return self

    def update_role(self, role):
        self.role = role
        return self

    def update_is_active(self, is_active):
        self.is_active = is_active
        return self

    def update_is_superuser(self, is_superuser):
        self.is_superuser = is_superuser
        return self

    def update_profile_picture_thumb(self, profile_picture_thumb):
        self.profile_picture_thumb = profile_picture_thumb
        return self

    def update_profile_picture_updated_at(self, profile_picture_updated_at):
        self.profile_picture_updated_at = profile_picture_updated_at
        return self

    def update_profile_picture_metadata(self, profile_picture_metadata):
        self.profile_picture_metadata = profile_picture_metadata
        return self

    def update_profile_overview(self, profile_overview):
        self.profile_overview = profile_overview
        return self

    def update_location(self, location):
        self.location = location
    profile_picture_thumb: Optional[str] = None
    profile_picture_updated_at: Optional[str] = None
    profile_picture_metadata: Optional[ProfilePictureMetadata] = None
    tagline: Optional[str] = None
    profile_overview: Optional[str] = None
    location: Optional[str] = None
    availability_status: AvailabilityStatus = AvailabilityStatus.AVAILABLE
    expected_salary: Optional[float] = None
    skills: List[str] = []
    education: List[Education] = []
    work_experience: List[WorkExperience] = []
    portfolio: List[Portfolio] = []
    languages: List[Dict[str, str]] = []
    certifications: List[Dict[str, str]] = []
    social_links: Dict[str, str] = {}
    employment_preferences: EmploymentPreferences = EmploymentPreferences()
    preferences: Dict[str, Any] = {}
    hashed_password: str
    created_at: datetime
    updated_at: datetime 