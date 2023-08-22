from src.typeclass.__function__ import __Function__

from math import sin, cos
from numpy import hstack, array

class Sphere(__Function__):
    def __call__(self, ts):
        return self.recursive_call(array([1]), ts)

    def recursive_call(self, arr, ts: array):
        t, *ts = ts
        arr = hstack((cos(t)*arr, sin(t)))
        if ts: return self.recursive_call(arr, ts)
        else : return arr

