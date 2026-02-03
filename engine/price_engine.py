class PriceEngine:
    """
    Phase-2 PRICE Engine (NRT compliant)

    PRICE is decided ONLY by the last crossed turning point
    from the alternating TP sequence generated in Phase-1.
    """

    def __init__(self):
        self.price_state = None              # "POSITIVE" or "NEGATIVE"
        self.last_crossed_index = None       # index in TP sequence

    def update(self, close_price, tp_sequence):
        """
        Parameters
        ----------
        close_price : float
            Current candle close price

        tp_sequence : list of tuples
            Ordered list from Phase-1:
            [("BULLISH", price), ("BEARISH", price), ...]
            Oldest → Newest
        """

        # Iterate from NEWEST → OLDEST
        for idx in range(len(tp_sequence) - 1, -1, -1):
            tp_type, tp_price = tp_sequence[idx]

            # Skip already processed crossings
            if self.last_crossed_index is not None and idx <= self.last_crossed_index:
                break

            # ---- Bullish TP crossed upward ----
            if tp_type == "BULLISH" and close_price > tp_price:
                self.last_crossed_index = idx
                self.price_state = "POSITIVE"
                return self.price_state

            # ---- Bearish TP crossed downward ----
            if tp_type == "BEARISH" and close_price < tp_price:
                self.last_crossed_index = idx
                self.price_state = "NEGATIVE"
                return self.price_state

        # If nothing new crossed, retain previous state
        return self.price_state
