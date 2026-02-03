import sqlite3
import json
from datetime import datetime

DB_PATH = "nrt.db"


def format_time_counts(tc):
    """
    Pretty print time counts
    """
    if not tc:
        return "N/A"

    try:
        counts = json.loads(tc)
        labels = ["T6", "T5", "T4", "T3", "T2", "T1", "CUR"]
        return " | ".join(
            f"{l}:{c if c is not None else '-'}"
            for l, c in zip(labels, counts)
        )
    except Exception:
        return tc


def review_latest():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Get latest entry per symbol
    cur.execute("""
        SELECT symbol, price_state, time_counts, close, ts
        FROM nrt_states
        WHERE (symbol, ts) IN (
            SELECT symbol, MAX(ts)
            FROM nrt_states
            GROUP BY symbol
        )
        ORDER BY symbol
    """)

    rows = cur.fetchall()
    conn.close()

    print("\n==============================================================")
    print("📊 NRT DATABASE REVIEW (LATEST PER SYMBOL)")
    print("==============================================================")

    if not rows:
        print("No data found in database.")
        return

    for sym, price, time_cnt, close, ts in rows:
        ts_fmt = datetime.fromisoformat(ts).strftime("%Y-%m-%d %H:%M:%S")

        print(f"\nSYMBOL : {sym}")
        print(f"PRICE  : {price}")
        print(f"TIME   : {format_time_counts(time_cnt)}")
        print(f"CLOSE  : {close}")
        print(f"TIME   : {ts_fmt}")


def review_full(symbol=None):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    if symbol:
        cur.execute("""
            SELECT price_state, time_counts, close, ts
            FROM nrt_states
            WHERE symbol = ?
            ORDER BY ts DESC
        """, (symbol,))
    else:
        cur.execute("""
            SELECT symbol, price_state, time_counts, close, ts
            FROM nrt_states
            ORDER BY ts DESC
        """)

    rows = cur.fetchall()
    conn.close()

    print("\n==============================================================")
    print("📊 NRT DATABASE FULL HISTORY")
    print("==============================================================")

    if not rows:
        print("No data found.")
        return

    for row in rows:
        if symbol:
            price, time_cnt, close, ts = row
            sym = symbol
        else:
            sym, price, time_cnt, close, ts = row

        ts_fmt = datetime.fromisoformat(ts).strftime("%Y-%m-%d %H:%M:%S")

        print(
            f"{ts_fmt} | "
            f"{sym:12} | "
            f"PRICE={price:8} | "
            f"TIME={format_time_counts(time_cnt)} | "
            f"CLOSE={close}"
        )


if __name__ == "__main__":
    # ---- OPTIONS ----
    review_latest()          # latest snapshot per symbol
    # review_full()          # uncomment to see full DB
    # review_full("NIFTY")   # uncomment to filter single symbol
