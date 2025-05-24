# services/knowledge_enhancer.py

from sqlalchemy.orm import Session
from models.trade_log import TradeLog
from collections import defaultdict


def analyze_strategy_performance(db: Session, user_id: int = 1):
    """
    Analyze past trades by symbol + strategy.
    Return: dict of { (symbol, strategy): { win_rate, avg_pnl, count } }
    """
    trades = db.query(TradeLog).filter(TradeLog.user_id == user_id).all()

    stats = defaultdict(lambda: {"wins": 0, "losses": 0, "pnl": 0.0, "count": 0})

    for t in trades:
        key = (t.symbol, t.strategy)
        stats[key]["count"] += 1
        stats[key]["pnl"] += t.profit_loss
        if t.profit_loss > 0:
            stats[key]["wins"] += 1
        else:
            stats[key]["losses"] += 1

    results = {}
    for key, val in stats.items():
        win_rate = (val["wins"] / val["count"]) * 100
        avg_pnl = val["pnl"] / val["count"]
        results[key] = {
            "win_rate": round(win_rate, 2),
            "avg_pnl": round(avg_pnl, 2),
            "count": val["count"]
        }

    return results


def get_best_strategy_for_symbol(performance: dict, symbol: str, min_trades: int = 5):
    """
    Returns the best strategy for a given symbol based on win rate.
    """
    best = None
    best_score = -1

    for (sym, strat), data in performance.items():
        if sym == symbol and data["count"] >= min_trades:
            if data["win_rate"] > best_score:
                best = strat
                best_score = data["win_rate"]

    return best
