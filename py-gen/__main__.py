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
from numpy import array_split, concatenate, square, array
from numpy.random import rand
from math import pi

from src.functions import Parallelogram, Bezier, Sphere, Dialate, \
        Translate, Composition, ID, Ball, Perlin_Noise, Perlin_Stack, \
        Perlin_Vector, Add, AccumulateOnto, Copy
from src.sculptures import FlexHyperCube, FlexCube, FlexPlane, \
        UnitLine, Cube, Square, HCube, TemporalFrameBezierNoise
from src.atoms import Point, Segment, Triangle, draw, wrap, write_to_file, List
from src.helpers.numpy import *

from mp.pose_landmark_detection import Pose_Landmark_Detection
from src.typeclass.__sculpture__ import __Sculpture__

# Remember to do make the sculpture that makes a set of beziers that reduce order in order. Update each to upgrade
# to the max order. What's more, add multithreading to rendering processes. Functions may or may not be seperable
# into component pieces.

def explore():
    for k in range(10):
        A = rand(10, 3)
        print(k, A)

        f = lambda A, noise, deformation: __Sculpture__( UnitLine(1500).sculpt()
                                    , Composition([
                                          Composition(
                                            [ Bezier()(A, [0])
                                            , Parallelogram(array([[1,0,0],[0,2*pi,0],[0,0,pi]]))
                                            , Translate(array([1,0,0]))
                                            , Ball()
                                            ])
                                        , AccumulateOnto(deformation, .0075)
                                        , AccumulateOnto(noise, .0025)
                                        , Parallelogram(array([[1,0,0], [0,0,1]]))
                                    ])
                                    ).sculpt()
        deform = Composition([ Bezier()(rand(3,5,5,5),[3,2,1])
                             , Parallelogram(array([[1,0,0],[0,2*pi,0],[0,0,pi]]))
                             , Ball()
                             ])
        noise = Perlin_Vector.random()(3)
        N = [make_closed_LNE(populate_MVT(A, 1, 2, i*.0125), 0, .5)  for i in range(2, 60)]
        L = List(list(map(lambda A: f(A, noise, deform), N)))

        write_to_file(f"smoothtest_{k+750}.svg", wrap(draw(L)))

## Line/Circle -> SumOfSpheres -> Bezier -> Concentric Circles / Squares
