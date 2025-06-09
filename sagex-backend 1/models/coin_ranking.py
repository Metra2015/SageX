# models/coin_ranking.py

from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from core.database import Base


class CoinRanking(Base):
    __tablename__ = "coin_rankings"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, nullable=False)
    score = Column(Float, nullable=False)  # e.g. volatility, momentum, etc.
    rank = Column(Integer, nullable=False)
    source = Column(String, default="system")  # "system", "user", "external"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
