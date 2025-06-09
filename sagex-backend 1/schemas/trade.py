# schemas/trade.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TradeCreate(BaseModel):
    symbol: str
    side: str  # "long" or "short"
    entry_price: float
    quantity: float
    is_demo: Optional[bool] = False


class TradeClose(BaseModel):
    trade_id: int
    exit_price: float


class TradeResponse(BaseModel):
    id: int
    symbol: str
    side: str
    entry_price: float
    exit_price: Optional[float]
    quantity: float
    profit_loss: Optional[float]
    is_closed: bool
    is_demo: bool
    opened_at: datetime
    closed_at: Optional[datetime]

    class Config:
        orm_mode = True
