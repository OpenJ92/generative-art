from src.typeclass.__sculpture__ import __Sculpture__
from src.functions.parallelogram import Parallelogram
from src.functions.translate import Translate
from src.functions.composition import Composition
from src.helpers.zipapply import ZipApply
from src.sculptures.unitcube import Square, HyperCube
from src.functions.copy import Copy

from numpy import array, diag
from itertools import product

# Can't this be extended to any dimension? Consider generalizing this.
# Make FlexCube with three parameters and HCube(3)
def FlexPlane(sculpture, nx, ny):
    funcs = []
    for x, y in product(range(nx), range(ny)):
        funcs = [ *funcs
                , Composition([ Parallelogram(diag(array([1/nx, 1/ny])))
                              , Translate(array([x/nx,y/ny]))
                              ])
                ]

    return __Sculpture__(__Sculpture__(sculpture.sculpt(), Copy(nx*ny)).sculpt(), ZipApply(funcs))

def FlexCube(atomcls, nx, ny):
    return __Sculpture__(FlexPlane(Square(atomcls), nx,ny).sculpt(), HyperCube()(3))

def FlexHyperCube(atomcls, n, nx, ny):
    return __Sculpture__(FlexCube(Square(atomcls), nx, ny).sculpt(), HyperCube()(n))
