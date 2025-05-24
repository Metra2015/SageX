# core/ai_engine.py

from sqlalchemy.orm import Session
from models.coin_ranking import CoinRanking
from datetime import datetime, timedelta

STRATEGIES = ["mean_reversion", "momentum_breakout"]

def choose_top_coins(db: Session, limit: int = 5):
    """
    Select top-ranked coins from last 30 minutes.
    """
    cutoff = datetime.utcnow() - timedelta(minutes=30)
    coins = db.query(CoinRanking).filter(
        CoinRanking.timestamp >= cutoff
    ).order_by(CoinRanking.rank.asc()).limit(limit).all()

    return [coin.symbol for coin in coins]


def evaluate_strategies(price_data: list[float]):
    """
    Selects the best strategy based on logic or later AI scoring.
    For now: try both and pick the one that gives a signal.
    """
    from core.trading_engine.mean_reversion import mean_reversion_signal
    from core.trading_engine.momentum_breakout import momentum_breakout_signal

    for strategy in STRATEGIES:
        if strategy == "mean_reversion":
            signal = mean_reversion_signal(price_data)
        elif strategy == "momentum_breakout":
            signal = momentum_breakout_signal(price_data)
        else:
            continue

        if signal:
            return strategy, signal

    return None, None


def get_trade_plan(db: Session, symbol: str, price_data: list[float]):
    """
    Final output: coin + strategy + signal.
    """
    strategy, signal = evaluate_strategies(price_data)

    if strategy and signal:
        return {
            "symbol": symbol.upper(),
            "strategy": strategy,
            "signal": signal
        }
    return None
