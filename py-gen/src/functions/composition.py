from typing import List
from numpy import array

from src.typeclass import Function
from src.executors import Sculpture
from src.atoms import Data


class Composition(Function):
    def __init__(self, funcs: List[Function]):
        self.funcs = funcs

    def __call__(self, data: array):
        for func in self.funcs:
            data = func(data)
        return data

    def call_data(self, data: Data) -> Data:
        for func in self.funcs:
            data = Sculpture(data, func).sculpt()
        return data
