from typing import Optional

from pydantic import BaseModel, Field, HttpUrl

from app.schemas.base import TimestampSchema


class CompanyBase(BaseModel):
    name: str
    description: str
    website: Optional[HttpUrl] = None
    logo_url: Optional[HttpUrl] = None
    industry: Optional[str] = None
    size: Optional[str] = Field(
        None, description="Company size range (e.g., '1-10', '11-50', '51-200', etc.)"
    )
    location: Optional[str] = None
    is_active: bool = True


class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(CompanyBase):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class CompanyResponse(TimestampSchema, CompanyBase):
    id: str
    created_by: str
    jobs_count: int = 0
