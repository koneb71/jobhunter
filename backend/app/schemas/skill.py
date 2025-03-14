from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class SkillBase(BaseModel):
    name: str
    description: Optional[str] = None
    category: Optional[str] = None

class SkillCreate(SkillBase):
    pass

class SkillUpdate(SkillBase):
    name: Optional[str] = None

class SkillInDBBase(SkillBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Skill(SkillInDBBase):
    pass

class SkillInDB(SkillInDBBase):
    pass 