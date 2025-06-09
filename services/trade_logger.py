# services/trade_logger.py

from sqlalchemy.orm import Session
from models.trade_log import TradeLog
from schemas.trade_log import TradeLogCreate


def log_trade(db: Session, trade: TradeLogCreate):
    log = TradeLog(**trade.dict())
    db.add(log)
    db.commit()
    db.refresh(log)
    return log
