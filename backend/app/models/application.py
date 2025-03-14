from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Application(BaseModel):
    id: str
    user_id: str
    job_id: str
    cover_letter: Optional[str] = None
    resume_url: Optional[str] = None
    status: str
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime
