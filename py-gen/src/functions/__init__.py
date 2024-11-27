from src.typeclass import Function, Sculpture
from src.atoms import Data, List

from numpy import array, einsum, ones, zeros
from itertools import product
from collections import defaultdict

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


## Here we can have functions that manipulate functions. Move Composition, Repeat, etc


class Concat(Function):
    def __init__(self, A: Function, B: Function):
        self.A = A
        self.B = B

    def __call__(self, x: array):
        return x

    def call_data(self, x: Data):
        return array(*self.A.call_data(x), *self.B.call_data(x))


class Add(Function):
    def __init__(self, A: Function, B: Function):
        self.A = A
        self.B = B

    def __call__(self, x: array):
        return self.A(x) + self.B(x)


## Perhaps this shouldn't be a product of functions, but a product of Sculptures...
## What does that even mean? 
class Multiply(Function):
    def __init__(self, A: Function, B: Function):
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


class ZipApply(Function):
    def __init__(self, funcs):
        self.funcs = funcs

    def __call__(self, data: array):
        return data

    def call_data(self, data: Data) -> Data:
        match data:
            case List(elements=elements):
                applied = []
                for element, func in zip(elements, self.funcs):
                    applied = [*applied, Sculpture(element, func).sculpt()]
                return List(applied)
            case _:
                raise NotImplementedError

class Map(Function):
    def __init__(self, func):
        self.func = func

    def __call__(self, data: array):
        return data

    def call_data(self, data: Data):
        match data:
            case List(elements=elements):
                applied = []
                for element in elements:
                    applied.append(Sculpture(element, self.func).sculpt())
                return List(applied)
            case _:
                raise NotImplementedError
