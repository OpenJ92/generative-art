from src.typeclass.__function__ import __Function__
from src.atoms import __Data__

from numpy import array


class Add(__Function__):
    def __init__(self, A: __Function__, B: __Function__):
        self.A = A
        self.B = B

    def __call__(self, x: array):
        return x

    def __call_data__(self, x: __Data__):
        return self.A.__call_data__(x) + self.B.__call_data__(x)
