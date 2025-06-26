# confidence_core.py

def calculate_confidence(rsi, ema, macd, signal):
    confidence = 90.0
    if abs(rsi - 50) > 20:
        confidence += 3
    if abs(macd - signal) > 0.05:
        confidence += 3
    if rsi < 30 or rsi > 70:
        confidence += 3
    return min(confidence, 99.9)