from src.functions.scale import Scale
from src.functions.translate import Translate
from src.functions.composition import Composition
from src.functions.copy import Repeat

from src.helpers.zipapply import ZipApply

from src.atoms import dimension

from src.typeclass.__sculpture__ import __Sculpture__

from numpy import array

def Concentric(sculpture, count):
    sculpture = sculpture.sculpt()
    dim = dimension(sculpture)

    funcs = []
    for comp in range(count + 1):
        funcs = [ Composition([Scale(comp/count)
                              ,Translate(array([1 - comp/count for _ in range(dim)]))
                              ])
                , *funcs
                ]
    return __Sculpture__(__Sculpture__(sculpture, Repeat(count)).sculpt(), ZipApply(funcs))
