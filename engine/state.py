class MotionState:
    def __init__(self):
        # Previous bar
        self.prev_high = None
        self.prev_low = None

        # Motion
        self.direction = 0           # +1 up, -1 down
        self.swing_high = None
        self.swing_low = None

        # Turning Points (PHASE-1)
        self.bullish_tp = None       # swing high
        self.bearish_tp = None       # swing low

        # Price State (PHASE-2)
        self.price_state = "NEGATIVE"
