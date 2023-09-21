# __Data__, __Function__, __Camera__, __Light__

# Sculpture(__Data__, __Function__) -> Named functions
# Enviornment([[Sculpture, Position, CoordinateBasis], ...], __Light__)
# Enviornment(env_file?)

# Photograph(__Camera__, __Data__)
# Photograph(__Camera__, Sculpture(__Data__, __Function__))
# Photograph(__Camera__, Enviornment([[Sculpture, Position, CoordinateBasis], ...], __Light__))
# Video(__Camera__, Sculpture(__Data__, __Function__), __Update__, frames)
# Video(__Camera__, Enviornment([[Sculpture, Position, CoordinateBasis], ...], __Light__), __Update__, frames)
from numpy.random import rand, randint
from numpy import (
    array_split,
    concatenate,
    square,
    array,
    ones,
    multiply,
    tensordot,
    stack,
    einsum,
)
from numpy.random import rand, randint
from math import pi, sqrt

from src.functions import (
    Parallelogram,
    Bezier,
    Sphere,
    Dialate,
    Translate,
    Composition,
    ID,
    Ball,
    Perlin_Noise,
    Perlin_Stack,
    Perlin_Vector,
    Add,
    AccumulateOnto,
    Copy,
    Barycentric,
)
from src.sculptures import (
    FlexHyperCube,
    FlexCube,
    FlexPlane,
    UnitLine,
    Cube,
    Square,
    HCube,
    Concentric,
    FlexSquare,
    UnitStrip,
)
from src.atoms import Point, Segment, Triangle, draw, wrap, write_to_file, List
from src.helpers.numpy import *

from mp.pose_landmark_detection import Pose_Landmark_Detection
from src.typeclass.__sculpture__ import __Sculpture__

# Remember to do make the sculpture that makes a set of beziers that reduce order in order. Update each to upgrade
# to the max order. What's more, add multithreading to rendering processes. Functions may or may not be seperable
# into component pieces.


def U04():
    for k in range(10):
        A = rand(7, 3)
        B = rand(5, 3)
        print(k, A)

        line = UnitStrip(1500)
        squares = lambda k: __Sculpture__(
            Concentric(FlexSquare(50), 100).sculpt(),
            Composition(
                [
                    Parallelogram([[2 * pi, 0], [0, 1 * pi]]),
                    Translate([pi * (k / 20), pi * (k / 20)]),
                    Sphere(),
                    Parallelogram(array([[1, 0, 0], [0, 0, 1]])),
                ]
            ),
        ).sculpt()

        f = lambda A, line, noise, deformation: __Sculpture__(
            line.sculpt(),
            Composition(
                [
                    Composition(
                        [
                            Bezier()(A, [0]),
                            Parallelogram(
                                array([[1, 0, 0], [0, 2 * pi, 0], [0, 0, pi]])
                            ),
                            Translate(array([1, 0, 0])),
                            Ball(),
                        ]
                    ),
                    AccumulateOnto(deformation, 0.03),
                    AccumulateOnto(noise, 0.01),
                    Parallelogram(array([[1, 0, 0], [0, 0, 1]])),
                ]
            ),
        ).sculpt()
        deform = Composition(
            [
                Bezier()(rand(3, *randint(low=4, high=10, size=(3,))), [3, 2, 1]),
                Parallelogram(array([[1, 0, 0], [0, 2 * pi, 0], [0, 0, pi]])),
                Translate(array([1, 0, 0])),
                Ball(),
            ]
        )
        noise = Perlin_Vector.random()(3)

        N = [
            make_closed_LNE(populate_MVT(A, 1, 1.75, i * 0.0125), 0, 0.5)
            for i in range(2, 30)
        ]
        M = [
            make_closed_LNE(populate_MVT(B, 1, 1.75, i * 0.0125), 0, 0.5)
            for i in range(2, 60)
        ]
        L = List(list(map(lambda A: f(A, line, noise, deform), N)))
        K = __Sculpture__(
            List(list(map(lambda A: f(A, line, noise, deform), M))), Dialate(2)
        ).sculpt()

        write_to_file(f"{k+732}.svg", wrap(draw(List([squares(pi * (k / 20)), L, K]))))


## Line/Circle -> SumOfSpheres -> Bezier -> Concentric Circles / Squares
## reduction Bezier
def U07(k):
    A = rand(40, 3)
    beziers = [
        Bezier()(make_closed_LNE(degree_elevation(A[i:], i, 0), 0, 0.5), [0])
        for i in range(0, 15)
    ]
    bezier = Bezier()(make_closed_LNE(stack([bez.control_points for bez in beziers], axis=0), 0, .75), [1, 0])

    design = __Sculpture__(
        FlexPlane(Square(Segment), 200, 100).sculpt(),
        Composition(
            [
                bezier,
                Parallelogram(array([[1, 0, 0], [0, 0, 1]])),
            ]
        ),
    ).sculpt()

    write_to_file(f"u07_{k+100}.svg", wrap(draw(design)))
