# trade_plan_runner.py

from sqlalchemy.orm import Session
from core.database import SessionLocal
from core.trading_engine.demo_manager import DemoTrader
from core.exchange import place_binance_market_order
from services.historical_data_service import get_candles


# ===== CONFIG =====
USE_REAL = False  # Set to True for live trade via Binance
CAPITAL = 1000.0
USER_ID = 1


def fetch_price_data(db: Session, symbol: str, window: int = 30):
    candles = get_candles(db, symbol, limit=window)
    if not candles:
        print(f"[{symbol}] No candle data found.")
        return None
    return [c.close for c in reversed(candles)]


def execute_plan(plan: dict, db: Session):
    print(f"\n🧠 Executing plan: {plan}")

    price_data = fetch_price_data(db, plan["symbol"])
    if not price_data:
        return

    current_price = price_data[-1]

    if USE_REAL:
        qty = round(CAPITAL / current_price, 5)
        result = place_binance_market_order(plan["symbol"], plan["signal"], qty)
        print(f"✅ [REAL] Order placed: {result}")
    else:
        demo = DemoTrader(USER_ID, plan["symbol"], plan["strategy"], price_data, capital=CAPITAL)
        result = demo.execute()
        print(f"🧪 [DEMO] Trade executed: {result}")


if __name__ == "__main__":
    # SAMPLE PLAN
    sample_plan = {
        "symbol": "BTCUSDT",
        "strategy": "mean_reversion",
        "signal": "buy"
    }

    db: Session = SessionLocal()
    try:
        execute_plan(sample_plan, db)
    finally:
        db.close()
