# core/trading_engine/momentum_breakout.py

def momentum_breakout_signal(price_data: list[float], window: int = 20) -> str | None:
    """
    Basic momentum breakout strategy.
    - If current price breaks above highest high in `window`, signal 'buy'
    - If it breaks below lowest low in `window`, signal 'sell'
    - Else: no signal
    """
    if len(price_data) < window:
        return None

    recent_prices = price_data[-window:]
    current_price = price_data[-1]

    highest = max(recent_prices)
    lowest = min(recent_prices)

    if current_price > highest:
        return "buy"
    elif current_price < lowest:
        return "sell"
    else:
        return None
