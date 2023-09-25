from src.functions import ZipApply, Parallelogram, Composition, Translate, Copy

from src.typeclass.__sculpture__ import __Sculpture__


def Stack(sculpture, paralellogram, translate, times):
    sculptures = __Sculpture__(sculpture.sculpt(), Copy(times)).sculpt()
    funcs = []
    for time in range(times):
        funcs = [
            *funcs,
            Composition(
                [Parallelogram(paralellogram), Translate((time / times) * translate)]
            ),
        ]
    return __Sculpture__(sculptures, ZipApply(funcs))
