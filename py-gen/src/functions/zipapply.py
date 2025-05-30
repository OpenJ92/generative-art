from src.typeclass import Function, Sculpture
from src.atoms import Data, List
from numpy import array

class ZipApply(Function):
    def __init__(self, funcs):
        self.funcs = funcs

    def __call__(self, data: array):
        return data

    def call_data(self, data: Data) -> Data:
        match data:
            case List(elements=elements):
                applied = []
                for element, func in zip(elements, self.funcs):
                    applied = [*applied, Sculpture(element, func).sculpt()]
                return List(applied)
            case _:
                raise NotImplementedError
