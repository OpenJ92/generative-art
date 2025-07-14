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
    cumsum,
    repeat,
    insert,
    pi,
    stack,
)
from numpy.random import rand, randint
from math import sqrt
import mediapipe as mp

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
    Const,
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

from src.executors import Sculpture


def U04():
    for k in range(10):
        A, B = rand(7, 3), rand(5, 3)
        line = UnitStrip(1500)

        def squares(k):
            sculpture = Concentric(FlexSquare(50), 100).sculpt()

            domain = Parallelogram([[2 * pi, 0], [0, 1 * pi]])
            translate = Translate([pi * (k / 20), pi * (k / 20)])
            projection = Parallelogram(array([[1, 0, 0], [0, 0, 1]]))
            function = Composition([domain, translate, Sphere(), projection])

            return Sculpture(sculpture, function).sculpt()

        def f(A, line, noise, deformation):
            bezier = Bezier()(A, [0])
            projection = Parallelogram(array([[1,0,0,0,0],[0,1,0,0,0],[0,0,1,0,0]]))
            domain = Parallelogram(array([[1, 0, 0], [0, 2 * pi, 0], [0, 0, pi]]))
            translate = Translate(array([1, 0, 0]))
            composition = Composition([bezier, projection, domain, translate, Ball()])

            deformation_ = AccumulateOnto(deformation, 0.03)
            noise_ = AccumulateOnto(noise, 0.01)
            projection = Parallelogram(array([[1, 0, 0], [0, 0, 1]]))
            function = Composition([composition, deformation_, noise_, projection])

            sculpture = Sculpture(line.sculpt(), function).sculpt()

            return sculpture


        bezier = Bezier()(rand(3, *randint(low=4, high=10, size=(3,))), [3, 2, 1])
        domain = Parallelogram(array([[1, 0, 0], [0, 2 * pi, 0], [0, 0, pi]]))
        translate = Translate(array([1, 0, 0]))
        deform = Composition([bezier, domain, translate, Ball()])
        noise = Perlin_Vector.random()(3)

        N = []
        for i in range(2, 30):
            control = make_closed_LNE(populate_MVT(A, 1.75, i * 0.0125), 0, 0.5)
            sculpture = f(control, line, noise, deform)
            N.append(sculpture)

        M = []
        for i in range(2, 60):
            control = make_closed_LNE(populate_MVT(B, 1.75, i * 0.0125), 0, 0.5)
            sculpture = f(control, line, noise, deform)
            M.append(sculpture)

        L = List(N)
        K = Sculpture(List(M), Dialate(2)).sculpt()

        write_to_file(f"{k+732}.svg", wrap(draw(List([squares(pi * (k / 20)), L, K]))))


def U07(k):
    A = rand(20, 3)

    beziers = []
    for i in range(0, 15, 2):
        function = Bezier()(make_closed_LNE(degree_elevation(A[i:], i, 0), 0, 0.5), [0])
        beziers.append(function)

    control = []
    for bezier in beziers:
        control.append(bezier.control_points)
    control = make_closed_LNE(populate_MVT(stack(control, axis=0), 2, 0.25), 0, 0.25)

    bezier = Bezier()(control, [1, 0]).update_with_random_weights()
    domain = Parallelogram(array([[1, 0, 0], [0, 4*pi, 0], [0, 0, 2*pi]]))
    translate = Translate([3,0,0])
    projection = Parallelogram(array([[1, 0, 0], [0, 0, 1]]))

    plane = FlexPlane(FlexSquare(5), 1000, 1).sculpt()
    design = Sculpture(plane, Composition([bezier, domain, translate, Ball(), projection])).sculpt()

    write_to_file(f"u07_{k+100}.svg", wrap(draw(design)))

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
    for section in range(quotient):
        lower, upper = width*height*section, width*height*(section+1)
        tiles = List(data.elements[lower:upper])
        sections.append(tiles)

    data = List(sections)
    data = Sculpture(data, Map(Tile(tiling, (1080, 1920)))).sculpt()

    ## For each element in data now, which are the paginated frames, we can export to svg
    for page, element in enumerate(data.elements):
        write_to_file(f"KinematicBezier_{_seed}_A_{page}.svg", wrap(draw(element)))
        print(f"KinematicBezier_{_seed}_{page}.svg")

## I think we done enough of these for now. It's time to work on Floral. Something
## different for the M.02 series. 


def M02(bezier_counts):
    ## Here we're going to make our moving mountains set. This'll be special because we'll be
    ## doing an isometric transform on the construction. 
    plains = Stack(UnitStrip(200), array([[1],[0],[0]]), array([0,1,0]), 80)

    def Mountain(bezier_count):
        beziers = []
        perlin = Perlin_Stack.random()
        for _ in range(bezier_count):
            dimensions = [randint(2, 10) for _ in range(3)]
            control = rand(*dimensions) - array([.25])
            beziers.append(Bezier()(control, [0,1,2]))

        scale = []
        proportions = 2*square(Sphere()(pi*rand(bezier_count-1)))
        for bezier, proportion in zip(beziers, proportions):
            scale.append(Composition([bezier, Scale(proportion)]))

        agglomeration = Const(0)
        for compose in scale:
            agglomeration = Add(compose, agglomeration)

        return Add(ID(), Composition([Add(agglomeration, perlin), Scale(array([0,0,1]))]))

    isometric = Parallelogram(array([[sqrt(3)/2, -sqrt(3)/2, 0], [0.5, 0.5, -1]]))

    dividers = [Composition([Translate([0,0,-2]), isometric])]
    samples = cumsum(2*len(bezier_counts)*square(Sphere()(rand(2*len(bezier_counts)-1))))
    bezier_counts = repeat(array(bezier_counts), 2)
    for bezier_count, translate in zip(bezier_counts, samples):
        function = Composition([Mountain(bezier_count), Translate(translate*array([0,0,1])), isometric])
        dividers.append(function)
    dividers.append(Composition([Translate([0,0,samples[-1]+2]), isometric]))
    dividers = iter(dividers)

    sculptures = []
    for first, second in zip(dividers,dividers):
        tectonic = Sculpture(plains.sculpt(), first).sculpt()
        sea = Sculpture(plains.sculpt(), second).sculpt()

        segments = [tectonic, sea]
        for up, down in zip(tectonic.elements, sea.elements):
            left = up.points[0].l, down.points[0].l
            right = up.points[-1].l, down.points[-1].l
            segments.extend([Segment(*left), Segment(*right)])

        sculptures.extend(segments)

    write_to_file(f"mountain_{rand()}.svg", wrap(draw(List(sculptures))))
