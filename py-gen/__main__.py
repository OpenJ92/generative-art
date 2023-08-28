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

from src.functions import Parallelogram, Bezier, Sphere, Dialate, Translate, Composition, ID, Ball
from src.sculptures import FlexHyperCube, FlexCube, FlexPlane, \
        UnitLine, Cube, Square, HCube, TemporalFrameBezierNoise
from src.atoms import Point, Segment, Triangle, draw, wrap, write_to_file, List
from src.helpers.numpy import *

from mp.pose_landmark_detection import Pose_Landmark_Detection
from src.typeclass.__sculpture__ import __Sculpture__

breakpoint()
A = make_closed(100*rand(3, 2), 0)
B = populate_MVT(A, 1, 5, .01)
f = lambda A: __Sculpture__(UnitLine(150).sculpt(), Bezier(A, [0])).sculpt()
M = populate_MVT(A, 1, 2, .01)
L = List([f(A), *[f(populate_MVT(A, 1, i, 1)) for i in range(2, 7)]])
## Q = List([Point(*x) for x in array_split(A, A.shape[0], 0)])
## R = List([Point(*x) for x in array_split(B, B.shape[0], 0)])
## D = List([f(A), Q, f(B), R, f(M)])

write_to_file("smoothtest42.svg", wrap(draw(L)))
