from src.typeclass import Function

class Max(Function):
    def __init__(self, axis):
        self.axis = axis

    def __call__(self, data):
        return data

    def call_data(self, data):
        match data:
            case Point(l=x):
                return x[self.axis]
            case Segment(l=l, m=m):
                return Point(max(self.call_data(l), self.call_data(m)))
            case Triangle(l=l, m=m, n=n):
                return Point(max(self.call_data(l), self.call_data(m), self.call_data(n)))
            case List(elements=elements):
                return Point(max(list(map(lambda x: self.call_data(x), elements))))
            case SegmentStrip(points=points):
                return Point(max(list(map(lambda x: self.call_data(x), points))))
            case Meta_Data(meta, data):
                return Point(self.call_data(data))

