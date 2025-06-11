from src.executors import Sculpture
from src.typeclass import Function
from src.functions.parallelogram import Parallelogram
from src.functions.translate import Translate
from src.functions.composition import Composition
from src.atoms import Data, dimension, List, Segment, Triangle, Point

from numpy import eye, take, array
from itertools import combinations
from enum import Enum


class Mode(Enum):
    FULL = 0
    BEZIER = 1


def pnpdispatch(mode):
    match mode:
        case Mode.FULL:
            return pnpNorm
        case Mode.BEZIER:
            return pnpBez


def pnpNorm(data, dim, hcdim):
    planes = list(combinations(range(hcdim), dimension(data)))
    notplanes = [tuple(k for k in range(hcdim) if k not in plane) for plane in planes]
    return planes, notplanes


def pnpBez(data, dim, hcdim):
    planes, notplanes = pnpNorm(data, dim, hcdim)
    return planes[:1], notplanes[:1]


def HyperCube(mode=Mode.FULL):
    class hypercube(Function):
        def __init__(self, N):
            self.N = N
            self.mode = mode

        def __call__(self, data: array):
            return data

        def call_data(self, data: Data):
            dimdata = dimension(data)
            if self.N == dimdata:
                return data
            if self.N >= dimdata:
                data = Sculpture(data, hypercube(self.N - 1)).sculpt()

            directions = eye(self.N)
            planes, notplanes = hypercube.pnp(data, dimdata, self.N)

            funcs = []
            for parallelogram, translations in zip(planes, notplanes):
                para = Parallelogram(take(directions, parallelogram, axis=0).T)
                translates = map(Translate, take(directions, translations, axis=0))
                funcs = [*funcs, para, *[Composition([para, t]) for t in translates]]

            comp = []
            for f in funcs:
                comp = [*comp, Sculpture(data, f).sculpt()]

            return List(comp)

    hypercube.pnp = pnpdispatch(mode)
    return hypercube
