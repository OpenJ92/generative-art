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

class Mode(Enum):
    NORM = 0
    BEZIER = 1

class HyperCube(__Function__):
    MODE = Mode

    def __init__(self, N, mode=Mode.NORM):
        self.N = N
        self.mode = mode

    def __call__(self, data: array):
        return data

    def __call_data__(self, data: __Data__):
        dimdata = dimension(data)
        if self.N == dimdata:
            return data
        if self.N >= dimdata:
            data = __Sculpture__(data, HyperCube(self.N-1, mode=self.mode)).sculpt()

        directions = eye(self.N)
        planes, notplanes = self.pnpdispatch(data, dimdata)

        funcs = []
        for parallelogram, translations in zip(planes, notplanes):
            para = Parallelogram(take(directions, parallelogram, axis=0).T)
            translates = list(map(Translate, take(directions, translations, axis=0)))
            funcs = [ *funcs, para, *[Composition([para, t]) for t in translates]]

        comp = []
        for f in funcs:
            comp = [ *comp, __Sculpture__(data, f).sculpt() ]

        return List(comp)

    def pnpdispatch(self, data, dim):
        match self.mode:
            case HyperCube.MODE.NORM: return self.pnpNorm(data, dim)
            case HyperCube.MODE.BEZIER: return self.pnpBez(data, dim)

    def pnpNorm(self, data, dim):
        planes = list(combinations(range(self.N), dimension(data)))
        notplanes = [tuple(k for k in range(self.N) if k not in plane) for plane in planes]
        return planes, notplanes

    def pnpBez(self, data, dim):
        planes, notplanes = self.pnpNorm(data, dim)
        return planes[:1], notplanes[:1]



def __Square__(atom):
    return __Sculpture__(__Sculpture__(atom, ID()).sculpt(), HyperCube(2))

def __Cube__(atom):
    return __Sculpture__(__Sculpture__(atom, ID()).sculpt(), HyperCube(3))

def PointSquare():
    return __Square__(List([Point(array([0])), Point(array([1]))]))

def SegmentSquare():
    return __Square__(Segment(array([0]),array([1])))

def TriangleSquare():
    return __Square__(List([ Triangle(array([0,0]), array([1,0]), array([0,1]))
                           , Triangle(array([0,1]), array([1,0]), array([1,1]))]))
def Square(atomcls):
    match atomcls.__qualname__:
        case Point.__qualname__:    return PointSquare()
        case Segment.__qualname__:  return SegmentSquare()
        case Triangle.__qualname__: return TriangleSquare()


def Cube(atomcls):
    return __Cube__(Square(atomcls).sculpt())

def HCube(atomcls, n):
    return __Sculpture__(Square(atomcls).sculpt(), HyperCube(n))

