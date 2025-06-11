from src.executors import Sculpture

class Tile(Sculpture):
    def __init__(self, sculptures, ranges):
        self.sculptures = sculptures
        self.ranges = ranges

    def sculpt(self):
        raise NotImplementedError
