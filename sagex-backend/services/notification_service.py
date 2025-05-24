# services/notification_service.py

from sqlalchemy.orm import Session
from models.notification import Notification
from schemas.notifications import NotificationCreate


def create_notification(db: Session, user_id: int, data: NotificationCreate):
    note = Notification(
        user_id=user_id,
        title=data.title,
        message=data.message
    )
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


def get_user_notifications(db: Session, user_id: int):
    return db.query(Notification).filter(
        Notification.user_id == user_id
    ).order_by(Notification.created_at.desc()).all()


def mark_notification_read(db: Session, user_id: int, notification_id: int, read: bool = True):
    note = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.user_id == user_id
    ).first()

    if not note:
        return None

    note.is_read = read
    db.commit()
    db.refresh(note)
    return note
