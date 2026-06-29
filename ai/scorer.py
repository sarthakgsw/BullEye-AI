def calculate_score(rsi, close, ema, macd, macd_signal, volume_status):

    score = 0
    reasons = []

    # RSI
    if rsi < 30:
        score += 30
        reasons.append("RSI Oversold")
    elif rsi < 50:
        score += 15
        reasons.append("RSI Neutral")

    # EMA
    if close > ema:
        score += 25
        reasons.append("Above EMA20")

    # MACD
    if macd > macd_signal:
        score += 25
        reasons.append("MACD Bullish")

    # Trend
    if close > ema and macd > macd_signal:
        score += 20
        reasons.append("Strong Uptrend")

    # Volume
    if volume_status == "🟢 High Volume Breakout":
        score += 15
        reasons.append("High Volume")

    elif volume_status == "🟡 Normal Volume":
        score += 5
        reasons.append("Normal Volume")

    elif volume_status == "🔴 Weak Volume":
        score -= 10
        reasons.append("Weak Volume")

    return score, reasons


def confidence(score):

    if score >= 85:
        return "🟢 STRONG BUY (95%)"

    elif score >= 70:
        return "🟢 BUY (80%)"

    elif score >= 50:
        return "🟡 HOLD (60%)"

    elif score >= 30:
        return "🟠 WEAK (40%)"

    else:
        return "🔴 SELL (20%)"