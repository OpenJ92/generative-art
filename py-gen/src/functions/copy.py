from src.typeclass.__function__ import __Function__
from src.atoms import __Data__, List

from itertools import repeat
from numpy import array

class Copy(__Function__):
    def __init__(self, times):
        self.times = times

    def __call__(self, data: array):
        return data

    def __call_data__(self, data: __Data__):
        return List(list(repeat(data, self.times)))
