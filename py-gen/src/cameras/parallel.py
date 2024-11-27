from src.typeclass.__function__ import Function

from numpy import array


class Parallel(Function):
    def __init__(self, view: array):
        self.view = view

    def __call__(self, data: array):
        pass
