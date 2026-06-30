def print_header():

    print("=" * 55)
    print("📈 BullEye AI v0.4 - AI Stock Analysis Platform")
    print("=" * 55)


def print_latest_analysis(
    stock,
    latest,
    pattern,
    weighted_score,
    final_ai_score
):

    print("\n========== LATEST MARKET ANALYSIS ==========\n")

    print(f"Stock            : {stock}")
    print(f"Close Price      : ₹{latest['Close']:.2f}")
    print(f"Trend            : {latest['Trend']}")
    print(f"Candlestick      : {pattern}")
    print(f"RSI              : {latest['RSI']:.2f}")
    print(f"EMA20            : ₹{latest['EMA20']:.2f}")
    print(f"MACD             : {latest['MACD']:.2f}")
    print(f"ATR              : {latest['ATR']:.2f}")

    print("-" * 35)

    print(f"AI Score         : {latest['Score']}/100")
    print(f"Weighted Score   : {weighted_score}/100")
    print(f"Smart AI Score   : {final_ai_score}/100")

    print("-" * 35)

    print(f"Confidence       : {latest['AI_Confidence']}")
    print(f"Signal           : {latest['Signal']}")
    print(f"Reasons          : {latest['Reasons']}")