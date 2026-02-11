import streamlit as st
from scan import run_scan

st.set_page_config(
    page_title="NRT Market Scanner",
    layout="wide"
)

st.title("📈 NRT Smart Market Scanner")
st.caption("Bollinger + RSI + Price + Time + Bias Engine")

if st.button("🚀 Run Scan"):

    with st.spinner("Scanning market..."):
        bullish = run_scan()

    st.success("Scan Complete")

    st.subheader("🔥 Bullish Signals")

    if bullish:
        for sym in bullish:
            st.write("✅", sym)
    else:
        st.write("No bullish setups today")
