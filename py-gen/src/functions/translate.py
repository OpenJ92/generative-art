from numpy import array

from src.typeclass.__function__ import __Function__


class Translate(__Function__):
    def __init__(self, dv):
        self.dv: array = dv

    def __call__(self, data: array):
        return data + self.dv
