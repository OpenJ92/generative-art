from src.typeclass.sculpture import Sculpture
from src.functions import ZipApply, Parallelogram, Translate, Composition
from src.sculptures.unitcube import Square, HyperCube
from src.functions.copy import Copy

from numpy import array, diag
from itertools import product


def FlexPlane(sculpture, nx, ny):
    funcs = []
    for x, y in product(range(nx), range(ny)):
        funcs.append(
            Composition( [
                    Parallelogram(diag(array([1 / nx, 1 / ny]))),
                    Translate(array([x / nx, y / ny])), ]
            ),
        )

    return Sculpture(
        Sculpture(sculpture.sculpt(), Copy(nx * ny)).sculpt(), ZipApply(funcs)
    )


def FlexCube(atomcls, nx, ny):
    return Sculpture(FlexPlane(Square(atomcls), nx, ny).sculpt(), HyperCube()(3))


def FlexHyperCube(atomcls, n, nx, ny):
    return Sculpture(FlexCube(Square(atomcls), nx, ny).sculpt(), HyperCube()(n))
