import streamlit as st
import database
from price_checker import get_price
from streamlit_autorefresh import st_autorefresh
import pandas as pd

st_autorefresh(interval=15000, key="refresh")

st.set_page_config("📈 Trading Terminal", layout="wide")

# ------------------ UI THEME ------------------
st.markdown("""
<style>
html, body {background:#0b1220;color:white;}
.stMetric {background:#111827;padding:15px;border-radius:12px;}
.stDataFrame {border-radius:12px;}
h1,h2,h3 {color:#e5e7eb;}
</style>
""", unsafe_allow_html=True)

database.create_table()
conn = database.connect()
c = conn.cursor()

st.title("📊 Pro Trade Terminal")

# ================= RISK PANEL =================

st.subheader("🧠 Risk Management")

col1,col2,col3 = st.columns(3)

capital = col1.number_input("Total Capital ₹", value=100000.0)
risk_pct = col2.number_input("Risk Per Trade %", value=1.0)
risk_amount = capital * (risk_pct/100)

col3.metric("Risk ₹ Per Trade", round(risk_amount,2))

st.divider()

# ================= ADD TRADE =================

with st.form("trade_form"):
    stock = st.text_input("Stock (RELIANCE, TCS, INFY)")
    buy = st.number_input("Buy Trigger", min_value=0.0)
    sl = st.number_input("Stoploss", min_value=0.0)
    target = st.number_input("Target", min_value=0.0)
    submit = st.form_submit_button("Add Trade")

if submit:
    c.execute("INSERT INTO trades VALUES (NULL,?,?,?,?,?)",
              (stock.upper(), buy, sl, target, "Pending"))
    conn.commit()
    st.success("Trade Added")

st.divider()

# ================= LOAD TRADES =================

c.execute("SELECT * FROM trades")
trades = c.fetchall()

pending, active, target_hit, sl_hit = [], [], [], []
positions = []
total_pl = 0

# ================= LOGIC =================

for t in trades:
    trade_id, stock, buy, sl, target, status = t
    price = get_price(stock)

    if price is None:
        continue

    # ---- Position sizing ----
    risk_per_share = abs(buy - sl)
    qty = int(risk_amount / risk_per_share) if risk_per_share else 0
    reward_risk = round((target - buy) / risk_per_share, 2) if risk_per_share else 0

    # ---- Entry not hit ----
    if price < buy:
        pending.append({
            "Stock":stock,
            "Buy":buy,
            "Current":round(price,2),
            "Qty":qty,
            "R:R":reward_risk
        })
        continue

    # ---- Active P/L ----
    pl = round((price - buy) * qty, 2)
    total_pl += pl

    row = {
        "Stock":stock,
        "Qty":qty,
        "Buy":buy,
        "Current":round(price,2),
        "P/L ₹":pl,
        "R:R":reward_risk
    }

    positions.append(row)

    if price >= target:
        target_hit.append(row)
        status = "Target Hit"
    elif price <= sl:
        sl_hit.append(row)
        status = "SL Hit"
    else:
        active.append(row)
        status = "Active"

    c.execute("UPDATE trades SET status=? WHERE id=?", (status, trade_id))

conn.commit()

df = pd.DataFrame(positions)

# ================= KPI BAR =================

st.subheader("📊 Portfolio Overview")

a,b,c1,d,e = st.columns(5)
a.metric("Active", len(active))
b.metric("Pending", len(pending))
c1.metric("Target Hit", len(target_hit))
d.metric("SL Hit", len(sl_hit))
e.metric("Net P/L ₹", round(total_pl,2))

st.divider()

# ================= COLOR TABLE =================

def color(val):
    if isinstance(val,(int,float)):
        if val > 0: return "color:#22c55e;font-weight:bold"
        if val < 0: return "color:#ef4444;font-weight:bold"
    return ""

# ================= TABS =================

tabs = st.tabs(["📈 Positions","🟡 Pending","🟢 Active","🎯 Target Hit","🔴 Stoploss Hit"])

with tabs[0]:
    if not df.empty:
        st.dataframe(df.style.applymap(color, subset=["P/L ₹"]), use_container_width=True)

with tabs[1]:
    st.dataframe(pd.DataFrame(pending), use_container_width=True)

with tabs[2]:
    st.dataframe(pd.DataFrame(active), use_container_width=True)

with tabs[3]:
    st.dataframe(pd.DataFrame(target_hit), use_container_width=True)

with tabs[4]:
    st.dataframe(pd.DataFrame(sl_hit), use_container_width=True)

st.caption("🔄 Live NSE prices | Risk-based position sizing")
