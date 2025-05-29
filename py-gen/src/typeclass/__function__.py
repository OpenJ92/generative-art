from abc import ABC, abstractmethod
from numpy import array

from src.atoms import (
    Empty,
    Point,
    Segment,
    SegmentStrip,
    Triangle,
    Composite,
    Data,
    Meta_Data,
    List,
)


class Function(ABC):
    @abstractmethod
    def __call__(self, data: array) -> array:
        ## Overwritten by user.
        pass

    def call_data(self, data: Data) -> Data:
        match data:
            case Empty:
                return Empty
            case Point(l=x):
                return Point(self.__call__(x))
            case Segment(l=l, m=m):
                return Segment(self.__call__(l), self.__call__(m))
            case Triangle(l=l, m=m, n=n):
                return Triangle(self.__call__(l), self.__call__(m), self.__call__(n))
            case List(elements=elements):
                return List(list(map(lambda x: self.call_data(x), elements)))
            case SegmentStrip(points=points):
                return SegmentStrip(list(map(lambda x: self.call_data(x), points)))
            case Meta_Data(meta, data):
                return Meta_Data(meta, self.call_data(data))
