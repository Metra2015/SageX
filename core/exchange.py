# core/exchange.py

import requests
import time
import hmac
import hashlib
import os

BINANCE_API_KEY = os.getenv("fowy91qSXBE06FClmi9kK7zG8t59xNJy4i3SZh3rxFbJTVmv7jxKiLgaZoB2vPKD")
BINANCE_SECRET = os.getenv("6w7hAAgm0lVkf79Jh3opVEoFdLsTmEvG7JtzkAjcfAGzrwRGhoA6UTp5ymvC5laX")

BYBIT_API_KEY = os.getenv("81a3UsuGI0xsUja7lN")
BYBIT_SECRET = os.getenv("KmoibXFLxplHjy1uzWpPhu93NXg7pL89U493")


### BINANCE FUNCTIONS

def binance_headers():
    return {
        "X-MBX-APIKEY": BINANCE_API_KEY
    }


def binance_sign(params: dict):
    query = "&".join([f"{k}={v}" for k, v in params.items()])
    signature = hmac.new(BINANCE_SECRET.encode(), query.encode(), hashlib.sha256).hexdigest()
    return f"{query}&signature={signature}"


def place_binance_market_order(symbol: str, side: str, quantity: float):
    url = "https://api.binance.com/api/v3/order"
    timestamp = int(time.time() * 1000)
    params = {
        "symbol": symbol.upper(),
        "side": side.upper(),
        "type": "MARKET",
        "quantity": quantity,
        "timestamp": timestamp
    }
    query = binance_sign(params)
    full_url = f"{url}?{query}"
    response = requests.post(full_url, headers=binance_headers())
    return response.json()


def get_binance_balance(asset: str = "USDT"):
    url = "https://api.binance.com/api/v3/account"
    timestamp = int(time.time() * 1000)
    query = binance_sign({"timestamp": timestamp})
    full_url = f"{url}?{query}"
    response = requests.get(full_url, headers=binance_headers())
    balances = response.json().get("balances", [])
    for b in balances:
        if b["asset"] == asset.upper():
            return float(b["free"])
    return 0.0


### BYBIT FUNCTIONS

def bybit_sign(params: dict):
    query = "&".join([f"{k}={v}" for k, v in sorted(params.items())])
    signature = hmac.new(BYBIT_SECRET.encode(), query.encode(), hashlib.sha256).hexdigest()
    return signature


def place_bybit_market_order(symbol: str, side: str, qty: float):
    url = "https://api.bybit.com/v2/private/order/create"
    timestamp = int(time.time() * 1000)
    params = {
        "api_key": BYBIT_API_KEY,
        "symbol": symbol.upper(),
        "side": side.upper(),
        "order_type": "Market",
        "qty": qty,
        "time_in_force": "GoodTillCancel",
        "timestamp": timestamp
    }
    params["sign"] = bybit_sign(params)
    response = requests.post(url, data=params)
    return response.json()


def get_bybit_balance(asset: str = "USDT"):
    url = "https://api.bybit.com/v2/private/wallet/balance"
    timestamp = int(time.time() * 1000)
    params = {
        "api_key": BYBIT_API_KEY,
        "timestamp": timestamp
    }
    params["sign"] = bybit_sign(params)
    response = requests.get(url, params=params)
    return float(response.json()["result"][asset]["available_balance"])
