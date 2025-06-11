from src.atoms import Data
from src.typeclass import Function


class Sculpture:
    def __init__(self, data: Data, function: Function):
        self.data = data
        self.function = function

    def sculpt(self) -> Data:
        return self.function.call_data(self.data)
