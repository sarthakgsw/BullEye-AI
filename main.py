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
from analysis.backtest import backtest
from indicators.atr import calculate_atr

print("📈 BullEye AI - RSI + EMA Module")

stock = input("Enter NSE Stock Symbol (e.g. RELIANCE.NS): ").strip().upper()

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
total, win, loss, rate = backtest(data)

print("\nCandlestick Pattern :", pattern)

print(
    data[
        [
            "Close",
            "ATR",
            "Support",
            "Resistance",
            "EMA20",
            "Trend",
            "RSI",
            "MACD",
            "MACD_Signal",
            "Histogram",
            "Score",
            "AI_Confidence",
            "Signal",
            "Reasons"
        ]
    ].tail(10)
)
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