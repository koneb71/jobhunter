from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base
import uuid
from enum import Enum

class NotificationType(str, Enum):
    JOB_APPLICATION = "job_application"
    JOB_UPDATE = "job_update"
    PROFILE_VIEW = "profile_view"
    VERIFICATION = "verification"
    SYSTEM = "system"
    PAYMENT = "payment"

class NotificationStatus(str, Enum):
    UNREAD = "unread"
    READ = "read"
    ARCHIVED = "archived"

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    type = Column(SQLAlchemyEnum(NotificationType, name="notification_type_enum"), nullable=False)
    title = Column(String, nullable=False)
    message = Column(String, nullable=False)
    status = Column(SQLAlchemyEnum(NotificationStatus, name="notification_status_enum"), default=NotificationStatus.UNREAD)
    created_at = Column(DateTime, default=datetime.utcnow)
    read_at = Column(DateTime, nullable=True)
    notification_data = Column(String, nullable=True)  # JSON string for additional data
    link = Column(String, nullable=True)  # URL to related content

    # Relationships
    user = relationship("User", back_populates="notifications") 