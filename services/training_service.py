# services/training_service.py

from sqlalchemy.orm import Session
from models.training_log import TrainingLog
from schemas.training import TrainingStart, TrainingEnd
from datetime import datetime


def start_training(db: Session, user_id: int, data: TrainingStart):
    # End any active training first
    active = db.query(TrainingLog).filter(
        TrainingLog.user_id == user_id,
        TrainingLog.success == None
    ).first()
    if active:
        return None  # Already training

    new_session = TrainingLog(
        user_id=user_id,
        start_balance=data.start_balance,
        target_balance=data.target_balance,
        days=data.days
    )
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return new_session


def end_training(db: Session, user_id: int, data: TrainingEnd):
    active = db.query(TrainingLog).filter(
        TrainingLog.user_id == user_id,
        TrainingLog.success == None
    ).first()

    if not active:
        return None

    active.ended_at = datetime.utcnow()
    active.success = data.final_balance >= active.target_balance
    db.commit()
    db.refresh(active)
    return active


def get_training_status(db: Session, user_id: int):
    return db.query(TrainingLog).filter(
        TrainingLog.user_id == user_id
    ).order_by(TrainingLog.started_at.desc()).all()
