def support_resistance(data):

    support = data["Low"].rolling(window=20).min()

    resistance = data["High"].rolling(window=20).max()

    return support, resistance