from numpy import array

from src.typeclass.__function__ import __Function__
from src.typeclass.__sculpture__ import __Sculpture__
from src.atoms import __Data__, List

class ZipApply(__Function__):
    def __init__(self, funcs):
        self.funcs = funcs

    def __call__(self, data: array):
        return data

    def __call_data__(self, data: __Data__) -> __Data__:
        match data:
            case List(elements=elements):
                applied = []
                for element, func in zip(elements, self.funcs):
                    applied = [*applied, __Sculpture__(element, func).sculpt()]
                return List(applied)
            case _:
                raise NotImplementedError
