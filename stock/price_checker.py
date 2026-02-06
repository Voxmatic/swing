from tvDatafeed import TvDatafeed, Interval

tv = TvDatafeed()   # anonymous login works fine

def get_price(symbol):
    try:
        # NSE symbols on TradingView use NSE:
        data = tv.get_hist(
            symbol=symbol,
            exchange="NSE",
            interval=Interval.in_1_minute,
            n_bars=1
        )

        if data is None or data.empty:
            return None

        return float(data["close"].iloc[-1])

    except Exception as e:
        return None
