def indicator_summary(
    rsi,
    close,
    ema20,
    macd,
    macd_signal,
    trend,
    volume_status,
    pattern,
    atr
):
    bullish = 0
    bearish = 0
    neutral = 0

    summary = {}

    # RSI
    if rsi < 30:
        summary["RSI"] = "🟢 Oversold"
        bullish += 1
    elif rsi > 70:
        summary["RSI"] = "🔴 Overbought"
        bearish += 1
    else:
        summary["RSI"] = "🟡 Neutral"
        neutral += 1

    # EMA20
    if close > ema20:
        summary["EMA20"] = "🟢 Bullish"
        bullish += 1
    else:
        summary["EMA20"] = "🔴 Bearish"
        bearish += 1

    # MACD
    if macd > macd_signal:
        summary["MACD"] = "🟢 Bullish"
        bullish += 1
    else:
        summary["MACD"] = "🔴 Bearish"
        bearish += 1

    # Trend
    summary["Trend"] = trend

    if "Uptrend" in trend:
        bullish += 1
    else:
        bearish += 1

    # Volume
    summary["Volume"] = volume_status

    if "High" in volume_status:
        bullish += 1
    elif "Weak" in volume_status:
        bearish += 1
    else:
        neutral += 1

    # ATR
    if atr > 50:
        summary["ATR"] = "🔴 High Volatility"
        bearish += 1
    else:
        summary["ATR"] = "🟢 Low Volatility"
        bullish += 1

    # Candlestick
    summary["Candlestick"] = pattern

    if "Bullish" in pattern:
        bullish += 1
    elif "Bearish" in pattern:
        bearish += 1
    else:
        neutral += 1

    # Final Market Bias
    if bullish > bearish:
        bias = "🟢 Bullish"
    elif bearish > bullish:
        bias = "🔴 Bearish"
    else:
        bias = "🟡 Neutral"

    return summary, bullish, bearish, neutral, bias