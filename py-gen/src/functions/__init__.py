from src.functions.parallelogram import Parallelogram
from src.functions.bezier import Bezier, RationalBezier
from src.functions.sphere import Sphere
from src.functions.dialate import Dialate
from src.functions.translate import Translate
from src.functions.composition import Composition
from src.functions.copy import Copy
from src.functions.hypercube import HyperCube
from src.functions.id import ID
from src.functions.ball import Ball
from src.functions.perlin_noise import Perlin_Noise, Perlin_Stack, Perlin_Vector
from src.functions.add import Add
from src.functions.accumulateonto import AccumulateOnto
from src.functions.barycentric import Barycentric

from src.typeclass.__function__ import __Function__
## Here we can have functions that manipulate functions. Move Composition, Repeat, etc

## class Concat(__Function__):
##     def __init__(self, vff1, vff2):
##         self.vff1 = vff1
##         self.vff2 = vff2
## 
##     def __call__(self, t):
##         return (*self.vff1(t), *self.vff2(t))
