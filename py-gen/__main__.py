# Data, Function, __Camera__, __Light__ # Sculpture(Data, Function) -> Named functions # Enviornment([[Sculpture, Position, CoordinateBasis], ...], __Light__) # Enviornment(env_file?)
# Photograph(__Camera__, Data)
# Photograph(__Camera__, Sculpture(Data, Function))
# Photograph(__Camera__, Enviornment([[Sculpture, Position, CoordinateBasis], ...], __Light__))
# Video(__Camera__, Sculpture(Data, Function), __Update__, frames)
# Video(__Camera__, Enviornment([[Sculpture, Position, CoordinateBasis], ...], __Light__), __Update__, frames)


## valid function composition graph. edges represent valid function composition. For every new function
## constructed, you register it with the function composition graph. Traversals over this graph form the
## composition of functions


## I believe we're at a point where this program has revealed it's inadequacies. As of current, all
## forms must be hard coded into they system by myself. While artistic intent is important, I can't 
## help but feel that I'm not using the medium to it's fullest extent. All functions are aware of 
## of thier forms (Vec[n] -> Vec[m]) or (Data -> Data) and so are capable of self assembling. What
## is more, the program is strictly single threaded. With the introduction of python 3.14, GIL will
## be unlocked and so to the power or parallel programming. Introduction of tagged functions as being
## "Parallel" or perhaps more specifically "Independent" and of Product Monoids over Data forms will
## unlock speedups worth pursuing. As a means to this end, a python specific Haskell isomorphism should
## be constructed so as to 'safely' implement these parallel programs in 'self assembly' mode. The 
## extrodinary thing here is the system is generic enough to be constructed 'point free' in so far as
## one might register functions and Data to a composition graph program which itself constructs
## parallel enabled computation graphs. The API should be suitable for users to construct custom
## sculptures if they so choose. Making this program a strict subset of the new one will be a goal.

## I'm starting to have a panic attack again. I don't know what I'm doing here. I implement functions 
## which are nodes in a composition graph. They could be many different typ[es a -> b,  a -> m b,
## m a -> m b They registered and connected in the composition graph. traversals are then deffered 
## computations (i.e, f @ g @ h ... ) as constructed by traversals of said composition graph with the 
## Functional Programming package. There should be a 'paralellism submodule that can scan the traversals 
## and determine paralellization potential. This can be done through tagging Function elements as Pure or 
## Effectful etc.etc. I'm feeling se scared.

