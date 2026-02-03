from data.fetcher import TVFetcher
from engine.motion_line import MotionEngine
from engine.price_engine import PriceEngine
from engine.time_phase3 import TimePhase3
from engine.bias_phase import BiasPhase

from bb_weekly_filter import passes_weekly_bb
from rsi_filter import passes_rsi_filter
from db import (
    init_db,
    insert_state,
    last_alert,
    update_alert,
    reset_alert,
    cooldown_ok
)
from discord_alert import send_alert

# ----------------------------------
# CONFIG
# ----------------------------------
EXCHANGE = "NSE"
BARS = 300
COOLDOWN_HOURS = 24

SYMBOLS = [
    "TRITURBINE"
]

# ----------------------------------
# INIT
# ----------------------------------
init_db()
tv = TVFetcher()

print("\n==============================")
print("RUNNING NRT BULLISH SCAN")
print("BB (LOWER) → RSI → PRICE+TIME / PRICE+BIAS")
print("==============================")

# ----------------------------------
# MAIN LOOP
# ----------------------------------
for SYMBOL in SYMBOLS:
    print(f"\nScanning: {SYMBOL}")

    # -----------------------------
    # WEEKLY BOLLINGER LOWER BAND
    # -----------------------------
    if not passes_weekly_bb(SYMBOL):
        print("❌ BB filter failed")
        continue

    # -----------------------------
    # FETCH DAILY DATA
    # -----------------------------
    try:
        df = tv.fetch_daily(SYMBOL, EXCHANGE, BARS)
    except Exception as e:
        print("FETCH ERROR:", e)
        continue

    if df is None or df.empty or len(df) < 50:
        print("NO DATA — SKIPPED")
        continue

    # -----------------------------
    # RSI FILTER
    # -----------------------------
    rsi_ok, last_rsi = passes_rsi_filter(df)
    if not rsi_ok:
        print(f"❌ RSI failed (RSI={last_rsi})")
        continue

    print(f"✅ BB + RSI passed (RSI={last_rsi})")

    motion_engine = MotionEngine()
    price_engine = PriceEngine()
    time_engine = TimePhase3()
    bias_engine = BiasPhase()

    price_state = None
    time_state = None
    bias_state = None

    # -----------------------------
    # NRT ENGINE
    # -----------------------------
    for _, row in df.iterrows():
        motion_engine.process_bar(row)

        price_state = price_engine.update(
            close_price=row.C,
            tp_sequence=motion_engine.state.tp_sequence
        )

        time_state = time_engine.update(
            row,
            motion_engine.state.tp_sequence
        )

        bias_state = bias_engine.update(
            row,
            motion_engine.state.tp_sequence
        )

    print(
        f"PRICE={price_state} | "
        f"TIME={time_state} | "
        f"BIAS={bias_state}"
    )

    # -----------------------------
    # FINAL BULLISH CONDITION
    # -----------------------------
    bullish_signal = (
        (price_state == "POSITIVE" and time_state == "POSITIVE") or
        (price_state == "POSITIVE" and bias_state == "POSITIVE")
    )

    if not bullish_signal:
        reset_alert(SYMBOL)
        continue

    # -----------------------------
    # STORE STATE
    # -----------------------------
    insert_state(
        symbol=SYMBOL,
        price_state=price_state,
        time_state=time_state,
        bias_state=bias_state,
        close=float(df.iloc[-1].C)
    )

    # -----------------------------
    # DISCORD ALERT (NO REPEAT)
    # -----------------------------
    prev = last_alert(SYMBOL)

    if prev:
        prev_state, alert_time = prev
        if prev_state == "BULLISH" and not cooldown_ok(alert_time, COOLDOWN_HOURS):
            continue
        if prev_state != "BULLISH":
            reset_alert(SYMBOL)

    send_alert(SYMBOL, "BULLISH")
    update_alert(SYMBOL, "BULLISH")

    print("🚨 BULLISH ALERT SENT:", SYMBOL)
