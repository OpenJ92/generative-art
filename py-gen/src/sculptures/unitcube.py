from src.typeclass.sculpture import Sculpture
from src.functions import ID, HyperCube
from src.sculptures.unitline import UnitLine, UnitStrip
from src.atoms import List, Segment, Triangle, Point

from numpy import array


def __Square__(atom):
    return Sculpture(__Sculpture__(atom, ID()).sculpt(), HyperCube()(2))


def __Cube__(atom):
    return Sculpture(__Sculpture__(atom, ID()).sculpt(), HyperCube()(3))


def PointSquare():
    return __Square__(List([Point(array([0])), Point(array([1]))]))


def SegmentSquare():
    return __Square__(Segment(array([0]), array([1])))


def TriangleSquare():
    return __Square__(
        List(
            [
                Triangle(array([0, 0]), array([1, 0]), array([0, 1])),
                Triangle(array([0, 1]), array([1, 0]), array([1, 1])),
            ]
        )
    )


def Square(atomcls):
    match atomcls.__qualname__:
        case Point.__qualname__:
            return PointSquare()
        case Segment.__qualname__:
            return SegmentSquare()
        case Triangle.__qualname__:
            return TriangleSquare()


def Cube(atomcls):
    return __Cube__(Square(atomcls).sculpt())


def HCube(atomcls, n):
    return Sculpture(Square(atomcls).sculpt(), HyperCube()(n))


def FlexSquare(n):
    return Sculpture(UnitStrip(n).sculpt(), HyperCube()(2))
