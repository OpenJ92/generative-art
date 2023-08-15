from typing import List
from numpy import array

from src.typeclass.__function__ import __Function__
from src.typeclass.__sculpture__ import __Sculpture__
from src.atoms import __Data__

class Composition(__Function__):
    def __init__(self, funcs: List[__Function__]):
        self.funcs = funcs

    def __call__(self, data: array):
        return data

    def __call_data__(self, data: __Data__) -> __Data__:
        for func in self.funcs:
            data = __Sculpture__(data, func).sculpt()
        return data
