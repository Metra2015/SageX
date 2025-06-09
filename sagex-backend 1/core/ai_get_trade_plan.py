
# core/ai_get_trade_plan.py
import os
import joblib
import random

model_path = "models/trade_classifier.pkl"

def get_trade_plan(db, symbol, price_data):
    last_price = price_data[-1]

    # Dummy strategy
    signal = random.choice(["BUY", "SELL"])
    strategy = "ai_model"

    # If model exists, use it
    if os.path.exists(model_path):
        model = joblib.load(model_path)
        features = [[last_price]]  # Replace with full feature vector
        prob = model.predict_proba(features)[0][1]
        if prob < 0.7:
            return None  # Skip low-confidence trades

    return {
        "symbol": symbol,
        "signal": signal,
        "strategy": strategy
    }
