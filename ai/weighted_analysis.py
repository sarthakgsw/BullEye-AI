def weighted_analysis(
    rsi,
    close,
    ema20,
    macd,
    macd_signal,
    trend,
    volume_status,
    pattern
):
    score = 0

    # Trend (30)
    if "Uptrend" in trend:
        score += 30

    # MACD (25)
    if macd > macd_signal:
        score += 25

    # EMA (20)
    if close > ema20:
        score += 20

    # RSI (15)
    if rsi < 30:
        score += 15
    elif rsi < 50:
        score += 8

    # Volume (5)
    if "High" in volume_status:
        score += 5

    # Candlestick (5)
    if "Bullish" in pattern:
        score += 5

    return score