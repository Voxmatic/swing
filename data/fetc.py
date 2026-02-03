import pandas as pd
import yfinance as yf

from tvDatafeed import TvDatafeed, Interval


class TVFetcher:
    """
    Unified market data fetcher:
    1) TradingView (primary)
    2) Yahoo Finance (fallback)

    Output format (ALWAYS):
    datetime | O | H | L | C
    """

    def __init__(self, username=None, password=None):
        if username and password:
            self.tv = TvDatafeed(username, password)
        else:
            self.tv = TvDatafeed()  # no-login mode

    # =================================================
    # PUBLIC API
    # =================================================
    def fetch_daily(self, symbol, exchange="NSE", bars=300):
        """
        Fetch DAILY OHLC data.
        Tries TradingView first, falls back to Yahoo Finance.
        """

        # ---------- Try TradingView ----------
        try:
            df = self._fetch_tv(symbol, exchange, bars)
            if df is not None and not df.empty:
                return df
        except Exception as e:
            print(f"[TV FAIL] {symbol} → {e}")

        # ---------- Fallback to Yahoo ----------
        try:
            df = self._fetch_yf(symbol)
            if df is not None and not df.empty:
                print(f"[DATA] {symbol} → Yahoo Finance")
                return df
        except Exception as e:
            print(f"[YF FAIL] {symbol} → {e}")

        return None

    # =================================================
    # INTERNAL: TRADINGVIEW
    # =================================================
    def _fetch_tv(self, symbol, exchange, bars):
        df = self.tv.get_hist(
            symbol=symbol,
            exchange=exchange,
            interval=Interval.in_daily,
            n_bars=bars
        )

        if df is None or df.empty:
            return None

        df = df.reset_index()

        df = df.rename(columns={
            "open": "O",
            "high": "H",
            "low": "L",
            "close": "C",
            "volume": "V",
            "datetime": "datetime"
        })

        # Ensure scalar numeric values
        for col in ["O", "H", "L", "C"]:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        df = df.dropna(subset=["O", "H", "L", "C"])

        return df[["datetime", "O", "H", "L", "C"]]

    # =================================================
    # INTERNAL: YAHOO FINANCE (SAFE FALLBACK)
    # =================================================
    def _fetch_yf(self, symbol):
        yf_symbol = self._map_yf_symbol(symbol)

        df = yf.download(
            yf_symbol,
            period="2y",
            interval="1d",
            auto_adjust=False,
            progress=False,
            group_by="column"
        )

        if df is None or df.empty:
            return None

        # ---- Flatten MultiIndex (CRITICAL FIX) ----
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        df = df.reset_index()

        # ---- Force scalar numeric OHLC ----
        for col in ["Open", "High", "Low", "Close"]:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        df = df.dropna(subset=["Open", "High", "Low", "Close"])

        df = df.rename(columns={
            "Date": "datetime",
            "Open": "O",
            "High": "H",
            "Low": "L",
            "Close": "C"
        })

        return df[["datetime", "O", "H", "L", "C"]]

    # =================================================
    # SYMBOL MAP FOR YAHOO
    # =================================================
    def _map_yf_symbol(self, symbol):
        symbol = symbol.upper().strip()

        INDEX_MAP = {
            "NIFTY": "^NSEI",
            "BANKNIFTY": "^NSEBANK",
            "FINNIFTY": "^CNXFIN"
        }

        if symbol in INDEX_MAP:
            return INDEX_MAP[symbol]

        # NSE stocks
        if not symbol.endswith(".NS"):
            return symbol + ".NS"

        return symbol
