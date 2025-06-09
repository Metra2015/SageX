# core/trading_engine/mean_reversion.py

def mean_reversion_signal(price_data: list[float], window: int = 20, threshold: float = 1.5):
    """
    Simple Mean Reversion signal generator.
    - price_data: List of past prices (latest last)
    - window: Number of candles to use for moving average
    - threshold: How far price must deviate to trigger a signal
    Returns: "buy", "sell", or None
    """
    if len(price_data) < window:
        return None

    recent_prices = price_data[-window:]
    mean = sum(recent_prices) / window
    current_price = price_data[-1]

    if current_price < mean * (1 - threshold / 100):
        return "buy"
    elif current_price > mean * (1 + threshold / 100):
        return "sell"
    else:
        return None
