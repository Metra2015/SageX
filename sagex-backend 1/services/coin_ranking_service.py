# services/coin_ranking_service.py

from sqlalchemy.orm import Session
from models.coin_ranking import CoinRanking
from schemas.coin_ranking import CoinRankCreate
from datetime import datetime


def add_coin_rank(db: Session, data: CoinRankCreate):
    rank_entry = CoinRanking(
        symbol=data.symbol.upper(),
        score=data.score,
        rank=data.rank,
        source=data.source
    )
    db.add(rank_entry)
    db.commit()
    db.refresh(rank_entry)
    return rank_entry


def get_top_coins(db: Session, limit: int = 10):
    return db.query(CoinRanking).order_by(
        CoinRanking.created_at.desc(), CoinRanking.rank.asc()
    ).limit(limit).all()


def get_coin_history(db: Session, symbol: str):
    return db.query(CoinRanking).filter(
        CoinRanking.symbol == symbol.upper()
    ).order_by(CoinRanking.created_at.desc()).all()
