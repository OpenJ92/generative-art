from src.typeclass.__sculpture__ import __Sculpture__
from src.functions.id import ID
from src.functions.hypercube import HyperCube
from src.atoms import List, Segment, Triangle, Point

from numpy import array

def __Square__(atom):
    return __Sculpture__(__Sculpture__(atom, ID()).sculpt(), HyperCube()(2))

def __Cube__(atom):
    return __Sculpture__(__Sculpture__(atom, ID()).sculpt(), HyperCube()(3))

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
    return __Sculpture__(Square(atomcls).sculpt(), HyperCube()(n))

