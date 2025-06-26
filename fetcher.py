# fetcher.py
import requests
import pandas as pd

def fetch_candles(symbol="EURUSD", interval="1m", limit=30):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}USDT&interval={interval}&limit={limit}"
    r = requests.get(url)
    raw = r.json()
    df = pd.DataFrame(raw, columns=["t", "o", "h", "l", "c", "v", "_", "__", "___", "____", "_____"])
    df["Open"] = df["o"].astype(float)
    df["High"] = df["h"].astype(float)
    df["Low"] = df["l"].astype(float)
    df["Close"] = df["c"].astype(float)
    return df[["Open", "High", "Low", "Close"]]