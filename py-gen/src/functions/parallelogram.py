from numpy import array
from src.typeclass import Function

class Parallelogram(Function):
    def __init__(self, A):
        self.A = A

    def __call__(self, data: array):
        try:
            return self.A @ data
        except Exception as e:
            breakpoint()
