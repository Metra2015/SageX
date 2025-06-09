# models/historical_data.py

from sqlalchemy import Column, Integer, String, Float, DateTime
from core.database import Base


class HistoricalData(Base):
    __tablename__ = "historical_data"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    timeframe = Column(String, default="1m")  # "1m", "1h", "1d"
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Float)
    timestamp = Column(DateTime, index=True)
