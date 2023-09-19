from numpy import array

from src.typeclass.__function__ import __Function__


class Dialate(__Function__):
    def __init__(self, a):
        self.a = a

    def __call__(self, data: array):
        return self.a * data
