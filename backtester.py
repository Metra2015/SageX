# backtester.py

from sqlalchemy.orm import Session
from core.database import SessionLocal
from models.historical_data import HistoricalData
from core.trading_engine.mean_reversion import mean_reversion_signal
from core.trading_engine.momentum_breakout import momentum_breakout_signal

STRATEGIES = {
    "mean_reversion": mean_reversion_signal,
    "momentum_breakout": momentum_breakout_signal
}

def get_candle_series(db: Session, symbol: str, timeframe: str = "1m", limit: int = 500):
    candles = db.query(HistoricalData).filter(
        HistoricalData.symbol == symbol.upper(),
        HistoricalData.timeframe == timeframe
    ).order_by(HistoricalData.timestamp.asc()).limit(limit).all()

    return [c.close for c in candles]


def backtest(symbol: str, strategy_name: str, window: int = 30, capital: float = 1000.0):
    db: Session = SessionLocal()
    try:
        prices = get_candle_series(db, symbol)
        strategy = STRATEGIES.get(strategy_name)
        if not strategy:
            print(f"❌ Unknown strategy: {strategy_name}")
            return

        wins = 0
        losses = 0
        total_pnl = 0.0
        trades = 0

        for i in range(window, len(prices) - 1):
            window_data = prices[i - window:i]
            signal = strategy(window_data)
            if signal:
                entry = prices[i]
                exit_ = prices[i + 1]
                qty = capital / entry
                pnl = (exit_ - entry) * qty
                if signal == "sell":
                    pnl *= -1  # invert for short

                trades += 1
                total_pnl += pnl
                if pnl > 0:
                    wins += 1
                else:
                    losses += 1

        if trades == 0:
            print("⚠️ No signals generated.")
            return

        print(f"\n📊 Backtest Summary for {symbol} | Strategy: {strategy_name}")
        print(f"Trades: {trades}")
        print(f"Wins: {wins} | Losses: {losses}")
        print(f"Win Rate: {round((wins / trades) * 100, 2)}%")
        print(f"Total P&L: ${round(total_pnl, 2)}")

    finally:
        db.close()


if __name__ == "__main__":
    backtest(symbol="BTCUSDT", strategy_name="mean_reversion", window=30)
