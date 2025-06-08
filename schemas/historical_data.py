# schemas/historical_data.py

from pydantic import BaseModel
from datetime import datetime


class HistoricalCandleCreate(BaseModel):
    symbol: str
    timeframe: str
    open: float
    high: float
    low: float
    close: float
    volume: float
    timestamp: datetime


class HistoricalCandleResponse(BaseModel):
    id: int
    symbol: str
    timeframe: str
    open: float
    high: float
    low: float
    close: float
    volume: float
    timestamp: datetime

    class Config:
        orm_mode = True
