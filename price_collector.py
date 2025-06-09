import time
import requests
import sqlite3
from datetime import datetime

def fetch_binance_price(symbol="BTCUSDT"):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    try:
        res = requests.get(url)
        return float(res.json()["price"])
    except Exception as e:
        print(f"Fetch failed: {e}")
        return None

def store_price(symbol, price):
    conn = sqlite3.connect("sagex.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS price_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT,
            price REAL,
            timestamp TEXT
        )
    """)
    cursor.execute("""
        INSERT INTO price_data (symbol, price, timestamp)
        VALUES (?, ?, ?)
    """, (symbol, price, datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()

def run_collector(interval=60):
    while True:
        price = fetch_binance_price()
        if price:
            store_price("BTCUSDT", price)
            print(f"[+] Logged price: {price}")
        time.sleep(interval)

if __name__ == "__main__":
    run_collector()
