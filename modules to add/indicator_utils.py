import pandas as pd

def add_indicators(df):
    df["ma_10"] = df["price"].rolling(window=10).mean()
    df["rsi"] = compute_rsi(df["price"])
    return df.dropna()

def compute_rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))
