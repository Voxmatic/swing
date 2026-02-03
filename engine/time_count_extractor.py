def extract_time_counts(time_engine):
    counts = list(time_engine.completed_tp_counts)

    while len(counts) < 6:
        counts.insert(0, "-")

    return {
        "T6": counts[0],
        "T5": counts[1],
        "T4": counts[2],
        "T3": counts[3],
        "T2": counts[4],
        "T1": counts[5],
        "CUR": time_engine.current_count,
    }
