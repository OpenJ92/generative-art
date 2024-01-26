from src.functions.parallelogram import Parallelogram
from src.functions.bezier import Bezier
from src.functions.sphere import Sphere
from src.functions.dialate import Dialate
from src.functions.translate import Translate
from src.functions.composition import Composition
from src.functions.copy import Copy
from src.functions.hypercube import HyperCube
from src.functions.id import ID
from src.functions.ball import Ball
from src.functions.perlin_noise import Perlin_Noise, Perlin_Stack, Perlin_Vector
from src.functions.accumulateonto import AccumulateOnto
from src.functions.barycentric import Barycentric
from src.functions.scale import Scale

from src.typeclass.__function__ import __Function__
from src.typeclass.__sculpture__ import __Sculpture__
from src.atoms import __Data__, List

from numpy import array, einsum, ones, zeros
from itertools import product
from collections import defaultdict


## Here we can have functions that manipulate functions. Move Composition, Repeat, etc


class Concat(__Function__):
    def __init__(self, A: __Function__, B: __Function__):
        self.A = A
        self.B = B

    def __call__(self, x: array):
        return x

    def __call_data__(self, x: __Data__):
        return array(*self.A.__call_data__(x), *self.B.__call_data__(x))


class Add(__Function__):
    def __init__(self, A: __Function__, B: __Function__):
        self.A = A
        self.B = B

    def __call__(self, x: array):
        return self.A(x) + self.B(x)


## Perhaps this shouldn't be a product of functions, but a product of Sculptures...
## What does that even mean? 
class Multiply(__Function__):
    def __init__(self, A: __Function__, B: __Function__):
        self.A = A
        self.B = B

    def __call__(self, x: array, y: array):
        outer = einsum("i, j", self.A(x), self.B(y))
        output_size = sum(outer.shape) - 1
        output = zeros(output_size)
        ranges = product(*list(map(lambda x: range(x), outer.shape)))
        for i, j in ranges:
            output[i + j] += outer[i][j]
        return output


class ZipApply(__Function__):
    def __init__(self, funcs):
        self.funcs = funcs

    def __call__(self, data: array):
        return data

    def __call_data__(self, data: __Data__) -> __Data__:
        match data:
            case List(elements=elements):
                applied = []
                for element, func in zip(elements, self.funcs):
                    applied = [*applied, __Sculpture__(element, func).sculpt()]
                return List(applied)
            case _:
                raise NotImplementedError
