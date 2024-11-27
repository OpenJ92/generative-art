from src.functions import ZipApply, Parallelogram, Composition, Translate, Copy

from src.typeclass.sculpture import Sculpture


def Stack(sculpture, paralellogram, translate, times):
    sculptures = Sculpture(sculpture.sculpt(), Copy(times)).sculpt()
    funcs = []
    for time in range(times):
        funcs = [
            *funcs,
            Composition(
                [Parallelogram(paralellogram), Translate((time / times) * translate)]
            ),
        ]
    return Sculpture(sculptures, ZipApply(funcs))
