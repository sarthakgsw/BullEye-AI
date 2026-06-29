def detect_trend(close, ema):

    if close > ema * 1.02:
        return "🟢 Strong Uptrend"

    elif close > ema:
        return "🟢 Uptrend"

    elif close < ema * 0.98:
        return "🔴 Strong Downtrend"

    elif close < ema:
        return "🔴 Downtrend"

    else:
        return "🟡 Sideways"