# core/trading_engine/demo_manager.py

from core.trading_engine.manager import run_strategy, simulate_trade
from datetime import datetime


class DemoTrader:
    def __init__(self, user_id: int, symbol: str, strategy: str, price_data: list[float], capital: float = 1000.0):
        self.user_id = user_id
        self.symbol = symbol
        self.strategy = strategy
        self.price_data = price_data
        self.capital = capital
        self.trade_log = []

    def execute(self):
        signal = run_strategy(self.symbol, self.price_data, self.strategy)

        if signal:
            entry_price = self.price_data[-1]
            simulated = simulate_trade(signal, entry_price, self.capital)

            trade = {
                "user_id": self.user_id,
                "symbol": self.symbol,
                "side": simulated["side"],
                "entry_price": simulated["entry_price"],
                "quantity": simulated["quantity"],
                "is_demo": True,
                "is_closed": True,
                "profit_loss": simulated.get("profit_loss", 0.0),
                "opened_at": simulated.get("opened_at", datetime.utcnow()),
                "closed_at": simulated.get("closed_at", datetime.utcnow()),
                "note": simulated.get("logic", "Simulated trade")
            }

            self.trade_log.append(trade)
            return trade

        return None

    def get_log(self):
        return self.trade_log
