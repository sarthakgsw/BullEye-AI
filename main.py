print("Welcome to BullEye AI 🚀")
print("Indian Stock Market AI Assistant")
print("Developer: Sarthak Goswami")
import yfinance as yf

print("📈 BullEye AI - Market Data Module")

# NSE Stock Symbol
stock = "RELIANCE.NS"

# છેલ્લા 1 વર્ષનો data download કરો
data = yf.download(stock, period="1y")

print("\nFirst 5 Rows:\n")
print(data.head())

print("\nLast 5 Rows:\n")
print(data.tail())