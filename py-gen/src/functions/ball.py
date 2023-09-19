from src.functions.sphere import Sphere
from src.typeclass.__function__ import __Function__


class Ball(__Function__):
    def __call__(self, ts):
        t, *ts = ts
        return t * Sphere()(ts)
