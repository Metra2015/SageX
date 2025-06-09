# schemas/trade_log.py

from pydantic import BaseModel
from datetime import datetime


class TradeLogCreate(BaseModel):
    user_id: int
    symbol: str
    side: str
    strategy: str
    entry_price: float
    exit_price: float
    quantity: float
    profit_loss: float
    is_demo: bool
    opened_at: datetime
    closed_at: datetime


class TradeLogResponse(TradeLogCreate):
    id: int
    logged_at: datetime

    class Config:
        orm_mode = True
