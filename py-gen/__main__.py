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

from src.functions import Parallelogram, Bezier, Sphere, Dialate, \
        Translate, Composition, ID, Ball, FUNCBezier, Perlin_Noise, Perlin_Stack, Perlin_Vector
from src.sculptures import FlexHyperCube, FlexCube, FlexPlane, \
        UnitLine, Cube, Square, HCube, TemporalFrameBezierNoise
from src.atoms import Point, Segment, Triangle, draw, wrap, write_to_file, List
from src.helpers.numpy import *

from mp.pose_landmark_detection import Pose_Landmark_Detection
from src.typeclass.__sculpture__ import __Sculpture__

def explore():
    for k in range(10):
        A = 100*rand(10, 2)
        print(k, A)
        f = lambda A: __Sculpture__(UnitLine(500).sculpt(), Bezier(A, [0])).sculpt()
        N = [make_closed_LNE(populate_MVT(A, 1, 5, i*.025), 0, .8)  for i in range(2, 30)]
        ## N = [populate_MVT(make_closed_LNE(A, 0, .5), 1, 5, .5 + i*.1)  for i in range(2, 10)]
        L = List(list(map(f, N)))
        write_to_file(f"smoothtest_{k+220}.svg", wrap(draw(L)))
