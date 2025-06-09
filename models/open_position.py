# models/open_position.py

from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from core.database import Base


class OpenPosition(Base):
    __tablename__ = "open_positions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    symbol = Column(String, nullable=False)
    strategy = Column(String, nullable=False)
    side = Column(String, nullable=False)  # "long" or "short"
    entry_price = Column(Float, nullable=False)
    quantity = Column(Float, nullable=False)
    is_demo = Column(Boolean, default=True)
    opened_at = Column(DateTime(timezone=True), server_default=func.now())
