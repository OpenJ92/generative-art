from src.functions import Parallelogram, Composition, Translate, Copy
from src.functions.zipapply import ZipApply

from src.executors import Sculpture


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
