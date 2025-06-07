from src.functions import Scale, Translate, Composition, Copy
from src.functions.zipapply import ZipApply
from src.atoms import dimension
from src.typeclass import Sculpture

from numpy import array


def Concentric(sculpture, count):
    sculpture = sculpture.sculpt()
    dim = dimension(sculpture)

    ## I'm understanding that this is an incorrect implementation. We need to supply
    ## a policy for finding the centroid of the object we're sculpting. With that
    ## we can carry out a Translate to the origin, carry out a Scale and finally
    ## Translate. *I think when I had constructed this, I only really considered 
    ## the computation with respect to a 'square'. This can be done to any object
    ## which has a computable centroid. 

    funcs = []
    for comp in range(count + 1):
        funcs = [
            Composition(
                [
                    Scale(comp / count),
                    Translate(array([1 - comp / (dim * count) for _ in range(dim)])),
                ]
            ),
            *funcs,
        ]
    return Sculpture(
        Sculpture(sculpture, Copy(count)).sculpt(), ZipApply(funcs)
    )
