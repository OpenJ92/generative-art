from numpy import array

from src.typeclass.__function__ import __Function__

class Parallelogram(__Function__):
    def __init__(self, A):
        self.A = A

    def __call__(self, data: array):
        return self.A @ data
