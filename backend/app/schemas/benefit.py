from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class BenefitBase(BaseModel):
    name: str
    description: Optional[str] = None
    category: Optional[str] = None

class BenefitCreate(BenefitBase):
    pass

class BenefitUpdate(BenefitBase):
    name: Optional[str] = None

class BenefitInDBBase(BenefitBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Benefit(BenefitInDBBase):
    pass

class BenefitInDB(BenefitInDBBase):
    pass 