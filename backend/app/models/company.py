from typing import Optional
from pydantic import BaseModel, HttpUrl
from datetime import datetime

class Company(BaseModel):
    id: str
    name: str
    description: str
    website: Optional[HttpUrl] = None
    logo_url: Optional[HttpUrl] = None
    industry: Optional[str] = None
    size: Optional[str] = None
    location: Optional[str] = None
    is_active: bool = True
    created_by: str
    created_at: datetime
    updated_at: datetime 