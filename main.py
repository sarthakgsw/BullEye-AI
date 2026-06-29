import yfinance as yf
from indicators.rsi import calculate_rsi
from indicators.ema import calculate_ema
from indicators.macd import calculate_macd
from strategies.signal import generate_signal
from ai.scorer import calculate_score, confidence
from indicators.candlestick import detect_pattern
from indicators.trend import detect_trend
from indicators.support_resistance import support_resistance
from analysis.volume import volume_analysis
from analysis.risk import risk_management
from analysis.position_sizing import position_size
from analysis.backtest import backtest
from indicators.atr import calculate_atr
from ai.decision import ai_decision

print("=" * 55)
print("📈 BullEye AI v0.3 - AI Stock Analysis Platform")
print("=" * 55)

stock = input("\nEnter NSE Stock Symbol (Default: RELIANCE.NS): ").strip().upper()

if not stock:
    stock = "RELIANCE.NS"

data = yf.download(stock, period="1y")

# MultiIndex columns હોય તો સરળ બનાવો
if hasattr(data.columns, "nlevels") and data.columns.nlevels > 1:
    data.columns = data.columns.get_level_values(0)

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
current_volume, avg_volume, volume_status = volume_analysis(data)
data["Support"], data["Resistance"] = support_resistance(data)
entry, stop_loss, target1, target2, rr = risk_management(
    data["Close"].iloc[-1],
    data["Support"].iloc[-1],
    data["Resistance"].iloc[-1]
)
capital = 100000      # Total Capital
risk_percent = 2      # Risk per Trade

qty, investment, max_risk, risk_per_share = position_size(
    capital,
    risk_percent,
    entry,
    stop_loss
)
pattern = detect_pattern(data)
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
# Final AI Decision
verdict, strength, recommendation = ai_decision(
    data["Score"].iloc[-1],
    data["Trend"].iloc[-1],
    volume_status,
    data["ATR"].iloc[-1]
)
total, win, loss, rate = backtest(data)


print("\n========== LATEST MARKET ANALYSIS ==========\n")

latest = data.iloc[-1]

print(f"Stock            : {stock}")
print(f"Close Price      : ₹{latest['Close']:.2f}")
print(f"Trend            : {latest['Trend']}")
print(f"Candlestick      : {pattern}")
print(f"RSI              : {latest['RSI']:.2f}")
print(f"EMA20            : ₹{latest['EMA20']:.2f}")
print(f"MACD             : {latest['MACD']:.2f}")
print(f"ATR              : {latest['ATR']:.2f}")
print(f"AI Score         : {latest['Score']}/100")
print(f"Confidence       : {latest['AI_Confidence']}")
print(f"Signal           : {latest['Signal']}")
print(f"Reasons          : {latest['Reasons']}")
print("\n========== VOLUME ANALYSIS ==========\n")

print(f"Current Volume : {int(current_volume):,}")

print(f"20 Day Avg     : {int(avg_volume):,}")

print(f"Status         : {volume_status}")
print("\n========== RISK MANAGEMENT ==========\n")

print(f"Entry Price : ₹{entry:.2f}")

print(f"Stop Loss  : ₹{stop_loss:.2f}")

print(f"Target 1   : ₹{target1:.2f}")

print(f"Target 2   : ₹{target2:.2f}")

print(f"Risk/Reward: 1 : {rr}")
print("\n========== BACKTEST ==========\n")

print(f"Total Trades   : {total}")

print(f"Winning Trades : {win}")

print(f"Losing Trades  : {loss}")

print(f"Win Rate       : {rate}%")
print("\n========== AI DECISION ==========\n")

print(f"Final Verdict : {verdict}")
print(f"Strength      : {strength}")

print("\nTrade Plan")
print("-" * 35)
print(f"Entry Price : ₹{entry:.2f}")
print(f"Stop Loss  : ₹{stop_loss:.2f}")
print(f"Target 1   : ₹{target1:.2f}")
print(f"Target 2   : ₹{target2:.2f}")

print("\nRecommendation")
print("-" * 35)

for line in recommendation.split("\n"):
    print(f"• {line}")

overall_rating = round(data["Score"].iloc[-1] / 10, 1)

print(f"\nOverall Rating : {overall_rating} / 10")
print("\n========== POSITION SIZING ==========\n")

print(f"Capital           : ₹{capital:,.0f}")
print(f"Risk Per Trade    : {risk_percent}%")
print(f"Maximum Risk      : ₹{max_risk:,.2f}")
print(f"Risk Per Share    : ₹{risk_per_share:.2f}")
print(f"Recommended Qty   : {qty} Shares")
print(f"Investment Needed : ₹{investment:,.2f}")