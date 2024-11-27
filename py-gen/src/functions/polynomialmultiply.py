from numpy import array, einsum, ones
from itertools import product

from src.typeclass.function import Function

class PolynomialMultiply(Function):
    def __init__(self, other: array):
        self.other = other

    def __call__(self, t: array):
        outer = einsum("i, j", t, self.other)
        t_shape = t.shape[0]
        other_shape = self.other.shape[0]
        indices = product(range(t_shape), range(other_shape))
        output = ones(t_shape + other_shape, )

        for i, j in indices:
            output[i + j] += outer[i, j]

        return output