from numpy.random import rand, randint, seed
from numpy import (
    identity,
    array_split,
    concatenate,
    square,
    array,
    ones,
    zeros,
    multiply,
    tensordot,
    hstack,
    einsum,
    sin,
    cos,
    linspace,
    array,
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
    Frame,
    Tile,
    ZipApply,
    Scale,
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
from src.atoms import Point, Segment, Triangle, SegmentStrip, Meta_Data, draw, wrap, write_to_file, List, Empty
from src.helpers.numpy import *

## Removed MediaPipe from project
## from mp.pose_landmark_detection import Pose_Landmark_Detection
from src.typeclass import Sculpture

# Remember to do make the sculpture that makes a set of beziers that reduce order in order. Update each to upgrade
# to the max order. What's more, add multithreading to rendering processes. Functions may or may not be seperable
# into component pieces.


def U04():
    for k in range(10):
        A = rand(7, 3)
        B = rand(5, 3)
        print(k, A)

        line = UnitStrip(1500)
        squares = lambda k: Sculpture(
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

        f = lambda A, line, noise, deformation: Sculpture(
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
        K = Sculpture(
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
    design = Sculpture(
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

    ## TODO: Constrcut PolynomialProduct Function taking any two np.arrays 

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
    data = Sculpture(data, Parallelogram(array([[1,0,0], [0,0,1]]))).sculpt()
    write_to_file(f"u18_{k+500}.svg", wrap(draw(data)))

def U15(k, degree):
    start, end = rand(), rand()
    stem = end*rand()


    pedal  = Linear_Pedal(start, end, degree, stem)
    data = Sculpture(FlexPlane(Square(Segment), 100, 100).sculpt(), pedal)
    data = Sculpture(data.sculpt(), Parallelogram(array([[1,0,0], [0,1,0]])))
    write_to_file(f"u15_{k+100}.svg", wrap(draw(data.sculpt())))

def U21(k):
    floral = Floral(2, .09, k)
    functions = len(floral.funcs[0].funcs)
    data = Sculpture(FlexPlane(Square(Segment), 100, 100).sculpt(), Copy(functions))
    data = Sculpture(data.sculpt(), floral)
    data = Sculpture(data.sculpt(), Parallelogram(array([[1,0,0], [0,1,0]])))
    write_to_file(f"u21_{k+100}.svg", wrap(draw(data.sculpt())))

def U22(k):
    floral = Floral(3, .05, k)
    functions = len(floral.funcs[0].funcs)
    data = Sculpture(FlexPlane(Square(Segment), 5, 5).sculpt(), Copy(functions))
    data = Sculpture(data.sculpt(), floral)

    perlins = [Perlin_Noise.random() for _ in range(3)]
    for perlin in perlins:
        perlin.scale = .001

    data = Sculpture(data.sculpt(), Perlin_Vector(perlins))

    data = Sculpture(data.sculpt(), Parallelogram(array([[1,0,0], [0,1,0]])))

    write_to_file(f"u22_{k+100}.svg", wrap(draw(data.sculpt())))

def U22Kinematic(_seed, frames, time_collapse_axes, sculpture_collapse_axes):
    ## Here we've taken a uniform sample of the time domain [0,1]. This will be
    ## be supplied to our control point Bezier R1 -> R(n x m x ... x ) which will
    ## further be supplied to our sculptural Beziers
    seed(_seed)

    time_domain = linspace(0,1,frames)

    ## Here we generate the initial random Bezier whose axes are 
    ## R(*time_collapes_axes x *sculpture_collapes_axes) We're going to need
    ## some function R -> R(time_collapes_axes). For the time being, we'll supply
    ## another random Bezier of the same type to be submitted. (Look to parameterize this in the future)
    time_transform_control = rand(randint(3, 10), time_collapse_axes)
    ## Note: This time_transform Bezier should loop back on itself as C1. This way we'll
    ## have perfect loop videos.
    time_transform = Bezier()(time_transform_control, [0])

    ## Here we have a Bezier whose control points have the dimension as the sum of 
    ## the time domain collapse axes and sculpture collapse axes with it's own collapse
    ## axes being the first time_collapse_axes elements [0, 1, ..., time_collapse_axes]
    ## This produces a MDA with dimension sculpture_collapse_axes to be submitted to the
    ## sculpture.
    control_point_generator_control = rand(*randint(3, 10, time_collapse_axes+sculpture_collapse_axes+1))
    control_point_generator = Bezier()(control_point_generator_control, collapse_axes=list(range(time_collapse_axes)))

    ## Sculpture generation. We sample the time domain so as to generate a vector suitable
    ## for submission to our control_point_generator. control_point_generator builds control_points
    ## for our bezier sculpture and is then used in the construction of function Bezier and
    ## registered into our beziers list.
    beziers = []
    frame = Frame((1080, 1920), 100)
    for time in time_domain:
        ## Vector R(time_collapes_axes)
        transformed_sample = time_transform([time])
        control_point_time = control_point_generator(transformed_sample)
        bezier = Bezier()(control_point_time, range(sculpture_collapse_axes))

        index = control_point_time.shape[-1]
        selector = identity(2)
        another = zeros([2, sculpture_collapse_axes-2])
        other = zeros([2, index-2])

        ## VERY SIMPLISTIC PROJECTIONS TAKING THE FIRST TWO COMPONENTS. REPLACE
        _up = Parallelogram(hstack([selector, another]).T)
        _down = Parallelogram(hstack([selector, other]))
        function = Composition([_up, bezier, _down, frame])

        beziers.append(function)

    ## data1 = Sculpture(Concentric(FlexSquare(50), 12*12).sculpt(), Copy(frames)).sculpt()
    ## data1 = Sculpture(data1, ZipApply(beziers)).sculpt()

    ## data0 = Sculpture(FlexPlane(Square(Segment), 60, 60).sculpt(), Copy(frames)).sculpt()
    ## data0 = Sculpture(data0, ZipApply(beziers)).sculpt()

    ## data1 = Sculpture(Concentric(Cube(Segment), 12*12).sculpt(), Copy(frames)).sculpt()
    ## data1 = Sculpture(data1, ZipApply(beziers)).sculpt()

    circle = SegmentStrip.from_itterable(list(map(Sphere(), linspace(0,2*pi, 100).reshape((100,1)))))
    circle = Sculpture(circle, Scale(.5)).sculpt()
    circle = Sculpture(circle, Translate(array([.5,.5])))

    circle = Sculpture(Concentric(circle, 125).sculpt(), Copy(frames)).sculpt()
    circle.elements[-1] = Meta_Data(data=circle.elements[-1], meta={"stroke":1})
    circle = Sculpture(circle, ZipApply(beziers)).sculpt()

    data = circle

    tiling = (5, 4)
    width, height = tiling
    quotient, remainder = divmod(frames, width*height)
    empty = [Empty] * remainder
    data.elements = [*data.elements, *empty]

    sections = []
    for section in range(quotient + 1):
        lower, upper = width*height*section, width*height*(section+1)
        tiles = List(data.elements[lower:upper])
        sections.append(tiles)

    data = List(sections)
    data = Sculpture(data, Map(Tile(tiling, (1080, 1920)))).sculpt()

    ## For each element in data now, which are the paginated frames, we can export to svg
    for page, element in enumerate(data.elements):
        write_to_file(f"KinematicBezier_{_seed}_A_{page}.svg", wrap(draw(element)))
        print(f"KinematicBezier_{_seed}_{page}.svg")

def U23(k, n):
    data = Rectangles(n*(2*rand(20,10,8)-1), 400, 1).sculpt()
    write_to_file(f"u23_{k+100}.svg", wrap(draw(data)))

def U24(k, n):
    control_points = n*(2*rand(20,10,8)-1)
    control_points = make_closed_MVT(control_points, 0, 1)
    control_points = make_closed_MVT(control_points, 1, 1)

    data = Rectangles(control_points, 200, 1).sculpt()
    write_to_file(f"u24_{k+100}.svg", wrap(draw(data)))

def U25(k, n):
    ## We need to make a quick 'frame' object
    control_points = n*(2*rand(10,10,20,10,8)-1)
    bezier = Bezier()(control_points, [0,1])

    ## frames = []
    ## for sample in 2*pi*linspace(24*5):
    ##     circle = array([sin(sample), cos(sample)]) + [.5, .5]
    ##     rectangles = Rectangles(bezier(control_points)(circle), 200, 1).sculpt()
    ##     ## Sculpture supplied to rectangles MUST be two dimensional. 
    ##     frame = Frame(rectangles, 297, 420); frame.fit(120)
    ##     frames.append(frame)

    ## pages = []
    ## for page in range(10):
    ##     selection = frames[12*page: 12*(page+1)]
    ##     tile = Tile(selection), 3, 4).sculpt() ## selection must be a list of Frames
    ##     pages.append(tile)

    ## for frame, page in enumerate(pages):
    ##     # write to file
    ##     pass

    ## breakpoint()
