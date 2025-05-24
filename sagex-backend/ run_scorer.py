# run_scorer.py

from sqlalchemy.orm import Session
from core.database import SessionLocal
from services.scoring_service import score_and_rank_coins

# Define which coins to rank
SYMBOLS = ["BTCUSDT", "ETHUSDT", "XRPUSDT", "SOLUSDT", "ADAUSDT", "LTCUSDT"]
TIMEFRAME = "1m"
WINDOW = 30  # last 30 candles

def run():
    db: Session = SessionLocal()
    try:
        results = score_and_rank_coins(SYMBOLS, db, timeframe=TIMEFRAME, window=WINDOW)
        print("\n🏆 Top Ranked Coins:")
        for r in results:
            print(f"→ {r['symbol']}: {r['score']}%")
    finally:
        db.close()

if __name__ == "__main__":
    run()
