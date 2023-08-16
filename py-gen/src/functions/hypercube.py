from src.typeclass.__sculpture__ import __Sculpture__
from src.typeclass.__composite__ import __Composite__
from src.typeclass.__function__ import __Function__
from src.functions.parallelogram import Parallelogram
from src.functions.translate import Translate
from src.functions.composition import Composition
from src.functions.id import ID
from src.atoms import __Data__, dimension, List, Segment, Triangle, Point

from numpy import eye, take, array
from itertools import combinations
from enum import Enum

## I think we need to reconstruct this as a function that produces
## either the NORM or BEZIER class. Working at the instance level here
## doesn't make much sense to me here. 
class Mode(Enum):
    NORM = 0
    BEZIER = 1

def pnpdispatch(mode):
    match mode:
        case Mode.NORM: return pnpNorm
        case Mode.BEZIER: return pnpBez

def pnpNorm(data, dim, hcdim):
    planes = list(combinations(range(hcdim), dimension(data)))
    notplanes = [tuple(k for k in range(hcdim) if k not in plane) for plane in planes]
    return planes, notplanes

def pnpBez(data, dim, hcdim):
    planes, notplanes = self.pnpNorm(data, dim, hcdim)
    return planes[:1], notplanes[:1]

def HyperCube(mode = Mode.NORM):
    class hypercube(__Function__):
        def __init__(self, N):
            self.N = N
            self.mode = mode

        def __call__(self, data: array):
            return data

        def __call_data__(self, data: __Data__):
            dimdata = dimension(data)
            if self.N == dimdata:
                return data
            if self.N >= dimdata:
                data = __Sculpture__(data, hypercube(self.N-1)).sculpt()

            directions = eye(self.N)
            planes, notplanes = hypercube.pnp(data, dimdata, self.N)

            funcs = []
            for parallelogram, translations in zip(planes, notplanes):
                para = Parallelogram(take(directions, parallelogram, axis=0).T)
                translates = map(Translate, take(directions, translations, axis=0))
                funcs = [ *funcs, para, *[Composition([para, t]) for t in translates]]

            comp = []
            for f in funcs:
                comp = [ *comp, __Sculpture__(data, f).sculpt() ]

            return List(comp)

    hypercube.pnp = pnpdispatch(mode)
    return hypercube
