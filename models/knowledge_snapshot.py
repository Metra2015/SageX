# models/knowledge_snapshot.py

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from core.database import Base


class KnowledgeSnapshot(Base):
    __tablename__ = "knowledge_snapshots"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    symbol = Column(String, nullable=False)
    side = Column(String, nullable=False)
    result = Column(String, nullable=False)  # "win", "loss", "neutral"
    pnl = Column(Float, nullable=False)
    entry_time = Column(DateTime)
    exit_time = Column(DateTime)
    is_demo = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
