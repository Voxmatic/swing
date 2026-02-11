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
    "NIFTY","BANKNIFTY","360ONE","3MINDIA","ABB","ACC","ACMESOLAR",
    "AIAENG","APLAPOLLO","AUBANK","AWL","BAJAJ-AUTO","BAJFINANCE",
    "BAJAJFINSV","RELIANCE","HDFCBANK","ICICIBANK","INFY","TCS",
    # you can keep full list here
]


# ----------------------------------
# INIT
# ----------------------------------
init_db()
tv = TVFetcher()

print("\n==============================")
print("RUNNING NRT BULLISH SCAN")
print("BB LOWER → RSI → PRICE+TIME or PRICE+BIAS")
print("==============================\n")


# ----------------------------------
# MAIN LOOP
# ----------------------------------
for SYMBOL in SYMBOLS:

    print(f"\n🔍 Scanning: {SYMBOL}")

    # =============================
    # 1️⃣ WEEKLY BOLLINGER FILTER
    # =============================
    if not passes_weekly_bb(SYMBOL):
        print("❌ BB lower band not touched")
        continue


    # =============================
    # 2️⃣ FETCH DAILY DATA
    # =============================
    try:
        df = tv.fetch_daily(SYMBOL, EXCHANGE, BARS)
    except Exception as e:
        print("FETCH ERROR:", e)
        continue

    if df is None or df.empty or len(df) < 50:
        print("NO DATA — SKIPPED")
        continue


    # =============================
    # 3️⃣ RSI FILTER
    # =============================
    rsi_ok, last_rsi = passes_rsi_filter(df)

    if not rsi_ok:
        print(f"❌ RSI filter failed (RSI={last_rsi:.2f})")
        continue

    print(f"✅ BB + RSI passed (RSI={last_rsi:.2f})")


    # =============================
    # 4️⃣ NRT ENGINES
    # =============================
    motion_engine = MotionEngine()
    price_engine = PriceEngine()
    time_engine  = TimePhase3()
    bias_engine  = BiasPhase()

    price_state = None
    time_state  = None
    bias_state  = None


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


    # =============================
    # 5️⃣ FINAL BULLISH LOGIC
    # =============================
    bullish_signal = (
        (price_state == "POSITIVE" and time_state == "POSITIVE") or
        (price_state == "POSITIVE" and bias_state == "POSITIVE")
    )

    if not bullish_signal:
        reset_alert(SYMBOL)
        continue


    # =============================
    # 6️⃣ STORE STATE
    # =============================
    insert_state(
        SYMBOL,
        price_state,
        time_state,
        bias_state,
        float(df.iloc[-1].C)
    )


    # =============================
    # 7️⃣ DISCORD ALERT (NO SPAM)
    # =============================
    prev = last_alert(SYMBOL)

    if prev:
        prev_state, alert_time = prev

        if prev_state == "BULLISH" and not cooldown_ok(alert_time, COOLDOWN_HOURS):
            print("⏳ Cooldown active — no repeat alert")
            continue

        if prev_state != "BULLISH":
            reset_alert(SYMBOL)


    send_alert(SYMBOL, "BULLISH")
    update_alert(SYMBOL, "BULLISH")

    print("🚨 BULLISH ALERT SENT:", SYMBOL)


print("\n✅ Scan completed.")
