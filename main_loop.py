
# main_loop.py (Updated Version)

import os
import logging
import time
from sqlalchemy.orm import Session
from core.config import settings
from core.database import SessionLocal
from core.ai_engine import choose_top_coins, get_trade_plan
from core.trading_engine.demo_manager import DemoTrader
from core.exchange import place_market_order
from services.historical_data_service import get_candles
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

# Logging setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Configs
CAPITAL = settings.CAPITAL
USE_REAL = settings.USE_REAL
EXCHANGE = settings.EXCHANGE
LOOP_INTERVAL = settings.LOOP_INTERVAL

def fetch_latest_prices(db: Session, symbol: str, window: int = 30):
    candles = get_candles(db, symbol, limit=window)
    if not candles:
        return None
    return [c.close for c in reversed(candles)]

def log_trade_result(symbol, signal, price, result, pnl=None):
    os.makedirs("logs", exist_ok=True)
    with open("logs/trade_results.csv", "a") as f:
        f.write(f"{datetime.utcnow()},{symbol},{signal},{price},{pnl},{result}\n")

def execute_trade_plan(db: Session, plan: dict, user_id: int = 1):
    try:
        price_data = fetch_latest_prices(db, plan["symbol"])
        if not price_data:
            return

        current_price = price_data[-1]
        if USE_REAL:
            qty = round(CAPITAL / current_price, 5)
            response = place_market_order(plan["symbol"], plan["signal"], qty, exchange=EXCHANGE)
            logging.info(f"[REAL] {plan['signal']} {plan['symbol']} @ {current_price} → {response}")
            log_trade_result(plan["symbol"], plan["signal"], current_price, result="real", pnl=None)
        else:
            demo = DemoTrader(user_id, plan["symbol"], plan["strategy"], price_data, capital=CAPITAL)
            result = demo.execute()
            logging.info(f"[DEMO] {plan['signal']} {plan['symbol']} → {result}")
            log_trade_result(plan["symbol"], plan["signal"], current_price, result=result)

    except Exception as e:
        logging.error(f"Error executing trade plan: {e}")

def run_loop():
    db: Session = SessionLocal()
    try:
        logging.info("Running SageX trading loop...")
        top_coins = choose_top_coins(db, limit=5)
        logging.info(f"Top coins: {top_coins}")

        for symbol in top_coins:
            price_data = fetch_latest_prices(db, symbol)
            if not price_data:
                continue

            plan = get_trade_plan(db, symbol, price_data)
            if plan:
                execute_trade_plan(db, plan)

    except Exception as e:
        logging.error(f"Loop error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_loop, 'interval', seconds=LOOP_INTERVAL)
    scheduler.start()
    logging.info("Scheduler started. Press Ctrl+C to exit.")
    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        logging.info("Scheduler stopped.")
