from src.helpers.zipapply import ZipApply
from src.functions.parallelogram import Parallelogram
from src.functions.composition import Composition
from src.functions.translate import Translate
from src.functions.copy import Copy

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
