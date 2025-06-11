from src.typeclass import Function
from src.executors import Sculpture
from src.atoms import Data, List
from numpy import array

class Map(Function):
    def __init__(self, func):
        self.func = func

    def __call__(self, data: array):
        return data

    def call_data(self, data: Data):
        match data:
            case List(elements=elements):
                applied = []
                for element in elements:
                    applied.append(Sculpture(element, self.func).sculpt())
                return List(applied)
            case _:
                raise NotImplementedError
