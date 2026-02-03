def screen_positive(state):
    price_ok = compute_price_signal(state)
    time_ok = compute_time_signal(state)
    if price_ok and time_ok:
        return "STRONG BUY"
    return None

def screen_negative(state):
    price_ok = compute_price_signal(state) == False
    time_ok = compute_time_signal(state) == False
    if price_ok and time_ok:
        return "STRONG SELL"
    return None
