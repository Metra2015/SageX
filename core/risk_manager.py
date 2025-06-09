# core/risk_manager.py

from decimal import Decimal


def check_capital_limit(current_allocated: float, max_capital: float) -> bool:
    """
    Ensure current allocation does not exceed max allowed capital.
    """
    return current_allocated <= max_capital


def check_loss_limit(potential_loss: float, max_loss: float) -> bool:
    """
    Ensure risk on this trade is within acceptable bounds.
    """
    return potential_loss <= max_loss


def should_trade(current_allocated: float, max_capital: float, potential_loss: float, max_loss: float) -> bool:
    """
    Combines capital and risk checks.
    Returns True if trade is allowed.
    """
    capital_ok = check_capital_limit(current_allocated, max_capital)
    risk_ok = check_loss_limit(potential_loss, max_loss)
    return capital_ok and risk_ok


def estimate_loss(entry_price: float, stop_price: float, capital: float) -> float:
    """
    Rough estimate of potential loss for stop-loss based risk control.
    """
    if stop_price >= entry_price:
        return 0.0

    qty = Decimal(capital) / Decimal(entry_price)
    loss = (Decimal(entry_price) - Decimal(stop_price)) * qty
    return float(loss)
