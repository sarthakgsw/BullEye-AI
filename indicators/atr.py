def calculate_atr(data, period=14):

    high_low = data["High"] - data["Low"]

    high_close = abs(data["High"] - data["Close"].shift())

    low_close = abs(data["Low"] - data["Close"].shift())

    tr = high_low.combine(high_close, max)

    tr = tr.combine(low_close, max)

    atr = tr.rolling(period).mean()

    return atr