from src.typeclass import Function
from src.atoms import Point, Segment, Segment, Triangle, List, SegmentStrip, Meta_Data, Empty
from math import inf

class Max(Function):
    def __init__(self, axis):
        self.axis = axis

    def __call__(self, data):
        return data

    def call_data(self, data):
        match data:
            case Empty():
                return -inf
            case Point(l=x):
                return x[self.axis]
            case Segment(l=l, m=m):
                return max(l[self.axis], m[self.axis])
            case Triangle(l=l, m=m, n=n):
                return max(l[self.axis], m[self.axis], n[self.axis])
            case List(elements=elements):
                return max(list(map(lambda x: self.call_data(x), elements)))
            case SegmentStrip(points=points):
                return max(list(map(lambda x: self.call_data(x), points)))
            case Meta_Data(meta, data):
                return self.call_data(data)

