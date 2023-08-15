# __Data__, __Function__, __Camera__, __Light__

# Sculpture(__Data__, __Function__) -> Named functions
# Enviornment([[Sculpture, Position, CoordinateBasis], ...], __Light__)
# Enviornment(env_file?)

# Photograph(__Camera__, __Data__)
# Photograph(__Camera__, Sculpture(__Data__, __Function__))
# Photograph(__Camera__, Enviornment([[Sculpture, Position, CoordinateBasis], ...], __Light__))

# Video(__Camera__, Sculpture(__Data__, __Function__), __Update__, frames)
# Video(__Camera__, Enviornment([[Sculpture, Position, CoordinateBasis], ...], __Light__), __Update__, frames)

import numpy as np
from numpy.random import rand, randint

from src.typeclass.__sculpture__ import __Sculpture__
from src.functions.parallelogram import Parallelogram
from src.functions.bezier import Bezier
from src.functions.sphere import Sphere
from src.functions.dialate import Dialate
from src.functions.translate import Translate
from src.functions.composition import Composition
from src.functions.add import Add

from src.sculptures.unitplane import FlexPlane, FlexCube, FlexHyperCube
from src.sculptures.unitline import UnitLine
from src.sculptures.unitcube import Cube, Square, HCube

from src.atoms import Point, Segment, Triangle

from mp.pose_landmark_detection import Pose_Landmark_Detection
