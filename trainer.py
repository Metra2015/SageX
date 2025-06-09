
# trainer.py
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
import os

log_path = "logs/trade_results.csv"
model_path = "models/trade_classifier.pkl"

if not os.path.exists(log_path):
    raise FileNotFoundError("No trade_results.csv found. Run some trades first.")

df = pd.read_csv(log_path)

# Feature engineering placeholder (you can expand this)
df = df.dropna()
df["label"] = (df["pnl"] > 0).astype(int)
X = df[["price"]]  # Later: add more indicators/features
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

joblib.dump(model, model_path)
print(f"✅ Model trained and saved to {model_path}")
