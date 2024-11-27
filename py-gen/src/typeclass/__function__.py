from abc import ABC, abstractmethod
from numpy import array

from src.atoms import (
    Point,
    Segment,
    SegmentStrip,
    Triangle,
    Composite,
    __Data__,
    __Meta_Data__,
    List,
)


class Function(ABC):
    @abstractmethod
    def __call__(self, data: array) -> array:
        pass

    def __call_data__(self, data: __Data__) -> __Data__:
        match data:
            case Point(l=x):
                return Point(self.__call__(x))
            case Segment(l=l, m=m):
                return Segment(self.__call__(l), self.__call__(m))
            case Triangle(l=l, m=m, n=n):
                return Triangle(self.__call__(l), self.__call__(m), self.__call__(n))
            case List(elements=elements):
                return List(list(map(lambda x: self.__call_data__(x), elements)))
            case SegmentStrip(points=points):
                return SegmentStrip(list(map(lambda x: self.__call_data__(x), points)))
            case __Meta_Data__(meta, data):
                return __Meta_Data__(meta, self.__call_data__(data))
