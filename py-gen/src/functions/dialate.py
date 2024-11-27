from numpy import array

from src.typeclass import Function


class Dialate(Function):
    def __init__(self, a):
        self.a = a

    def __call__(self, data: array):
        return self.a * data
