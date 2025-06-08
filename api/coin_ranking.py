from fastapi import APIRouter, Query
from services.coin_ranking_service import get_top_ranked_coins

router = APIRouter()

@router.get("/top")
def get_top_coins(limit: int = Query(10, description="Number of top coins to return")):
    """
    Returns the top-ranked coins based on the latest scoring.
    """
    return get_top_ranked_coins(limit)
