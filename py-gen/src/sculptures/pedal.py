from src.typeclass import Sculpture
from src.functions import Bezier, Composition, Parallelogram, Scale, Translate, ZipApply, Ball
from src.sculptures import UnitStrip

from numpy import array, concatenate, linspace, stack, flip
from numpy.random import rand, randint, seed
from math import pi

def Linear_Pedal(start, end, degree, stem_end, _seed):
    ## Assumed Coordinate system (r, theta, phi)
    start = array([0, 1, 0]).reshape((3,1)) * 2 * start
    end   = array([1, 0, 0]).reshape((3,1)) * 1 * end

    seed(_seed)

    ## _base = rand(3, degree)
    samples = rand(3, degree)
    ## base = Sculpture(UnitStrip(degree).sculpt(), Bezier()(_base, [1]))
    ## samples = base.sculpt().extract_to_array().T

    _outer_pedal_right = concatenate([start, samples, end], axis=1).T \
                       @ array([[1, 0,0]
                               ,[0,.5,0]
                               ,[0, 0,1]])
    _outer_pedal_left  = flip(_outer_pedal_right, 0) \
                       @ array([[1, 0,0]
                               ,[0,-1,0]
                               ,[0, 0,1]])


    stem = Composition([Parallelogram(array([[1],[0],[0]])), Scale(stem_end)])
    _inner_pedal_right = Sculpture(UnitStrip(degree+2).sculpt(), stem) \
                                     .sculpt() \
                                     .extract_to_array()
    _inner_pedal_left = flip(_inner_pedal_right, 0)

    _inner_pedal = concatenate([_inner_pedal_right, _inner_pedal_left])
    _outer_pedal = concatenate([_outer_pedal_right, _outer_pedal_left])

    control_points = stack([_outer_pedal, _inner_pedal])
    return Bezier()(control_points, [0,1])

    ## Here is the base/hard coded 'stem' centered pedal. 'Floral' will produce
    ## k groups of n Pedals. We'll carry out a Linear_Squashing policy on each of
    ## of them and Translate them into position on the Sphere(3) domain. Remember
    ## to maintain P(R|L)([0,theta]) = [0, y, z]. 

def Floral(layers, deviation, _seed):
    seed(_seed)

    pedals = []
    for layer in range(layers):
        start, end = rand(), rand()
        stem = end * rand()

        ## Assumed Coordinate system (r, theta, phi)
        ## Basis pedal for current layer
        pedal = Linear_Pedal(start, end, randint(3, 20), stem, _seed)

        count = randint(5, 20)
        control, axes = pedal.control_points, pedal.collapse_axes
        for l in range(0, count):
            control_points = (deviation * rand(*control.shape)) + control
            phi, theta     = (pi * layer) / layers, (2 * pi * l) / count

            pedal     = Bezier()(control_points, axes)
            translate = Translate([0, theta, phi])
            squash    = Parallelogram([[1,0,0],[0,1,0],[0,0,1]])

            function  = Composition([pedal, squash, translate])
            pedals.append(function)

    return Composition([ZipApply(pedals), Ball()])

## Here we need to reconstruct the above so as to accept a Bezier Pedal like
## the one defined above. Notice that Linear_Pedal is a RealizedFunction
