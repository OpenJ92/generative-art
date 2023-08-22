from src.functions.scale import Scale
from src.functions.translate import Translate
from src.functions.composition import Composition
from src.helpers.zipapply import ZipApply
from src.functions.copy import Copy
from src.atoms import Segment, List

from numpy import array, diag

def UnitLine(nx):
    funcs = []
    for x in range(nx):
        funcs = [ *funcs
                 , Composition([ Scale(1/nx)
                               , Translate(array([x/nx]))
                               ])
                ]

    return __Sculpture__(__Sculpture__(Segment(array([0]), array([1])), Copy(nx)).sculpt(), ZipApply(funcs))
