import yfinance as yf


def passes_weekly_bb(symbol, tolerance=0.03):
    """
    Bullish Bollinger filter (WEEKLY)

    Pass when price is:
    - below middle band
    - near lower band
    - below lower band
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

    middle = close.rolling(20).mean()
    std = close.rolling(20).std()

    lower = middle - 2 * std

    last_close = float(close.iloc[-1])
    last_middle = float(middle.iloc[-1])
    last_lower = float(lower.iloc[-1])

    # ---------------------------------
    # ✅ NEW SMART BB CONDITIONS
    # ---------------------------------

    # 1️⃣ Between middle → lower (pullback zone)
    if last_close <= last_middle:
        return True

    # 2️⃣ Near lower band
    if last_close <= last_lower * (1 + tolerance):
        return True

    # 3️⃣ Breakdown below lower band
    if last_close < last_lower:
        return True

    return False
