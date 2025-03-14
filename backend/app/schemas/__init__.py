"""
Schemas package for Pydantic models.
"""

from .auth import Token, TokenPayload
from .company import CompanyCreate, CompanyResponse, CompanyUpdate
from .job import JobCreate, JobResponse, JobUpdate
from .job_application import (
    ApplicationStatus,
    JobApplicationCreate,
    JobApplicationResponse,
    JobApplicationUpdate,
)
from .notification import NotificationCreate, NotificationResponse, NotificationUpdate
from .payment import PaymentCreate, PaymentResponse, PaymentUpdate
from .search import SearchParams, SearchResponse
from .user import UserCreate, UserResponse, UserUpdate
from .verification import (
    VerificationRequestCreate,
    VerificationRequestResponse,
    VerificationRequestUpdate,
)

__all__ = [
    "JobApplicationCreate",
    "JobApplicationUpdate",
    "JobApplicationResponse",
    "ApplicationStatus",
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "JobCreate",
    "JobUpdate",
    "JobResponse",
    "CompanyCreate",
    "CompanyUpdate",
    "CompanyResponse",
    "NotificationCreate",
    "NotificationUpdate",
    "NotificationResponse",
    "PaymentCreate",
    "PaymentUpdate",
    "PaymentResponse",
    "VerificationRequestCreate",
    "VerificationRequestUpdate",
    "VerificationRequestResponse",
    "Token",
    "TokenPayload",
    "SearchParams",
    "SearchResponse",
]
