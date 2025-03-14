from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class Notification(BaseModel):
    id: str
    user_id: str
    title: str
    message: str
    notification_type: str
    priority: str
    status: str
    data: dict
    related_id: Optional[str] = None
    read_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime 