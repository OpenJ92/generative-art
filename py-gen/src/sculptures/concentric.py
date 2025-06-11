from src.functions import Scale, Translate, Composition, Copy
from src.functions.zipapply import ZipApply
from src.functions.min import Min
from src.functions.max import Max
from src.atoms import dimension
from src.executors import Sculpture

from numpy import array


def Concentric(data, count):
    data = data.sculpt()
    dim = dimension(data)
    if not dim:
        breakpoint()

    ## Hardcoded Bounding Box translates
    center = []
    for index in range(dim):
        min = Min(index).call_data(data)
        max = Max(index).call_data(data)
        center.append((min + max) / 2)
    center = array(center)

    funcs = []
    for comp in range(count + 1):
        transform = Composition([Translate(-center), Scale(comp/count), Translate(center)])
        funcs.append(transform)

    return Sculpture(data,  Composition([Copy(count), ZipApply(funcs)]))
