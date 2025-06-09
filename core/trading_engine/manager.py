# core/trading_engine/manager.py

from core.trading_engine.mean_reversion import mean_reversion_signal
from core.trading_engine.momentum_breakout import momentum_breakout_signal
from core.trading_engine.short_simulation import simulate_short_trade
from datetime import datetime


def run_strategy(symbol: str, price_data: list[float], strategy: str) -> str | None:
    """
    Run a selected strategy on price data.
    Returns: "buy", "sell", or None
    """
    if strategy == "mean_reversion":
        return mean_reversion_signal(price_data)
    elif strategy == "momentum_breakout":
        return momentum_breakout_signal(price_data)
    else:
        return None


def simulate_long_trade(entry_price: float, capital: float = 1000.0):
    """
    Simulates a long position: buy low, sell high.
    For training/demo purposes only.
    """
    quantity = capital / entry_price
    return {
        "side": "long",
        "entry_price": entry_price,
        "quantity": round(quantity, 4),
        "status": "opened",
        "opened_at": datetime.utcnow()
    }


def simulate_trade(signal: str, current_price: float, capital: float = 1000.0):
    """
    Handles both long and short simulations.
    """
    if signal == "buy":
        return simulate_long_trade(current_price, capital)
    elif signal == "sell":
        # Simulate short (borrow + sell)
        return simulate_short_trade(entry_price=current_price, exit_price=current_price, capital=capital)
    return None
