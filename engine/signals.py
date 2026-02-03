def compute_price_signal(state, lookback=15):
    if len(state.TP_dir) < lookback:
        return 0
    return all(d == 1 for d in state.TP_dir[-lookback:])

def compute_time_signal(state, lookback=15):
    if len(state.ML) < lookback:
        return 0
    return all(state.ML[i] > state.ML[i-1] for i in range(-lookback+1, 0))

def compute_bias_signal(price, time):
    if price and time:
        return 1
    if not price and not time:
        return -1
    return 0
