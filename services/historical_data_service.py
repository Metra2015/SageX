# services/historical_data_service.py

from sqlalchemy.orm import Session
from models.historical_data import HistoricalData
from schemas.historical_data import HistoricalCandleCreate
from datetime import datetime


def insert_candle(db: Session, candle: HistoricalCandleCreate):
    new_candle = HistoricalData(**candle.dict())
    db.add(new_candle)
    db.commit()
    db.refresh(new_candle)
    return new_candle


def get_candles(
    db: Session,
    symbol: str,
    timeframe: str = "1m",
    limit: int = 100,
    before: datetime = None
):
    query = db.query(HistoricalData).filter(
        HistoricalData.symbol == symbol.upper(),
        HistoricalData.timeframe == timeframe
    )

    if before:
        query = query.filter(HistoricalData.timestamp <= before)

    return query.order_by(HistoricalData.timestamp.desc()).limit(limit).all()
