from engine.state import MotionState
import math

class MotionState:
    def __init__(self):
        self.prev_high = None
        self.prev_low = None

        self.direction = 0          # +1 up, -1 down
        self.swing_high = None
        self.swing_low = None

        self.bullish_tp = None
        self.bearish_tp = None

        # Ordered TP sequence
        self.tp_sequence = []


class MotionEngine:
    def __init__(self):
        self.state = MotionState()

    def _append_tp(self, tp_type, value):
        self.state.tp_sequence.append((tp_type, value))

    def process_bar(self, row):
        s = self.state
        H, L = row.H, row.L

        # -------- INIT --------
        if s.prev_high is None:
            s.prev_high = H
            s.prev_low = L
            s.swing_high = H
            s.swing_low = L
            return

        # -------- INSIDE BAR --------
        if H <= s.prev_high and L >= s.prev_low:
            return

        # -------- OUTSIDE BAR DETECTION --------
        outside_bar = H > s.prev_high and L < s.prev_low

        # Resolve outside bar in direction of trend
        if outside_bar:
            if s.direction >= 0:
                # Treat as UP bar
                H_effective = H
                L_effective = s.prev_low
            else:
                # Treat as DOWN bar
                H_effective = s.prev_high
                L_effective = L
        else:
            H_effective = H
            L_effective = L

        # -------- UP MOVE --------
        if H_effective > s.prev_high:
            if s.direction <= 0:
                if s.direction == -1:
                    s.bearish_tp = s.swing_low
                    self._append_tp("BEARISH", s.bearish_tp)

                s.swing_high = H_effective
                s.direction = 1
            else:
                s.swing_high = max(s.swing_high, H_effective)

        # -------- DOWN MOVE --------
        elif L_effective < s.prev_low:
            if s.direction >= 0:
                if s.direction == 1:
                    s.bullish_tp = s.swing_high
                    self._append_tp("BULLISH", s.bullish_tp)

                s.swing_low = L_effective
                s.direction = -1
            else:
                s.swing_low = min(s.swing_low, L_effective)

        s.prev_high = H
        s.prev_low = L