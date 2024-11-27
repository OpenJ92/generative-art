from src.typeclass.__function__ import Function

from math import sin, cos
from numpy import hstack, array, zeros


class Sphere(Function):
    def __call__(self, ts):
        return self.recursive_call(array([1]), ts)

    def recursive_call(self, arr, ts: array):
        t, *ts = ts
        arr = hstack((cos(t) * arr, sin(t)))
        if ts:
            return self.recursive_call(arr, ts)
        else:
            return arr


# class Sphere(Function, __Random__):
#     convert = {"C" : True, "S" : False}
#     fn      = {True : cos, False : sin}
# 
#     @classmethod
#     def _parse(cls, word):
#         pass
# 
#     def _validate_thetas(self, thetas):
#         return len(thetas) == self.size
# 
#     def __init__(self, word):
#         if not (self.information := Sphere._parse(word)):
#             raise ValueError
# 
#     def _evaluate(self, thetas):
#         output = zeros(self.information['size'])
#         output[information['init']] = 1
# 
#         information = [ thetas
#                       , self.information['policies']
#                       , self.information['locations']
#                       ]
# 
#         for theta, policy, location in zip(information):
#             output *= fn[policy](theta)
#             output[location] = fn[not policy](theta)
# 
#         return output
# 
#     def __call__(self, thetas):
#         if not self._validate_thetas(thetas):
#             raise ValueError
#         return self._evaluate(thetas)
