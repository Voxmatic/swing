def compute_strength(price, time, bias, tp_count, time_dom):
    score = 0

    if price == bias:
        score += 3
    if time == bias:
        score += 3
    if time_dom >= 2:
        score += 2
    if tp_count >= 6:
        score += 2

    return round(score / 10, 2)
