class Hole:
    def __init__(
        self,
        hole_type: str,
        position: dict,
        size: float,
        tolerance: float
    ):
        self.hole_type = hole_type
        self.position = position
        self.size = size
        self.tolerance = tolerance
