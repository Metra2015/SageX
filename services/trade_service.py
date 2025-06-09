# services/trade_service.py

from sqlalchemy.orm import Session
from models.trade import Trade
from schemas.trade import TradeCreate, TradeClose
from datetime import datetime


def open_trade(db: Session, user_id: int, trade_data: TradeCreate):
    trade = Trade(
        user_id=user_id,
        symbol=trade_data.symbol.upper(),
        side=trade_data.side.lower(),
        entry_price=trade_data.entry_price,
        quantity=trade_data.quantity,
        is_demo=trade_data.is_demo
    )
    db.add(trade)
    db.commit()
    db.refresh(trade)
    return trade


def close_trade(db: Session, user_id: int, data: TradeClose):
    trade = db.query(Trade).filter(
        Trade.id == data.trade_id,
        Trade.user_id == user_id,
        Trade.is_closed == False
    ).first()

    if not trade:
        return None

    trade.exit_price = data.exit_price
    trade.profit_loss = (data.exit_price - trade.entry_price) * trade.quantity
    if trade.side == "short":
        trade.profit_loss *= -1

    trade.is_closed = True
    trade.closed_at = datetime.utcnow()
    db.commit()
    db.refresh(trade)
    return trade


def get_user_trades(db: Session, user_id: int, is_demo: bool = False):
    return db.query(Trade).filter(
        Trade.user_id == user_id,
        Trade.is_demo == is_demo
    ).order_by(Trade.opened_at.desc()).all()
