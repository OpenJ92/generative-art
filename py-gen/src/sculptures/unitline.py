from src.functions import ZipApply, Copy, Scale, Translate, Composition, ID
from src.atoms import Segment, List, SegmentStrip
from src.typeclass import Sculpture

from numpy import array, diag, linspace


def UnitLine(nx):
    funcs = []
    for x in range(nx):
        funcs = [*funcs, Composition([Scale(1 / nx), Translate(array([x / nx]))])]

    return Sculpture(
        Sculpture(Segment(array([0]), array([1])), Copy(nx)).sculpt(),
        ZipApply(funcs),
    )


# There are no repeated points in this form as it's piped though Function machines
def UnitStrip(n):
    return Sculpture(
        SegmentStrip.from_itterable(linspace(0, 1, num=n, endpoint=True).reshape(n, 1)),
        ID(),
    )
