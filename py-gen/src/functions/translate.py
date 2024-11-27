from src.typeclass import Function
from numpy import array


class Translate(Function):
    def __init__(self, dv):
        self.dv: array = dv

    def __call__(self, data: array):
        return data + self.dv
