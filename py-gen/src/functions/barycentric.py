from numpy import array_split, squeeze, square

from src.typeclass.__function__ import __Function__
from src.functions.sphere import Sphere


class Barycentric(__Function__):
    def __init__(self, points):
        self.points = points

    def __call__(self, ts):
        axis = 0
        ts = square(Sphere()(ts))
        points = array_split(self.points, self.points.shape[axis], axis)
        lincomb = sum([t * point for t, point in zip(ts, points)])
        return squeeze(lincomb)
