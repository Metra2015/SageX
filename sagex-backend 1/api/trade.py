# api/trade.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.trade import TradeCreate, TradeClose, TradeResponse
from services.trade_service import open_trade, close_trade, get_user_trades
from core.database import get_db
from models.trade import Trade

# For now, we'll simulate authentication with user_id = 1 (replace with real user later)
router = APIRouter()


@router.post("/open", response_model=TradeResponse)
def create_trade(trade: TradeCreate, db: Session = Depends(get_db)):
    # Simulated user_id
    user_id = 1
    return open_trade(db, user_id, trade)


@router.post("/close", response_model=TradeResponse)
def close_trade_route(data: TradeClose, db: Session = Depends(get_db)):
    user_id = 1  # Simulated user_id
    closed = close_trade(db, user_id, data)
    if not closed:
        raise HTTPException(status_code=404, detail="Trade not found or already closed")
    return closed


@router.get("/", response_model=list[TradeResponse])
def list_user_trades(is_demo: bool = False, db: Session = Depends(get_db)):
    user_id = 1  # Simulated user_id
    return get_user_trades(db, user_id, is_demo)
