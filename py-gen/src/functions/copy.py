from src.typeclass.function import Function
from src.atoms import Data, List

from itertools import repeat
from numpy import array


class Copy(Function):
    def __init__(self, times):
        self.times = times

    def __call__(self, data: array):
        return data

    def call_data(self, data: Data):
        return List(list(repeat(data, self.times)))
