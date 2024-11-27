from src.functions import ZipApply, Scale, Translate, Composition, Copy

from src.atoms import dimension

from src.typeclass.sculpture import Sculpture

from numpy import array


def Concentric(sculpture, count):
    sculpture = sculpture.sculpt()
    dim = dimension(sculpture)

    funcs = []
    for comp in range(count + 1):
        funcs = [
            Composition(
                [
                    Scale(comp / count),
                    Translate(array([1 - comp / (2 * count) for _ in range(dim)])),
                ]
            ),
            *funcs,
        ]
    return Sculpture(
        Sculpture(sculpture, Copy(count)).sculpt(), ZipApply(funcs)
    )
