from tvDatafeed import TvDatafeed, Interval

tv = TvDatafeed()

def get_price(symbol):
    data = tv.get_hist(symbol, "NSE", Interval.in_1_minute, n_bars=1)
    return float(data['close'].iloc[-1])
