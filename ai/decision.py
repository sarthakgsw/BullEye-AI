def ai_report(score, reasons):

    print("\n========== AI REPORT ==========\n")

    print(f"AI Score : {score}/100")

    if score >= 85:
        print("Recommendation : 🟢 STRONG BUY")

    elif score >= 70:
        print("Recommendation : 🟢 BUY")

    elif score >= 50:
        print("Recommendation : 🟡 HOLD")

    elif score >= 30:
        print("Recommendation : 🟠 WAIT")

    else:
        print("Recommendation : 🔴 SELL")

    print("\nReasons :")

    for reason in reasons:
        print("✅", reason)