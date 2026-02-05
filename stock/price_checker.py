import yfinance as yf

def get_price(symbol):
    if not symbol.endswith(".NS"):
        symbol += ".NS"

    data = yf.Ticker(symbol).history(period="1d", interval="1m")

    if data.empty:
        return None

    return float(data["Close"].iloc[-1])
