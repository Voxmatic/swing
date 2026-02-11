import streamlit as st
from scan import run_scan

st.set_page_config(page_title="NRT Scanner", layout="wide")

st.title("📈 NRT BULLISH SCANNER")

if st.button("Run Scan"):

    with st.spinner("Scanning market..."):
        results = run_scan()

    if not results:
        st.warning("No bullish stocks found")
    else:
        st.success(f"{len(results)} bullish stocks found")

        for r in results:
            st.write(
                f"✅ {r['symbol']} | "
                f"PRICE={r['price']} | "
                f"TIME={r['time']} | "
                f"BIAS={r['bias']} | "
                f"CLOSE={r['close']}"
            )
