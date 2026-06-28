def generate_signal(rsi, close, ema):
    if rsi < 30 and close > ema:
        return "🟢 BUY"

    elif rsi > 70 and close < ema:
        return "🔴 SELL"

    else:
        return "🟡 HOLD"