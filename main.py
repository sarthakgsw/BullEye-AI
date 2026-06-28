import yfinance as yf
from indicators.rsi import calculate_rsi
from indicators.ema import calculate_ema
from indicators.macd import calculate_macd
from strategies.signal import generate_signal

print("📈 BullEye AI - RSI + EMA Module")

stock = "RELIANCE.NS"

data = yf.download(stock, period="1y")

# MultiIndex columns હોય તો સરળ બનાવો
if hasattr(data.columns, "nlevels") and data.columns.nlevels > 1:
    data.columns = data.columns.get_level_values(0)

data["RSI"] = calculate_rsi(data)
data["EMA20"] = calculate_ema(data)
data["MACD"], data["MACD_Signal"], data["Histogram"] = calculate_macd(data)
data["Signal"] = data.apply(
    lambda row: generate_signal(
        row["RSI"],
        row["Close"],
        row["EMA20"]
    ),
    axis=1
)

print(
    data[
        [
            "Close",
            "EMA20",
            "RSI",
            "MACD",
            "MACD_Signal",
            "Histogram",
            "Signal"
        ]
    ].tail(10)
)