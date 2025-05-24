# api/notifications.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.notifications import NotificationCreate, NotificationResponse, NotificationMarkRead
from services.notification_service import create_notification, get_user_notifications, mark_notification_read
from core.database import get_db

router = APIRouter()


@router.post("/", response_model=NotificationResponse)
def send_notification(data: NotificationCreate, db: Session = Depends(get_db)):
    user_id = 1  # Simulated user
    return create_notification(db, user_id, data)


@router.get("/", response_model=list[NotificationResponse])
def fetch_notifications(db: Session = Depends(get_db)):
    user_id = 1  # Simulated user
    return get_user_notifications(db, user_id)


@router.post("/read", response_model=NotificationResponse)
def mark_read(data: NotificationMarkRead, db: Session = Depends(get_db)):
    user_id = 1  # Simulated user
    result = mark_notification_read(db, user_id, data.notification_id, data.read)
    if not result:
        raise HTTPException(status_code=404, detail="Notification not found.")
    return result
