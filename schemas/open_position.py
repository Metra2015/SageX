# schemas/open_position.py

from pydantic import BaseModel
from datetime import datetime


class OpenPositionCreate(BaseModel):
    user_id: int
    symbol: str
    strategy: str
    side: str
    entry_price: float
    quantity: float
    is_demo: bool = True


class OpenPositionResponse(BaseModel):
    id: int
    user_id: int
    symbol: str
    strategy: str
    side: str
    entry_price: float
    quantity: float
    is_demo: bool
    opened_at: datetime

    class Config:
        orm_mode = True
