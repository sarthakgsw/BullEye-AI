def detect_pattern(data):

    latest = data.iloc[-1]

    open_price = latest["Open"]
    close_price = latest["Close"]
    high_price = latest["High"]
    low_price = latest["Low"]

    body = abs(close_price - open_price)
    upper_shadow = high_price - max(open_price, close_price)
    lower_shadow = min(open_price, close_price) - low_price

    # Doji
    if body <= (high_price - low_price) * 0.1:
        return "⚪ Doji"

    # Hammer
    elif lower_shadow > body * 2 and upper_shadow < body:
        return "🟢 Hammer"

    # Shooting Star
    elif upper_shadow > body * 2 and lower_shadow < body:
        return "🔴 Shooting Star"

    # Bullish Candle
    elif close_price > open_price:
        return "🟢 Bullish Candle"

    # Bearish Candle
    else:
        return "🔴 Bearish Candle"