from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum

class NotificationStatus(str, Enum):
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"
    READ = "read"

class NotificationBase(BaseModel):
    user_id: int
    message: str
    status: Optional[NotificationStatus] = NotificationStatus.PENDING


class NotificationCreate(NotificationBase):
    pass

class NotificationUpdate(BaseModel):
    message: Optional[str] = None
    status: Optional[NotificationStatus] = None


class NotificationResponse(NotificationBase):
    id: int
    created_at: datetime
    updated_at: datetime