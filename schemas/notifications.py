# schemas/notifications.py

from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class NotificationCreate(BaseModel):
    title: str
    message: str


class NotificationResponse(BaseModel):
    id: int
    title: str
    message: str
    is_read: bool
    created_at: datetime

    class Config:
        orm_mode = True


class NotificationMarkRead(BaseModel):
    notification_id: int
    read: Optional[bool] = True
