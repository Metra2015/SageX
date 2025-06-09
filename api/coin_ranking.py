from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from core.database import SessionLocal
from services.historical_data_service import get_candles
import joblib
import os

router = APIRouter()

MODEL_PATH = "models/trade_classifier.pkl"
SYMBOLS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "AVAXUSDT", "LINKUSDT"]  # Add or change as needed

@router.get("/", summary="Get top-ranked coins by AI model")
def get_top_ranked_coins():
    if not os.path.exists(MODEL_PATH):
        raise HTTPException(status_code=500, detail="AI model not trained")

    model = joblib.load(MODEL_PATH)
    db: Session = SessionLocal()

    rankings = []
    for symbol in SYMBOLS:
        candles = get_candles(db, symbol, limit=30)
        if not candles:
            continue

        prices = [c.close for c in candles]
        last_price = prices[-1]
        # TODO: Replace with real feature vector
        features = [[last_price]]
        try:
            score = model.predict_proba(features)[0][1]  # Confidence score
            rankings.append({"symbol": symbol, "score": round(score * 100, 2)})
        except Exception as e:
            print(f"⚠️ Model failed on {symbol}: {e}")
            continue

    db.close()
    # Sort descending by confidence
    return sorted(rankings, key=lambda x: x["score"], reverse=True)
