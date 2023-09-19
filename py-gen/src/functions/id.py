from src.typeclass.__function__ import __Function__

from numpy import array


class ID(__Function__):
    def __call__(self, data: array):
        return data
