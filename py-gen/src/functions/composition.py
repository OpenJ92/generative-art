from typing import List
from numpy import array

from src.typeclass.__function__ import Function
from src.typeclass.sculpture import Sculpture
from src.atoms import __Data__


class Composition(Function):
    def __init__(self, funcs: List[Function]):
        self.funcs = funcs

    def __call__(self, data: array):
        for func in self.funcs:
            data = func(data)
        return data

    def __call_data__(self, data: __Data__) -> __Data__:
        for func in self.funcs:
            data = Sculpture(data, func).sculpt()
        return data
