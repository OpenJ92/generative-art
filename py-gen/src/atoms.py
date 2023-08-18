from __future__ import annotations
from dataclasses import dataclass
from typing import List
from numpy import array, zeros, diag

from src.typeclass.__composite__ import __Composite__

class Point:
    def __init__(self, l):
        self.l: array = l
        self.embeded_dimension = l.size
        self.intrinsic_dimension = 0

    def __add__(self, x):
        if not isinstance(x, Point): raise NotImplementedError(f"Sum of {self} and {x} not defined")
        match x:
            case Point(l=l):
                return Point(self.l + l)


class Segment:
    def __init__(self, l, m):
        self.l: array = l
        self.m: array = m
        self.embeded_dimension = l.size
        self.intrinsic_dimension = 1

    def __add__(self, x):
        if not isinstance(x, Segment): raise NotImplementedError(f"Sum of {self} and {x} not defined")
        match x:
            case Segment(l=l, m=m):
                return Segment(self.l + l, self.m + m)



# make assertions that all arrays are of equal size or make it 
# so we store the triangle as a matrix...
class Triangle:
    def __init__(self, l, m, n):
        self.l: array = l
        self.m: array = m
        self.n: array = n
        self.embeded_dimension = l.size
        self.intrinsic_dimension = 2

    def __add__(self, x):
        if not isinstance(x, Triangle): raise NotImplementedError(f"Sum of {self} and {x} not defined")
        match x:
            case Triangle(l=l, m=m, n=n):
                return Triangle(self.l + l, self.m + m, self.n + n)


Atomic = Point | Segment | Triangle

class SegmentStrip():
    def __init__(self):
        # Were looking to make the strip class if __Data__ in order to minimize
        # time to computation. Typical functions will be called as a map over the
        # set of points. The relationships between points will be stored in dictionaries
        # to be consturcted into segments at the appropriate times. In effect, they're not
        # drawable. Drawable needs to convert Strips into the appropriate List form to be
        # drawn. Perhaps not. I think I remember that there may be polygon/line forms
        # that allow us to go directly to svg.
        points = list()
        relations = defaultdict(list)

class List():
    ## We need to figure how to derive dimension
    def __init__(self, elements):
        self.elements = elements

class TriangleStrip():
    pass

class TriangleFan():
    pass

class PatchList():
    pass

Composite = SegmentStrip | TriangleFan | TriangleStrip | PatchList | List

@dataclass
class __Meta_Data__():
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
        case List(elements=elements):
            if len(elements) == 0:
                raise NotImplementedError
            return dimension(elements[0])
        case __Meta_Data__(meta, data):
            return dimension(data)

## Ultimately, this function should only work on 2D data. That is to say that after
## carrying out the sculpture and take our 'photo', the data is in the proper configuration
## to draw.
def draw(data: __Data__) -> str:
    if dimension(data) != 2:
        raise NotImplementedError
    match data:
            case Point(l=l):
                x0, y0 = l
                return f'<circle cx="{x0}" cy="{y0}" r="5"/>\n'
            case Segment(l=l, m=m):
                x0, y0 = l
                x1, y1 = m
                return f'<polyline points="{x0},{y0} {x1},{y1}" />\n'
            case Triangle(l=l, m=m, n=n):
                x0, y0,  = l
                x1, y1,  = m
                x2, y2,  = n
                return f'<polygon points="{x0},{y0} {x1},{y1} {x2},{y2} {x0},{y0}" />\n'
            case List(elements=elements):
                return "".join(list(map(draw, elements)))
            case __Meta_Data__(meta, data):
                return draw(data)

def wrap(work: str) -> str:
    header = "<svg width=\"297mm\" height=\"210mm\" viewBox=\"0 0 297 210\" xmlns=\"http://www.w3.org/2000/svg\">\n"
    footer = "</svg>"
    return header + work + footer

def write_to_file(name, obj):
    with open(name, 'x') as file:
        file.write(obj)
