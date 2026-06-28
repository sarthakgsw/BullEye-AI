def generate_signal(score):

    if score >= 85:
        return "🟢 STRONG BUY"

    elif score >= 70:
        return "🟢 BUY"

    elif score >= 50:
        return "🟡 HOLD"

    elif score >= 30:
        return "🟠 WEAK"

    else:
        return "🔴 SELL"