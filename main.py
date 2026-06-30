import yfinance as yf

from indicators.rsi import calculate_rsi
from indicators.ema import calculate_ema
from indicators.macd import calculate_macd
from indicators.atr import calculate_atr
from indicators.trend import detect_trend
from indicators.candlestick import detect_pattern
from indicators.support_resistance import support_resistance

from strategies.signal import generate_signal

from ai.scorer import calculate_score, confidence
from ai.decision import ai_decision
from ai.indicator_summary import indicator_summary
from ai.weighted_analysis import weighted_analysis
from ai.smart_score import smart_score

from analysis.volume import volume_analysis
from analysis.risk import risk_management
from analysis.position_sizing import position_size
from analysis.backtest import backtest

from ui.display import print_header, print_latest_analysis


# ==========================================================
# HEADER
# ==========================================================

print_header()

stock = input("\nEnter NSE Stock Symbol (Default: RELIANCE.NS): ").strip().upper()

if not stock:
    stock = "RELIANCE.NS"

data = yf.download(stock, period="1y")

# Fix MultiIndex Columns
if hasattr(data.columns, "nlevels") and data.columns.nlevels > 1:
    data.columns = data.columns.get_level_values(0)

# ==========================================================
# INDICATORS
# ==========================================================

data["RSI"] = calculate_rsi(data)

data["EMA20"] = calculate_ema(data)

data["ATR"] = calculate_atr(data)

data["Trend"] = data.apply(
    lambda row: detect_trend(
        row["Close"],
        row["EMA20"]
    ),
    axis=1
)

data["MACD"], data["MACD_Signal"], data["Histogram"] = calculate_macd(data)

pattern = detect_pattern(data)

current_volume, avg_volume, volume_status = volume_analysis(data)

data["Support"], data["Resistance"] = support_resistance(data)

# ==========================================================
# RISK MANAGEMENT
# ==========================================================

entry, stop_loss, target1, target2, rr = risk_management(
    data["Close"].iloc[-1],
    data["Support"].iloc[-1],
    data["Resistance"].iloc[-1]
)

# ==========================================================
# POSITION SIZING
# ==========================================================

capital = 100000
risk_percent = 2

qty, investment, max_risk, risk_per_share = position_size(
    capital,
    risk_percent,
    entry,
    stop_loss
)

# ==========================================================
# AI SCORE
# ==========================================================

scores = data.apply(
    lambda row: calculate_score(
        row["RSI"],
        row["Close"],
        row["EMA20"],
        row["MACD"],
        row["MACD_Signal"],
        volume_status
    ),
    axis=1
)

data["Score"] = scores.apply(lambda x: x[0])

data["Reasons"] = scores.apply(lambda x: ", ".join(x[1]))

data["AI_Confidence"] = data["Score"].apply(confidence)

data["Signal"] = data["Score"].apply(generate_signal)

# ==========================================================
# WEIGHTED ANALYSIS
# ==========================================================

weighted_score = weighted_analysis(
    data["RSI"].iloc[-1],
    data["Close"].iloc[-1],
    data["EMA20"].iloc[-1],
    data["MACD"].iloc[-1],
    data["MACD_Signal"].iloc[-1],
    data["Trend"].iloc[-1],
    volume_status,
    pattern
)

# ==========================================================
# SMART AI SCORE
# ==========================================================

final_ai_score = smart_score(
    data["Score"].iloc[-1],
    weighted_score
)

# ==========================================================
# AI DECISION
# ==========================================================

verdict, strength, recommendation = ai_decision(
    final_ai_score,
    data["Trend"].iloc[-1],
    volume_status,
    data["ATR"].iloc[-1]
)

# ==========================================================
# INDICATOR SUMMARY
# ==========================================================

summary, bullish, bearish, neutral, bias = indicator_summary(
    data["RSI"].iloc[-1],
    data["Close"].iloc[-1],
    data["EMA20"].iloc[-1],
    data["MACD"].iloc[-1],
    data["MACD_Signal"].iloc[-1],
    data["Trend"].iloc[-1],
    volume_status,
    pattern,
    data["ATR"].iloc[-1]
)

# ==========================================================
# BACKTEST
# ==========================================================

total, win, loss, rate = backtest(data)

latest = data.iloc[-1]
# ==========================================================
# LATEST MARKET ANALYSIS
# ==========================================================

print_latest_analysis(
    stock,
    latest,
    pattern,
    weighted_score,
    final_ai_score
)

# ==========================================================
# VOLUME ANALYSIS
# ==========================================================

print("\n========== VOLUME ANALYSIS ==========\n")

print(f"Current Volume : {int(current_volume):,}")
print(f"20 Day Avg     : {int(avg_volume):,}")
print(f"Status         : {volume_status}")

# ==========================================================
# RISK MANAGEMENT
# ==========================================================

print("\n========== RISK MANAGEMENT ==========\n")

print(f"Entry Price : ₹{entry:.2f}")
print(f"Stop Loss   : ₹{stop_loss:.2f}")
print(f"Target 1    : ₹{target1:.2f}")
print(f"Target 2    : ₹{target2:.2f}")
print(f"Risk/Reward : 1 : {rr}")

# ==========================================================
# BACKTEST
# ==========================================================

print("\n========== BACKTEST ==========\n")

print(f"Total Trades   : {total}")
print(f"Winning Trades : {win}")
print(f"Losing Trades  : {loss}")
print(f"Win Rate       : {rate}%")

# ==========================================================
# AI DECISION
# ==========================================================

print("\n========== AI DECISION ==========\n")

print(f"Final Verdict : {verdict}")
print(f"Strength      : {strength}")

print("\nTrade Plan")
print("-" * 35)

print(f"Entry Price : ₹{entry:.2f}")
print(f"Stop Loss   : ₹{stop_loss:.2f}")
print(f"Target 1    : ₹{target1:.2f}")
print(f"Target 2    : ₹{target2:.2f}")

print("\nRecommendation")
print("-" * 35)

for line in recommendation.split("\n"):
    print(f"• {line}")

overall_rating = round(final_ai_score / 10, 1)

print(f"\nOverall Rating : {overall_rating} / 10")

# ==========================================================
# INDICATOR SUMMARY
# ==========================================================

print("\n========== INDICATOR SUMMARY ==========\n")

for name, status in summary.items():
    print(f"{name:<15}: {status}")

print()

print(f"Bullish Indicators : {bullish}")
print(f"Bearish Indicators : {bearish}")
print(f"Neutral Indicators : {neutral}")

print(f"\nMarket Bias : {bias}")

# ==========================================================
# POSITION SIZING
# ==========================================================

print("\n========== POSITION SIZING ==========\n")

print(f"Capital            : ₹{capital:,.0f}")
print(f"Risk Per Trade     : {risk_percent}%")
print(f"Maximum Risk       : ₹{max_risk:,.2f}")
print(f"Risk Per Share     : ₹{risk_per_share:.2f}")
print(f"Recommended Qty    : {qty} Shares")
print(f"Investment Needed  : ₹{investment:,.2f}")

print("\n=======================================================")
print("✅ Analysis Completed Successfully")
print("Thank you for using BullEye AI")
print("=======================================================")