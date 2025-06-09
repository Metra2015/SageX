# schemas/knowledge.py

from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class SnapshotCreate(BaseModel):
    symbol: str
    side: str  # "long" or "short"
    result: str  # "win", "loss", "neutral"
    pnl: float
    entry_time: datetime
    exit_time: datetime
    is_demo: Optional[bool] = False


class SnapshotResponse(BaseModel):
    id: int
    symbol: str
    side: str
    result: str
    pnl: float
    entry_time: datetime
    exit_time: datetime
    is_demo: bool
    created_at: datetime

    class Config:
        orm_mode = True
