import pandas as pd
import numpy as np


def compute_rsi(close, period=14):
    delta = close.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


def passes_rsi_filter(df, low=0, high=40):
    """
    Daily RSI filter
    """
    close = df["C"]
    rsi = compute_rsi(close)

    last_rsi = float(rsi.iloc[-1])

    return low <= last_rsi <= high, round(last_rsi, 2)
