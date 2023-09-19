from src.typeclass.__function__ import __Function__

from numpy import array, diag


class Scale(__Function__):
    def __init__(self, scale):
        self.scale = scale

    def __call__(self, data: array):
        return self.scale * data
