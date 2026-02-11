import streamlit as st
import sqlite3
import pandas as pd
from tvDatafeed import TvDatafeed, Interval

# =========================
# CONFIG
# =========================

st.set_page_config("Kite Style Trading Portal", layout="wide")

tv = TvDatafeed(username=None, password=None)

# =========================
# DATABASE
# =========================

conn = sqlite3.connect("trades.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS trades (
id INTEGER PRIMARY KEY,
symbol TEXT,
buy REAL,
sl REAL,
target REAL,
status TEXT,
entry_triggered INTEGER
)
""")
conn.commit()

# =========================
# ACCURATE LTP
# =========================

def get_price(symbol):
    try:
        df = tv.get_hist(
            symbol=symbol,
            exchange="NSE",
            interval=Interval.in_1_minute,
            n_bars=3
        )
        return round(float(df["close"].iloc[-1]), 2)
    except:
        return None

# =========================
# UPDATE STATUS
# =========================

def update_trades():
    rows = c.execute("SELECT * FROM trades").fetchall()

    for r in rows:
        id, sym, buy, sl, tgt, status, triggered = r
        price = get_price(sym)

        if price is None:
            continue

        if not triggered and price >= buy:
            c.execute(
                "UPDATE trades SET entry_triggered=1,status='ACTIVE' WHERE id=?",
                (id,)
            )

        elif triggered:
            if price >= tgt:
                c.execute("UPDATE trades SET status='TARGET HIT' WHERE id=?", (id,))
            elif price <= sl:
                c.execute("UPDATE trades SET status='STOPLOSS HIT' WHERE id=?", (id,))

    conn.commit()

# =========================
# EDIT & DELETE
# =========================

def delete_trade(tid):
    c.execute("DELETE FROM trades WHERE id=?", (tid,))
    conn.commit()
    st.experimental_rerun()

def update_trade(tid, buy, sl, target):
    c.execute(
        "UPDATE trades SET buy=?, sl=?, target=? WHERE id=?",
        (buy, sl, target, tid)
    )
    conn.commit()
    st.experimental_rerun()

# =========================
# KITE STYLE CARD
# =========================

def trade_card(row):

    ltp = get_price(row.symbol)
    if ltp is None:
        st.warning("Price unavailable")
        return

    pnl = round(ltp - row.buy, 2)
    color = "#00c853" if pnl >= 0 else "#ff5252"

    st.markdown(f"""
    <div style="
    background:white;
    padding:16px;
    border-radius:14px;
    box-shadow:0 4px 15px rgba(0,0,0,0.12);
    margin-bottom:12px;">
        <h3>{row.symbol}</h3>
        <b>LTP:</b> {ltp}<br>
        <b>BUY:</b> {row.buy}<br>
        <b style="color:{color};font-size:18px;">P&L: {pnl}</b><br>
        🎯 {row.target} &nbsp;&nbsp; ❌ {row.sl}
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        if st.button("✏️ Edit", key=f"edit{row.id}"):
            st.session_state["edit"] = row.id

    with c2:
        if st.button("🗑 Delete", key=f"del{row.id}"):
            delete_trade(row.id)

    if st.session_state.get("edit") == row.id:
        with st.form(f"editform{row.id}"):
            nb = st.number_input("New Buy", value=float(row.buy))
            ns = st.number_input("New Stoploss", value=float(row.sl))
            nt = st.number_input("New Target", value=float(row.target))
            save = st.form_submit_button("Save Changes")

            if save:
                update_trade(row.id, nb, ns, nt)

# =========================
# HEADER
# =========================

st.title("📈 Zerodha Kite-Style Trading Portal")

# =========================
# REFRESH BUTTON
# =========================

if st.button("🔄 Refresh Prices & Update Trades"):
    update_trades()
    st.experimental_rerun()

# =========================
# ADD TRADE
# =========================

with st.form("add_trade"):
    a, b, c_, d = st.columns(4)

    sym = a.text_input("Stock (NSE)", placeholder="RELIANCE")
    buy = b.number_input("Buy Price", step=0.1)
    sl = c_.number_input("Stoploss", step=0.1)
    tgt = d.number_input("Target", step=0.1)

    submit = st.form_submit_button("➕ Add Trade")

    if submit:
        c.execute(
            "INSERT INTO trades VALUES (NULL,?,?,?,?,?,?)",
            (sym, buy, sl, tgt, "PENDING", 0)
        )
        conn.commit()
        st.success("Trade added!")

# =========================
# TABS
# =========================

tabs = st.tabs([
    "🕒 Pending",
    "📊 Active",
    "🎯 Target Hit",
    "❌ Stoploss Hit",
    "📈 Analytics"
])

def show(status):
    df = pd.read_sql(
        f"SELECT * FROM trades WHERE status='{status}'",
        conn
    )

    if df.empty:
        st.info("No trades here")
        return

    cols = st.columns(2)

    for i, row in df.iterrows():
        with cols[i % 2]:
            trade_card(row)

with tabs[0]: show("PENDING")
with tabs[1]: show("ACTIVE")
with tabs[2]: show("TARGET HIT")
with tabs[3]: show("STOPLOSS HIT")

# =========================
# ANALYTICS
# =========================

with tabs[4]:
    df = pd.read_sql("SELECT * FROM trades", conn)

    total = len(df)
    wins = len(df[df.status == "TARGET HIT"])
    losses = len(df[df.status == "STOPLOSS HIT"])

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Trades", total)
    c2.metric("Targets Hit", wins)
    c3.metric("Stoploss Hit", losses)

    if total:
        c4.metric("Win Rate", f"{round(wins/total*100,1)}%")

# =========================
# FOOTER
# =========================

st.caption("Manual refresh Kite-style Trading Dashboard")
