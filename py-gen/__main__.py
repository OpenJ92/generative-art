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
        Translate, Composition, ID, Ball, Perlin_Noise, Perlin_Stack, Perlin_Vector, Add
from src.sculptures import FlexHyperCube, FlexCube, FlexPlane, \
        UnitLine, Cube, Square, HCube, TemporalFrameBezierNoise
from src.atoms import Point, Segment, Triangle, draw, wrap, write_to_file, List
from src.helpers.numpy import *

from mp.pose_landmark_detection import Pose_Landmark_Detection
from src.typeclass.__sculpture__ import __Sculpture__

# Add is not configured properly. I want a proper __call__ funtion which takes the existing data and adds
# onto it the valuation of another function atop it. AccumulateOnto?
def explore():
    for k in range(20):
        A = rand(10, 4)
        print(k, A)
        f = lambda A: __Sculpture__( UnitLine(500).sculpt()
                                    , Composition([
                                     Add( Perlin_Vector.random()(4)
                                        , Composition(
                                            [ Bezier()(A, [0])
                                            , Parallelogram(array([[1,0,0,0],[0,2*pi,0,0],[0,0,pi,0],[0,0,0,pi]]))
                                            , Translate(array([1,0,0,0]))
                                            , Ball()
                                            ])
                                       )
                                    , Parallelogram(array([[1,0,0,0], [0,0,0,1]]))
                                    ])
                                    ).sculpt()

        N = [make_closed_LNE(populate_MVT(A, 1, 2, i*.0125), 0, .5)  for i in range(2, 60)]
        L = List(list(map(f, N)))
        write_to_file(f"smoothtest_{k+640}.svg", wrap(draw(L)))
