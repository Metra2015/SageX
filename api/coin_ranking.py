from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from services.coin_ranking_service import get_top_ranked_coins
from core.database import get_db  # Make sure this path is correct

router = APIRouter()

@router.get("/top")
def get_top_coins(
    limit: int = Query(10, description="Number of top coins to return"),
    db: Session = Depends(get_db)
):
    """
    Returns the top-ranked coins based on the latest scoring.
    """
    return get_top_ranked_coins(db, limit)
