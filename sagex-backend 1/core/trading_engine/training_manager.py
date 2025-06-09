# core/trading_engine/training_manager.py

from datetime import datetime, timedelta


class TrainingEvaluator:
    def __init__(self, start_balance: float, target_balance: float, start_time: datetime, duration_days: int = 30):
        self.start_balance = start_balance
        self.target_balance = target_balance
        self.start_time = start_time
        self.duration_days = duration_days

    def evaluate(self, current_balance: float, now: datetime = None):
        now = now or datetime.utcnow()
        deadline = self.start_time + timedelta(days=self.duration_days)

        result = {
            "status": "in_progress",
            "success": None,
            "expired": False
        }

        if now >= deadline:
            result["expired"] = True
            if current_balance >= self.target_balance:
                result["status"] = "success"
                result["success"] = True
            else:
                result["status"] = "failed"
                result["success"] = False
        else:
            if current_balance >= self.target_balance:
                result["status"] = "success"
                result["success"] = True

        return result
