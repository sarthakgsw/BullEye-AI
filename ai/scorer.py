def calculate_score(rsi, close, ema, macd, macd_signal):

    score = 0

    # RSI
    if rsi < 30:
        score += 30
    elif rsi < 50:
        score += 15

    # EMA
    if close > ema:
        score += 25

    # MACD
    if macd > macd_signal:
        score += 25

    # Trend
    if close > ema and macd > macd_signal:
        score += 20

    return score


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