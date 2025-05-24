# binance_fetcher.py

import requests
from datetime import datetime
from time import sleep
import pytz
import os
from sqlalchemy.orm import Session
from core.database import SessionLocal
from schemas.historical_data import HistoricalCandleCreate
from services.historical_data_service import insert_candle


BINANCE_BASE_URL = "https://api.binance.com/api/v3/klines"


def fetch_binance_candles(symbol: str, interval: str = "1m", limit: int = 100):
    symbol = symbol.upper()
    url = f"{BINANCE_BASE_URL}?symbol={symbol}&interval={interval}&limit={limit}"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Binance API error: {response.text}")
    return response.json()


def convert_to_schema(data, symbol: str, interval: str):
    """
    Converts Binance kline response to HistoricalCandleCreate schemas
    """
    candles = []
    for d in data:
        candle = HistoricalCandleCreate(
            symbol=symbol,
            timeframe=interval,
            open=float(d[1]),
            high=float(d[2]),
            low=float(d[3]),
            close=float(d[4]),
            volume=float(d[5]),
            timestamp=datetime.fromtimestamp(d[0] / 1000, tz=pytz.UTC)
        )
        candles.append(candle)
    return candles


def import_binance_data(symbol: str, interval: str = "1m", limit: int = 100):
    raw = fetch_binance_candles(symbol, interval, limit)
    candles = convert_to_schema(raw, symbol, interval)
    db: Session = SessionLocal()
    imported = 0
    for candle in candles:
        insert_candle(db, candle)
        imported += 1
    db.close()
    print(f"[{symbol}] Imported {imported} candles.")
    return imported


if __name__ == "__main__":
    pairs = ["BTCUSDT", "ETHUSDT", "XRPUSDT", "SOLUSDT"]
    for pair in pairs:
        try:
            import_binance_data(pair, interval="1m", limit=100)
            sleep(1.5)  # Avoid rate limit
        except Exception as e:
            print(f"Failed to import {pair}: {str(e)}")
