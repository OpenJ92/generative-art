from src.typeclass import Function
from numpy import array, diag


class Scale(Function):
    def __init__(self, scale):
        self.scale = scale

    def __call__(self, data: array):
        return self.scale * data
