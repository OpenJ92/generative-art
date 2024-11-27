from src.typeclass.__function__ import Function


class AccumulateOnto(Function):
    def __init__(self, acc, scale):
        self.acc = acc
        self.scale = scale
        ## This should be tied to acc. Look to decouple

    def __call__(self, ts):
        value = ts + self.scale * self.acc(ts)
        return value
