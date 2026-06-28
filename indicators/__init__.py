import yfinance as yf
from indicators.rsi import calculate_rsi

print("📈 BullEye AI - RSI Module")

stock = "RELIANCE.NS"

data = yf.download(stock, period="1y")

# જો MultiIndex columns આવે તો સરળ બનાવો
if hasattr(data.columns, "nlevels") and data.columns.nlevels > 1:
    data.columns = data.columns.get_level_values(0)

data["RSI"] = calculate_rsi(data)

print(data[["Close", "RSI"]].tail(10))