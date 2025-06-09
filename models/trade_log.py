# models/trade_log.py

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from core.database import Base


class TradeLog(Base):
    __tablename__ = "trade_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    symbol = Column(String, nullable=False)
    side = Column(String, nullable=False)  # "long" or "short"
    strategy = Column(String, nullable=True)
    entry_price = Column(Float, nullable=False)
    exit_price = Column(Float, nullable=False)
    quantity = Column(Float, nullable=False)
    profit_loss = Column(Float, nullable=False)
    is_demo = Column(Boolean, default=True)
    opened_at = Column(DateTime)
    closed_at = Column(DateTime)
    logged_at = Column(DateTime(timezone=True), server_default=func.now())
