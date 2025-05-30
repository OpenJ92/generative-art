from src.typeclass import Function
from numpy import array

class Add(Function):
    def __init__(self, A: Function, B: Function):
        self.A = A
        self.B = B

    def __call__(self, x: array):
        return self.A(x) + self.B(x)
