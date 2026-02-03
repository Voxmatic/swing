from data.fetcher import TVFetcher
from engine.motion_line import MotionEngine
from engine.price_engine import PriceEngine
from engine.time_phase3 import TimePhase3   # <-- NEW FILE

SYMBOL = "BAJFINANCE"
EXCHANGE = "NSE"
BARS = 300

tv = TVFetcher()
df = tv.fetch_daily(SYMBOL, EXCHANGE, BARS)

motion_engine = MotionEngine()
price_engine = PriceEngine()
time_engine = TimePhase3()

price_state = None
time_state = None

for _, row in df.iterrows():
    motion_engine.process_bar(row)

    price_state = price_engine.update(
        close_price=row.C,
        tp_sequence=motion_engine.state.tp_sequence
    )

    time_state = time_engine.evaluate(
        motion_engine.state.tp_sequence
    )

s = motion_engine.state

print("\n==============================")
print("NRT RESULT (PHASE 1 → 3)")
print("==============================")
print("SYMBOL      :", SYMBOL)
print("PRICE STATE :", price_state)
print("TIME STATE  :", time_state)
print("Close       :", df.iloc[-1].C)
