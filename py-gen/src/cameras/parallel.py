from src.typeclass.__function__ import __Function__

from numpy import array

class Parallel(__Function__):
    def __init__(self, view: array):
        self.view = view

    def __call__(self, data: array):
        pass
