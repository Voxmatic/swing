class TimePhase3:
    """
    Phase-3 TIME Engine (True NRT)

    TIME COUNT = number of candles where motion line is touched,
    excluding inside bars, including outside & violent outside bars.
    """

    def __init__(self):
        self.time_state = None
        self.last_tp_index = None
        self.prev_leg_count = None
        self.running_leg_count = 0

        self.prev_high = None
        self.prev_low = None

    def _is_inside_bar(self, H, L):
        return H <= self.prev_high and L >= self.prev_low

    def update(self, row, tp_sequence):
        """
        row : dataframe row (must contain H, L)
        tp_sequence : Phase-1 TP list (read-only)
        """

        H, L = row.H, row.L
        idx = row.name

        # INIT
        if self.prev_high is None:
            self.prev_high = H
            self.prev_low = L
            return self.time_state or "NEUTRAL"

        # Detect inside bar
        inside = self._is_inside_bar(H, L)

        # Count motion-line bar
        if not inside:
            self.running_leg_count += 1

        # Detect NEW turning point
        if len(tp_sequence) >= 2:
            last_tp = tp_sequence[-1]
            tp_idx = last_tp[2] if len(last_tp) >= 3 else idx

            if self.last_tp_index != tp_idx:
                # New TP confirmed
                if self.prev_leg_count is None:
                    self.prev_leg_count = self.running_leg_count
                else:
                    # Apply TP count +1 inertia rule
                    if self.time_state == "POSITIVE":
                        if self.running_leg_count >= self.prev_leg_count + 1:
                            self.time_state = "NEGATIVE"
                    elif self.time_state == "NEGATIVE":
                        if self.running_leg_count >= self.prev_leg_count + 1:
                            self.time_state = "POSITIVE"

                # Reset for new leg
                self.prev_leg_count = self.running_leg_count
                self.running_leg_count = 0
                self.last_tp_index = tp_idx

                # INIT state
                if self.time_state is None:
                    self.time_state = (
                        "POSITIVE" if last_tp[0] == "BULLISH" else "NEGATIVE"
                    )

        self.prev_high = H
        self.prev_low = L

        return self.time_state
