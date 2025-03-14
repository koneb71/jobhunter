from typing import Optional
from pydantic import BaseModel, EmailStr

from app.schemas.base import TimestampSchema
from app.schemas.user import UserResponse

class Token(BaseModel):
    access_token: str
    token_type: str
    user: Optional[UserResponse] = None

class TokenPayload(BaseModel):
    sub: Optional[int] = None

class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False
    full_name: Optional[str] = None

class UserCreate(UserBase):
    email: EmailStr
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None

class UserResponse(TimestampSchema, UserBase):
    id: str
    email: EmailStr 