from src.typeclass.function import Function

from numpy import array


class ID(Function):
    def __call__(self, data: array):
        return data
