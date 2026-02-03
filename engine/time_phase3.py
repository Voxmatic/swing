class TimePhase3:
    """
    Phase-3 TIME Engine (True NRT Logic)

    TIME COUNT = count of motion-line bars only
    (inside bars excluded, outside/violent bars included)

    TIME rules:
    - running > previous  → dominance flip
    - running == previous → NEUTRAL
    - running < previous  → hold state
    """

    def __init__(self):
        self.time_state = None            # POSITIVE / NEGATIVE / NEUTRAL
        self.prev_leg_count = None        # completed TP leg count
        self.running_leg_count = 0        # current leg count
        self.last_tp_seen = None

        self.prev_high = None
        self.prev_low = None

    def _is_inside_bar(self, H, L):
        return H <= self.prev_high and L >= self.prev_low

    def update(self, row, tp_sequence):
        H, L = row.H, row.L

        # INIT
        if self.prev_high is None:
            self.prev_high = H
            self.prev_low = L
            return self.time_state or "NEUTRAL"

        # Count motion-line bars ONLY
        inside = self._is_inside_bar(H, L)
        if not inside:
            self.running_leg_count += 1

        # Detect new TP
        if tp_sequence:
            last_tp = tp_sequence[-1]

            if self.last_tp_seen != last_tp:
                # New TP confirmed → leg completed
                if self.prev_leg_count is None:
                    self.prev_leg_count = self.running_leg_count
                else:
                    # Apply dominance + equality rule
                    if self.running_leg_count > self.prev_leg_count:
                        self.time_state = (
                            "POSITIVE" if last_tp[0] == "BULLISH" else "NEGATIVE"
                        )
                    elif self.running_leg_count == self.prev_leg_count:
                        self.time_state = "NEUTRAL"
                    # else → hold previous state

                # Reset for new leg
                self.prev_leg_count = self.running_leg_count
                self.running_leg_count = 0
                self.last_tp_seen = last_tp

                # Initial state
                if self.time_state is None:
                    self.time_state = (
                        "POSITIVE" if last_tp[0] == "BULLISH" else "NEGATIVE"
                    )

        self.prev_high = H
        self.prev_low = L

        return self.time_state
