# __Data__, __Function__, __Camera__, __Light__

# Sculpture(__Data__, __Function__) -> Named functions
# Enviornment([[Sculpture, Position, CoordinateBasis], ...], __Light__)
# Enviornment(env_file?)

# Photograph(__Camera__, __Data__)
# Photograph(__Camera__, Sculpture(__Data__, __Function__))
# Photograph(__Camera__, Enviornment([[Sculpture, Position, CoordinateBasis], ...], __Light__))
# Video(__Camera__, Sculpture(__Data__, __Function__), __Update__, frames)
# Video(__Camera__, Enviornment([[Sculpture, Position, CoordinateBasis], ...], __Light__), __Update__, frames)


## valid function composition graph. edges represent valid function composition. For every new function
## constructed, you register it with the function composition graph. Traversals over this graph form the
## composition of functions
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
    Map,
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
    Stack,
    Linear_Pedal,
    Sphere_Line,
    Floral,
    Rectangles,
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
            make_closed_LNE(populate_MVT(A, 1.75, i * 0.0125), 0, 0.5)
            for i in range(2, 30)
        ]
        M = [
            make_closed_LNE(populate_MVT(B, 1.75, i * 0.0125), 0, 0.5)
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
    A = rand(20, 3)
    beziers = [
        Bezier()(make_closed_LNE(degree_elevation(A[i:], i, 0), 0, 0.5), [0])
        for i in range(0, 15, 2)
    ]
    bezier = Bezier()(
        make_closed_LNE(
            populate_MVT(
                stack([bez.control_points for bez in beziers], axis=0), 2, 0.25
            ),
            0,
            0.25,
        ),
        [1, 0],
    ).update_with_random_weights()

    plane = FlexPlane(FlexSquare(5), 1000, 1).sculpt()
    ## plane = Stack(UnitStrip(1500), array([[1], [0]]), array([0, 1]), 300).sculpt()
    design = __Sculpture__(
        plane,
        Composition(
            [
                bezier,
                Parallelogram(array([[1, 0, 0], [0, 4*pi, 0], [0, 0, 2*pi]])),
                Translate([3,0,0]),
                Ball(),
                Parallelogram(array([[1, 0, 0], [0, 0, 1]])),
            ]
        ),
    ).sculpt()

    write_to_file(f"u07_{k+100}.svg", wrap(draw(design)))


def U08(k):
    ## U07 with ndarray at 3xnxmxk R3 -> R3 Construct stacks of Concentrics(Squares). Close over all
    ## Three collapse dimensions
    pass


def U11():
    ## Hypersphere products. Define poly-multipy and carry out over k-sphere * l-sphere.
    ## I've been very curious about the visual form of these for a long time now. Do a
    ## collection of projections of each product and place in canvases. Three per canvas

    ## TODO: Constrcut PolynomialProduct __Function__ taking any two np.arrays 

    pass


def U12():
    ## Bezier k-form as velocity function.
    pass


def U14():
    ## Bezier k-form as acceleration function
    pass


def U17():
    return Linear_Pedal(.2, .7, 5)

def U18(k):
    data = Sphere_Line(5)(FlexPlane(Square(Segment),100,100).sculpt()).sculpt()
    data = __Sculpture__(data, Parallelogram(array([[1,0,0], [0,0,1]]))).sculpt()
    write_to_file(f"u18_{k+500}.svg", wrap(draw(data)))

def U15(k, degree):
    start, end = rand(), rand()
    stem = end*rand()


    pedal  = Linear_Pedal(start, end, degree, stem)
    data = __Sculpture__(FlexPlane(Square(Segment), 100, 100).sculpt(), pedal)
    data = __Sculpture__(data.sculpt(), Parallelogram(array([[1,0,0], [0,1,0]])))
    write_to_file(f"u15_{k+100}.svg", wrap(draw(data.sculpt())))

def U21(k):
    floral = Floral(2, .09, k)
    functions = len(floral.funcs[0].funcs)
    data = __Sculpture__(FlexPlane(Square(Segment), 100, 100).sculpt(), Copy(functions))
    data = __Sculpture__(data.sculpt(), floral)
    data = __Sculpture__(data.sculpt(), Parallelogram(array([[1,0,0], [0,1,0]])))
    write_to_file(f"u21_{k+100}.svg", wrap(draw(data.sculpt())))

def U22(k):
    floral = Floral(3, .05, k)
    functions = len(floral.funcs[0].funcs)
    data = __Sculpture__(FlexPlane(Square(Segment), 50, 50).sculpt(), Copy(functions))
    data = __Sculpture__(data.sculpt(), floral)

    perlins = [Perlin_Noise.random() for _ in range(3)]
    for perlin in perlins:
        perlin.scale = .001

    data = __Sculpture__(data.sculpt(), Perlin_Vector(perlins))
    data = __Sculpture__(data.sculpt(), Parallelogram(array([[1,0,0], [0,1,0]])))

    write_to_file(f"u22_{k+100}.svg", wrap(draw(data.sculpt())))

def U23(k, n):
    data = Rectangles(n*(2*rand(20,10,8)-1), 8, 8)
    write_to_file(f"u23_{k+100}.svg", wrap(draw(data)))
