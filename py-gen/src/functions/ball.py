from src.functions.sphere import Sphere
from src.typeclass import Function


class Ball(Function):
    def __call__(self, ts):
        t, *ts = ts
        return t * Sphere()(ts)
