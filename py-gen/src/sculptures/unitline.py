from src.functions.scale import Scale
from src.functions.translate import Translate
from src.functions.composition import Composition
from src.functions.id import ID
from src.helpers.zipapply import ZipApply
from src.functions.copy import Copy
from src.atoms import Segment, List, SegmentStrip
from src.typeclass.__sculpture__ import __Sculpture__

from numpy import array, diag, linspace

def UnitLine(nx):
    funcs = []
    for x in range(nx):
        funcs = [ *funcs
                 , Composition([ Scale(1/nx)
                               , Translate(array([x/nx]))
                               ])
                ]

    return __Sculpture__(__Sculpture__(Segment(array([0]), array([1])), Copy(nx)).sculpt(), ZipApply(funcs))

# There are no repeated points in this form as it's piped though __Function__ machines
def UnitStrip(n):
    return __Sculpture__(SegmentStrip.from_itterable(linspace(0, 1, num=n, endpoint=True).reshape(n,1)), ID())

