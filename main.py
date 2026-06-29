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
pattern = detect_pattern(data)
data["Score"] = data.apply(
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
data["AI_Confidence"] = data["Score"].apply(confidence)
data["Signal"] = data["Score"].apply(generate_signal)

print("\nCandlestick Pattern :", pattern)

print(
    data[
        [
            "Close",
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
            "Signal"
        ]
    ].tail(10)
)
print("\n========== VOLUME ANALYSIS ==========\n")

print(f"Current Volume : {int(current_volume):,}")

print(f"20 Day Avg     : {int(avg_volume):,}")

print(f"Status         : {volume_status}")