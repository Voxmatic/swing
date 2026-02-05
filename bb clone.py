import yfinance as yf


def passes_weekly_bb(symbol, tolerance=0.005):
    """
    Bullish Bollinger filter:
    Only LOWER band proximity is valid
    """

    try:
        df = yf.download(
            symbol + ".NS",
            interval="1wk",
            period="2y",
            progress=False,
            auto_adjust=False
        )
    except Exception:
        return False

    if df is None or df.empty or len(df) < 25:
        return False

    close = df["Close"].squeeze()

    ma = close.rolling(20).mean()
    std = close.rolling(20).std()

    lower = ma - 2 * std

    last_close = float(close.iloc[-1])
    last_lower = float(lower.iloc[-1])

    return last_close <= last_lower * (1 + tolerance)
