from numpy import array, array_split, squeeze, stack, concatenate
from functools import reduce
from math import comb
from enum import Enum

from src.typeclass.__function__ import __Function__
from src.typeclass.__sculpture__ import __Sculpture__
from src.typeclass.__random__ import __Random__
from src.functions.hypercube import HyperCube
from src.functions.hypercube import Mode as HCMode
from src.atoms import Segment, List

## Like Hypersphere, we need to reconstruct Bezier to dispatch on convolve
## strategy. Be it recursive, closed or AST constructions


class Mode(Enum):
    CLOSED = 0
    DECASTELJAU = 1

def collapsedispatch(mode):
    match mode:
        case Mode.CLOSED: return collapse_closed
        case Mode.DECASTELJAU: return collapse_decasteljau

def collapse_closed(s, scp, t, m):
    ## condense sub-arrays with closed-form
    f = lambda n: lambda t: lambda i: comb(n, i)*((1-t)**(n-i))*(t**i)
    collapse_function = f(s.control_points.shape[m]-1)(t)
    parts = [collapse_function(i)*part for i, part in enumerate(scp)]

    retv = squeeze(sum(parts),axis=m)
    return retv

def collapse_decasteljau(s, scp, t, m):
    ## The de Casteljau Algorithm
    ## condense sub-arrays with convolution 
    convolve = lambda t: lambda c: lambda p: (1-t)*p + t*c
    while len(scp) > 1: scp = [convolve(t)(p)(c) for p, c in zip(scp, scp[1:])]

    ## collect result of above computation and remove the condensed axis
    retv, *_ = scp
    retv = squeeze(retv, axis=m)
    return retv

def Bezier(mode = Mode.CLOSED):
    class bezier(__Random__, __Function__):
        def __init__(self, control_points: array, collapse_axes: array):
            self.control_points = control_points
            self.collapse_axes = collapse_axes

        def __call__(self, ts: array) -> array:
            ## Extract domain value and axis indicator.
            t, *ts = ts
            m, *ms = self.collapse_axes

            ## Along the given axis, gather sub-arrays from control points
            scp = array_split(self.control_points, self.control_points.shape[m], m)

            ## collapse given dispatch
            retv = bezier.collapse(self, scp, t, m)

            ## recur computation if there're more axes to compress or finished consuming
            ## the domain elements
            if ms and ts:
                ms = map(lambda x: x if x < m else x - 1, ms)
                retv = bezier(retv, ms).__call__(ts)

            return retv

        @classmethod
        def random(cls):
            raise NotImplementedError

        @classmethod
        def ID(cls, dim):
            HCD = HyperCube(HCMode.BEZIER)(dim)
            data = __Sculpture__(Segment(array([0]), array([1])), HCD).sculpt()

            def dfs(data):
                match data:
                    case List(elements=[Segment(l=l, m=m), *_]):
                        return stack(list(map(lambda seg: stack([seg.l, seg.m]), data.elements)))
                    case List(elements=[List(), *_]):
                        return stack(list(map(dfs, data.elements)))

            id_control_points = dfs(data)
            id_collapse_axes = range(dim)[::-1]

            return cls(id_control_points, id_collapse_axes)

    bezier.collapse = collapsedispatch(mode)
    return bezier

class RationalBezier(__Random__, __Function__):
    def __init__(control_points, collapse_axes, weights):
        self.control_points = control_points
        self.collapse_axes = collapse_axes
        self.weights = weights

    def __call__(self, ts):
        pass

    @classmethod
    def random(self):
        pass
