# services/scoring_service.py

from sqlalchemy.orm import Session
from models.historical_data import HistoricalData
from models.coin_ranking import CoinRanking
from datetime import datetime, timedelta


def score_coin(symbol: str, db: Session, timeframe: str = "1m", window: int = 30):
    """
    Calculates a momentum score for a given symbol.
    Score = % price change over last `window` candles.
    """
    candles = db.query(HistoricalData).filter(
        HistoricalData.symbol == symbol.upper(),
        HistoricalData.timeframe == timeframe
    ).order_by(HistoricalData.timestamp.desc()).limit(window).all()

    if len(candles) < 2:
        return None

    candles = list(reversed(candles))  # Oldest first
    first = candles[0].close
    last = candles[-1].close

    if first == 0:
        return None

    pct_change = ((last - first) / first) * 100
    return round(pct_change, 2)


def score_and_rank_coins(symbols: list[str], db: Session, timeframe: str = "1m", window: int = 30):
    scored = []
    for symbol in symbols:
        score = score_coin(symbol, db, timeframe, window)
        if score is not None:
            scored.append({"symbol": symbol, "score": score})

    # Sort descending
    scored.sort(key=lambda x: x["score"], reverse=True)

    for rank, entry in enumerate(scored, start=1):
        coin = CoinRanking(
            symbol=entry["symbol"].upper(),
            score=entry["score"],
            rank=rank,
            source="scoring_service"
        )
        db.add(coin)

    db.commit()
    return scored
