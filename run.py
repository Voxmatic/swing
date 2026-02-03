import time

from data.fetcher import TVFetcher
from engine.motion_line import MotionEngine
from engine.price_engine import PriceEngine
from engine.time_phase3 import TimePhase3
from engine.time_count_extractor import extract_time_counts

from db import init_db, insert_state


# ----------------------------------
# CONFIG
# ----------------------------------
EXCHANGE = "NSE"
BARS = 300
SLEEP_SEC = 1.2

# ----------------------------------
# SYMBOLS (TradingView format ONLY)
# ----------------------------------
SYMBOLS = [
    "NIFTY",
    "BANKNIFTY",
    "FINNIFTY",
    "RELIANCE",
    "HDFCBANK",
    "ICICIBANK",
    "INFY",
    "TCS",
    "BAJAJ-AUTO",
    "BAJFINANCE",
    "BAJAJFINSV",
]

# ----------------------------------
# INIT DATABASE
# ----------------------------------
init_db()


def run_symbol(symbol: str):
    tv = TVFetcher()

    try:
        df = tv.fetch_daily(symbol, EXCHANGE, BARS)
    except Exception as e:
        print(f"[{symbol}] FETCH ERROR → {e}")
        return

    if df is None or df.empty or len(df) < 50:
        print(f"[{symbol}] NO DATA / SKIPPED")
        return

    # ----------------------------------
    # ENGINE INITIALIZATION
    # ----------------------------------
    motion_engine = MotionEngine()
    price_engine = PriceEngine()
    time_engine = TimePhase3()

    price_state = None

    # ----------------------------------
    # BAR BY BAR PROCESSING
    # ----------------------------------
    for _, row in df.iterrows():

        # Phase-1
        motion_engine.process_bar(row)

        # Phase-2
        price_state = price_engine.update(
            close_price=row.C,
            tp_sequence=motion_engine.state.tp_sequence
        )

        # Phase-3
        row.motion_moved = motion_engine.state.motion_moved
        time_engine.update(
            row,
            motion_engine.state.tp_sequence
        )

    # ----------------------------------
    # EXTRACT FINAL TIME COUNTS
    # ----------------------------------
    time_counts = extract_time_counts(time_engine)

    # ----------------------------------
    # STORE RESULT IN DATABASE
    # ----------------------------------
    insert_state(
        symbol=symbol,
        price_state=price_state,
        time_counts=time_counts,
        close=float(df.iloc[-1].C)
    )

    print(
        f"[DB STORED] {symbol} | "
        f"PRICE={price_state} | "
        f"TIME={time_engine.time_state} | "
        f"COUNTS={time_counts}"
    )


def main():
    print("\n==============================")
    print("RUNNING NRT DATA COLLECTION")
    print("==============================\n")

    total = len(SYMBOLS)

    for idx, sym in enumerate(SYMBOLS, start=1):
        symbol = sym.strip().upper()

        print(f"[{idx}/{total}] Processing {symbol}")

        run_symbol(symbol)

        time.sleep(SLEEP_SEC)


if __name__ == "__main__":
    main()
