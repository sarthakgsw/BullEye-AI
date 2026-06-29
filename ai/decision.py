def ai_decision(score, trend, volume_status, atr):
    """
    BullEye AI - Final Decision Engine
    """

    # Final Verdict
    if score >= 85 and trend == "🟢 Uptrend":
        verdict = "🟢 STRONG BUY"
        strength = "★★★★★"
        recommendation = (
            "Excellent bullish setup.\n"
            "Price is above EMA20 with strong momentum.\n"
            "Fresh buying can be considered."
        )

    elif score >= 70 and trend == "🟢 Uptrend":
        verdict = "🟢 BUY"
        strength = "★★★★☆"
        recommendation = (
            "Bullish trend is active.\n"
            "Buying opportunity is available."
        )

    elif score >= 50:
        verdict = "🟡 HOLD"
        strength = "★★★☆☆"
        recommendation = (
            "Wait for better confirmation.\n"
            "Avoid aggressive entries."
        )

    elif score >= 30:
        verdict = "🟠 WEAK"
        strength = "★★☆☆☆"
        recommendation = (
            "Market momentum is weak.\n"
            "Avoid fresh buying."
        )

    else:
        verdict = "🔴 SELL"
        strength = "★☆☆☆☆"
        recommendation = (
            "Bearish setup detected.\n"
            "Selling or staying away is recommended."
        )

    # Volume Analysis
    if volume_status == "🟢 High Volume Breakout":
        recommendation += "\n✅ High Volume supports the move."

    elif volume_status == "🟡 Normal Volume":
        recommendation += "\n🟡 Volume is normal."

    else:
        recommendation += "\n⚠️ Weak volume reduces confidence."

    # ATR Analysis
    if atr > 50:
        recommendation += "\n⚠️ High volatility detected."

    else:
        recommendation += "\n✅ Volatility is under control."

    return verdict, strength, recommendation