class BiasPhase:
    """
    River BIAS Engine (REPAINTING VERSION)

    Matches TradingView River Bias behavior.

    Key properties:
    - Bias is NEVER neutral
    - Bias flips ONLY on BAR CLOSE beyond structure
    - Structural levels repaint until bar close
    - Motion line is contextual, not the trigger
    """

    def __init__(self):
        self.bias_state = None
        self.last_support = None       # last bullish TP low
        self.last_resistance = None    # last bearish TP high

    # ----------------------------------
    # MAIN UPDATE (REPAINTING)
    # ----------------------------------
    def update(self, row, tp_sequence, motion_state=None):
        """
        row must contain: H, L, C
        """

        C = row.C

        # ---------------------------
        # INITIALIZE BIAS ASAP
        # ---------------------------
        if self.bias_state is None:
            if tp_sequence:
                last_tp = tp_sequence[-1]
                self.bias_state = (
                    "POSITIVE" if last_tp[0] == "BULLISH" else "NEGATIVE"
                )
            else:
                self.bias_state = "POSITIVE"

        # ---------------------------
        # TRACK STRUCTURAL LEVELS (REPAINTING)
        # ---------------------------
        if tp_sequence:
            last_tp = tp_sequence[-1]

            if last_tp[0] == "BULLISH":
                self.last_support = last_tp[1]

            elif last_tp[0] == "BEARISH":
                self.last_resistance = last_tp[1]

        # ---------------------------
        # BIAS FLIP ON BAR CLOSE
        # ---------------------------
        if self.bias_state == "POSITIVE":
            if self.last_support is not None and C < self.last_support:
                self.bias_state = "NEGATIVE"

        elif self.bias_state == "NEGATIVE":
            if self.last_resistance is not None and C > self.last_resistance:
                self.bias_state = "POSITIVE"

        return self.bias_state
