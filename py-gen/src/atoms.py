from __future__ import annotations
from dataclasses import dataclass
from numpy import array, zeros, diag, stack

from src.typeclass.__composite__ import __Composite__


class Point:
    def __init__(self, l):
        self.l: array = l
        self.embeded_dimension = l.size
        self.intrinsic_dimension = 0


class Segment:
    def __init__(self, l, m):
        self.l: array = l
        self.m: array = m
        self.embeded_dimension = l.size
        self.intrinsic_dimension = 1


# make assertions that all arrays are of equal size or make it
# so we store the triangle as a matrix...
class Triangle:
    def __init__(self, l, m, n):
        self.l: array = l
        self.m: array = m
        self.n: array = n
        self.embeded_dimension = l.size
        self.intrinsic_dimension = 2


Atomic = Point | Segment | Triangle


class SegmentStrip:
    @classmethod
    def from_itterable(cls, ittr):
        return cls(list(map(lambda arr: Point(arr), ittr)))

    def __init__(self, points):
        self.points = points

    def extract_to_array(self):
        return stack([point.l for point in self.points])



class List:
    ## We need to figure how to derive dimension
    def __init__(self, elements):
        self.elements = elements


class TriangleStrip:
    pass


class TriangleFan:
    pass


class PatchList:
    pass


Composite = SegmentStrip | TriangleFan | TriangleStrip | PatchList | List


@dataclass
class __Meta_Data__:
    meta: dict
    data: __Data__


__Data__ = Atomic | Composite | __Meta_Data__


def dimension(data: __Data__):
    match data:
        case Point(l=l):
            return l.size
        case Segment(l=l, m=m):
            return l.size
        case Triangle(l=l, m=m, n=n):
            return l.size
        case List(elements=[element, *_]):
            return dimension(element)
        case List(elements=_):
            raise NotImplementedError
        case SegmentStrip(points=[Point(l=l), *_]):
            return dimension(Point(l))
        case SegmentStrip(points=_):
            raise NotImplementedError
        case __Meta_Data__(meta, data):
            return dimension(data)

## Rudimentary Parser. Applicative Functor Parser in python?
color = {0:"black", 1:"red", 2:"blue", 3:"green"}
def parse_meta(meta: dict):
    elements = []
    for key, value in meta.items():
        elements.append(f"{key}=\"{color[value]}\"")
    return "".join(elements)

def apply_construct(applied):
    def f(meta):
        for index in range(len(applied)):
            applied[index] = applied[index](meta)
        return applied
    return f

## Ultimately, this function should only work on 2D data. That is to say that after
## carrying out the sculpture and take our 'photo', the data is in the proper configuration
## to draw_helper.
def draw_helper(data: __Data__) -> str:
    if dimension(data) != 2:
        raise NotImplementedError
    match data:
        case Point(l=l):
            x0, y0 = l
            return lambda meta: \
                    f'<circle cx="{x0}" cy="{y0}" r="5" {meta}/>\n'

        case Segment(l=l, m=m):
            x0, y0 = l; x1, y1 = m
            return lambda meta: \
                    f'<polyline points="{x0},{y0} {x1},{y1}" {meta}/>\n'

        case Triangle(l=l, m=m, n=n):
            x0, y0 = l; x1, y1 = m; x2, y2 = n
            return lambda meta: \
                    f'<polygon points="{x0},{y0} {x1},{y1} {x2},{y2} {x0},{y0}" {meta}/>\n'

        case List(elements=elements):
            applied = []
            for element in elements:
                applied.append(draw_helper(element))
            return lambda meta: "".join(apply_construct(applied)(meta))

        case SegmentStrip(points=points):

            def f(points):
                match points:
                    case (Point(l=l1), Point(l=l2)):
                        return Segment(l1, l2)
                    case _:
                        raise NotImplementedError

            applied = []
            for point, pojnt in zip(points, points[1:]):
                applied.append(draw_helper(f((point, pojnt))))

            return lambda meta: "".join(apply_construct(applied)(meta))

        case __Meta_Data__(meta=m, data=da):
            return lambda _: draw_helper(da)(parse_meta(m))

def draw(data):
    return draw_helper(data)("")


def wrap(work: str) -> str:
    header = '<svg width="297mm" height="210mm" viewBox="0 0 297 210" \
              xmlns="http://www.w3.org/2000/svg">\n'
    footer = "</svg>"
    return header + work + footer


def write_to_file(name, obj):
    with open(name, "x") as file:
        file.write(obj)
