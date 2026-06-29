def volume_analysis(data):

    current_volume = data["Volume"].iloc[-1]

    avg_volume = data["Volume"].rolling(20).mean().iloc[-1]

    if current_volume > avg_volume * 1.5:
        status = "🟢 High Volume Breakout"

    elif current_volume < avg_volume * 0.7:
        status = "🔴 Weak Volume"

    else:
        status = "🟡 Normal Volume"

    return current_volume, avg_volume, status