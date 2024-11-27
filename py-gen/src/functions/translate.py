from numpy import array

from src.typeclass.__function__ import Function


class Translate(Function):
    def __init__(self, dv):
        self.dv: array = dv

    def __call__(self, data: array):
        return data + self.dv
