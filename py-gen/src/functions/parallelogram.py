from numpy import array

from src.typeclass.__function__ import Function

class Parallelogram(Function):
    def __init__(self, A):
        self.A = A

    def __call__(self, data: array):
        return self.A @ data
