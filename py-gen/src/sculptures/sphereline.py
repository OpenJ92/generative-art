from src.typeclass.__sculpture__ import __Sculpture__

from src.functions import Sphere, Bezier, Composition, Translate, Scale, Add, ID, Parallelogram
from src.atoms import Point
from src.helpers.numpy import make_closed_LNE
from src.sculptures import FlexPlane, UnitStrip
from src.helpers.numpy import make_closed_LNE

from numpy import array, concatenate, linspace, stack, diag
from numpy.random import rand, randint
from math import pi

def Sphere_Line(depth):
    ## Sphere: Make curve that wraps around n spheres and sum. Sample
    ## function for k points for first element in control points in Join
    sphere = ID()
    for level in range(depth):
        control_points = make_closed_LNE(rand(randint(2, 50), 2), 0, .25)
        bezier = Composition([ Sphere()
                             , Scale(4)
                             , Parallelogram([[0,4*pi],[0,8*pi]])
                             , Bezier()(control_points, [0])
                             ][::-1])
        sphere = Add(sphere, bezier)

    sphere_samples = __Sculpture__(UnitStrip(30).sculpt(), sphere).sculpt().extract_to_array()

    ## Line: Make curve from two samples from largest sphere from above.
    ## Sample line for k points for the second element in control points
    ## in Join

    ## point = Composition([Scale(4), Sphere()][::-1])
    ## start = .5 * __Sculpture__(Point(rand(2)), point).sculpt().l
    ## end   = -start

    start = sphere([0])
    end   = sphere([1])

    line = Composition([ Translate(start)
                       , Parallelogram(diag(end - start))
                       , Parallelogram(array([1,1,1]).reshape(3, 1))
                       ][::-1])
    line_samples = __Sculpture__(UnitStrip(30).sculpt(), line).sculpt().extract_to_array()

    ## Join: Stack matrices from above and supply to Bezier. Submit FlexPlane
    ## and Bezier to __Sculpture__ and return.
    sphereline = Bezier()(stack([line_samples, sphere_samples]), [0, 1])
    return lambda data: __Sculpture__(data, sphereline)
