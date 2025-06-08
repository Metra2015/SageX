# main_loop.py

from sqlalchemy.orm import Session
from core.database import SessionLocal
from core.ai_engine import choose_top_coins, get_trade_plan
from core.trading_engine.demo_manager import DemoTrader
from core.exchange import place_binance_market_order
from services.historical_data_service import get_candles
import time


CAPITAL = 1000.0
USE_REAL = False  # True = Binance trade; False = Demo trade
LOOP_INTERVAL = 60  # seconds


def fetch_latest_prices(db: Session, symbol: str, window: int = 30):
    candles = get_candles(db, symbol, limit=window)
    if not candles:
        return None
    return [c.close for c in reversed(candles)]


def execute_trade_plan(db: Session, plan: dict, user_id: int = 1):
    price_data = fetch_latest_prices(db, plan["symbol"])
    if not price_data:
        return

    if USE_REAL:
        # Calculate quantity to buy
        current_price = price_data[-1]
        qty = round(CAPITAL / current_price, 5)
        response = place_binance_market_order(plan["symbol"], plan["signal"], qty)
        print(f"✅ [REAL] {plan['signal']} {plan['symbol']} @ {current_price} → {response}")
    else:
        demo = DemoTrader(user_id, plan["symbol"], plan["strategy"], price_data, capital=CAPITAL)
        result = demo.execute()
        print(f"🧪 [DEMO] {plan['signal']} {plan['symbol']} → {result}")


def run_loop():
    db: Session = SessionLocal()
    print("🚀 Starting SageX main loop...")
    try:
        while True:
            top_coins = choose_top_coins(db, limit=5)
            print(f"\n🧠 Top coins: {top_coins}")

            for symbol in top_coins:
                price_data = fetch_latest_prices(db, symbol)
                if not price_data:
                    continue

                plan = get_trade_plan(db, symbol, price_data)
                if plan:
                    execute_trade_plan(db, plan)

            print("⏱ Sleeping...\n")
            time.sleep(LOOP_INTERVAL)

    except KeyboardInterrupt:
        print("🛑 Loop stopped by user.")
    finally:
        db.close()


if __name__ == "__main__":
    run_loop()
