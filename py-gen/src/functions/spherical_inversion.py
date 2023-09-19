from numpy import array, square

from src.typeclass.__function__ import __Function__
from src.typeclass.__random__ import __Random__


class SphereInversion(__Random__, __Function__):
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    def __call__(self, data: array):
        diff = data - self.center
        length_diff = sum(square(diff))
        return self.center + (self.radius**2 * (diff / length_diff))

    @classmethod
    def random(self):
        raise NotImplementedError
