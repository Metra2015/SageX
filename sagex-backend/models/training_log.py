# models/training_log.py

from sqlalchemy import Column, Integer, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from core.database import Base


class TrainingLog(Base):
    __tablename__ = "training_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    start_balance = Column(Float, nullable=False)
    target_balance = Column(Float, nullable=False)
    days = Column(Integer, default=30)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    ended_at = Column(DateTime(timezone=True), nullable=True)
    success = Column(Boolean, default=None)  # True, False, or None if in progress
