from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

from app.schemas.base import TimestampSchema

class NotificationType(str, Enum):
    JOB_APPLICATION = "job_application"
    JOB_UPDATE = "job_update"
    PAYMENT = "payment"
    SYSTEM = "system"

class NotificationPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class NotificationStatus(str, Enum):
    UNREAD = "unread"
    READ = "read"
    ARCHIVED = "archived"

class NotificationBase(BaseModel):
    title: str
    message: str
    notification_type: NotificationType
    priority: NotificationPriority = NotificationPriority.MEDIUM
    status: NotificationStatus = NotificationStatus.UNREAD
    data: dict = Field(default_factory=dict)

class NotificationCreate(NotificationBase):
    user_id: str
    related_id: Optional[str] = None  # ID of related entity (job, application, etc.)

class NotificationUpdate(BaseModel):
    status: Optional[NotificationStatus] = None
    data: Optional[dict] = None

class NotificationResponse(TimestampSchema, NotificationBase):
    id: str
    user_id: str
    related_id: Optional[str] = None
    read_at: Optional[datetime] = None 