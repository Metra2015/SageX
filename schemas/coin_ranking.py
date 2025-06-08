# schemas/coin_ranking.py

from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class CoinRankCreate(BaseModel):
    symbol: str
    score: float
    rank: int
    source: Optional[str] = "system"


class CoinRankResponse(BaseModel):
    id: int
    symbol: str
    score: float
    rank: int
    source: str
    created_at: datetime

    class Config:
        orm_mode = True
