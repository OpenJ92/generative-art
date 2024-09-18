from src.typeclass.__sculpture__ import __Sculpture__
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

    return __Sculpture__(
        __Sculpture__(sculpture.sculpt(), Copy(nx * ny)).sculpt(), ZipApply(funcs)
    )


def FlexCube(atomcls, nx, ny):
    return __Sculpture__(FlexPlane(Square(atomcls), nx, ny).sculpt(), HyperCube()(3))


def FlexHyperCube(atomcls, n, nx, ny):
    return __Sculpture__(FlexCube(Square(atomcls), nx, ny).sculpt(), HyperCube()(n))
