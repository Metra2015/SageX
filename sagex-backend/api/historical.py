# api/historical.py

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from schemas.historical_data import HistoricalCandleCreate, HistoricalCandleResponse
from services.historical_data_service import insert_candle, get_candles
from core.database import get_db
from datetime import datetime

router = APIRouter()


@router.post("/", response_model=HistoricalCandleResponse)
def upload_candle(candle: HistoricalCandleCreate, db: Session = Depends(get_db)):
    return insert_candle(db, candle)


@router.get("/", response_model=list[HistoricalCandleResponse])
def fetch_candles(
    symbol: str,
    timeframe: str = "1m",
    limit: int = Query(100, le=500),
    before: datetime = None,
    db: Session = Depends(get_db)
):
    return get_candles(db, symbol, timeframe, limit, before)
