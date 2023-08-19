from src.typeclass.__sculpture__ import __Sculpture__
from src.functions.bezier import Bezier
from mp.pose_landmark_detection import Pose_Landmark_Detection

from numpy import stack

def TemporalFrameBezierNoise():
    frame, frames = Pose_Landmark_Detection("py-gen/mp/pose_landmarker_full.task").setupmodel()
    scale = lambda convert: __Sculpture__(convert, Parallelogram(diag([width, height]))).sculpt()

    A = []
    for detection in frames.elements:
        A = [*A, stack(map(lambda x: x.data.l, detection.elements))]
    A = stack(A)

    ##!  When we break the Pose_Landmark_Detection class into OCV and MP, we'll want to be
    ##!  able to query OCV for the number of frames. 

    ## Construct Bezier form from (0,0) to (frames, frames) with random deviation control
    ## points along the way. Take output and round to nearest integer.

    ## With the above form B. Construct from A the mda C = A[range(*B(t)), :, :]. This will
    ## be placed into a new bezier form that'll form the basis/coordinate system for some
    ## Sculpture. One that'll likely vary with t as C did.

    ## Consider the fact that we're constructing a function from data here. Perhaps we should 
    ## move this into the functions directory

    breakpoint()
