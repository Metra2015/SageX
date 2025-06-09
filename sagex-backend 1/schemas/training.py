# schemas/training.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TrainingStart(BaseModel):
    start_balance: float
    target_balance: float
    days: Optional[int] = 30


class TrainingEnd(BaseModel):
    final_balance: float


class TrainingStatus(BaseModel):
    id: int
    start_balance: float
    target_balance: float
    days: int
    started_at: datetime
    ended_at: Optional[datetime]
    success: Optional[bool]

    class Config:
        orm_mode = True
