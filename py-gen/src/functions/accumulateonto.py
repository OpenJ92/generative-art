from src.typeclass import Function


class AccumulateOnto(Function):
    def __init__(self, acc, scale):
        self.acc = acc
        self.scale = scale
        ## This should be tied to acc. Look to decouple

    def __call__(self, ts):
        try:
            value = ts + self.scale * self.acc(ts)
        except Exception as e:
            breakpoint()
            return ts
        return value
