# strategy.py
import pandas_ta as ta

def generate_signal(df):
    df["rsi"] = ta.rsi(df["Close"], length=14)
    df["ema"] = ta.ema(df["Close"], length=14)
    macd_df = ta.macd(df["Close"])
    df["macd"] = macd_df["MACD_12_26_9"]
    df["signal"] = macd_df["MACDs_12_26_9"]

    latest = df.iloc[-1]

    if latest["rsi"] < 30 and latest["Close"] > latest["ema"] and latest["macd"] > latest["signal"]:
        return "UP", "RSI Oversold + EMA Bullish + MACD Crossover"
    elif latest["rsi"] > 70 and latest["Close"] < latest["ema"] and latest["macd"] < latest["signal"]:
        return "DOWN", "RSI Overbought + EMA Bearish + MACD Crossdown"
    else:
        return None, None