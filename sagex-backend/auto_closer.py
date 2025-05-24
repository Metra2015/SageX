# auto_closer.py

from sqlalchemy.orm import Session
from core.database import SessionLocal
from services.open_position_service import get_user_open_positions, close_position_by_id
from models.historical_data import HistoricalData
from models.open_position import OpenPosition
from datetime import datetime
from decimal import Decimal


# CONFIG
TP_PERCENT = 0.05  # take profit if +5%
SL_PERCENT = 0.03  # stop loss if –3%


def fetch_current_price(db: Session, symbol: str):
    candle = db.query(HistoricalData).filter(
        HistoricalData.symbol == symbol.upper()
    ).order_by(HistoricalData.timestamp.desc()).first()
    return candle.close if candle else None


def should_close(entry_price: float, current_price: float, side: str):
    change = (Decimal(current_price) - Decimal(entry_price)) / Decimal(entry_price)
    if side == "short":
        change *= -1  # Invert logic for shorts

    if change >= Decimal(TP_PERCENT):
        return "tp"
    elif change <= -Decimal(SL_PERCENT):
        return "sl"
    return None


def auto_close_positions(user_id: int = 1, is_demo: bool = True):
    db: Session = SessionLocal()
    closed = []

    try:
        positions = get_user_open_positions(db, user_id, is_demo)
        for pos in positions:
            current_price = fetch_current_price(db, pos.symbol)
            if not current_price:
                continue

            trigger = should_close(pos.entry_price, current_price, pos.side)
            if trigger:
                close_position_by_id(db, pos.id)

                result = {
                    "symbol": pos.symbol,
                    "side": pos.side,
                    "entry": pos.entry_price,
                    "exit": current_price,
                    "qty": pos.quantity,
                    "type": trigger,
                    "pnl": round((current_price - pos.entry_price) * pos.quantity * (-1 if pos.side == "short" else 1), 2),
                    "closed_at": datetime.utcnow()
                }
                closed.append(result)
                print(f"🔒 {trigger.upper()} | Closed {pos.symbol} @ {current_price}: {result['pnl']} USD")

    finally:
        db.close()

    return closed


if __name__ == "__main__":
    auto_close_positions()
