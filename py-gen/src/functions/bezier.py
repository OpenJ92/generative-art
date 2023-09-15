from numpy import array, array_split, squeeze, stack, concatenate, ones
from functools import reduce, partial
from math import comb
from enum import Enum

from src.typeclass.__function__ import __Function__
from src.typeclass.__sculpture__ import __Sculpture__
from src.typeclass.__random__ import __Random__
from src.functions.hypercube import HyperCube
from src.functions.hypercube import Mode as HCMode
from src.atoms import Segment, List
from src.helpers.numpy import rational

## Like Hypersphere, we need to reconstruct Bezier to dispatch on convolve
## strategy. Be it recursive, closed or AST constructions


class Mode(Enum):
    CLOSED = 0
    DECASTELJAU = 1
    RATIONAL = 2

def collapse_dispatch(mode):
    match mode:
        case Mode.CLOSED: return collapse_closed
        case Mode.DECASTELJAU: return collapse_decasteljau

## Rational Closed form? 
def collapse_closed(this, control_vector, t, collapse_axis, weights):
    ## condense sub-arrays with closed-form
    f = lambda n: lambda t: lambda i: comb(n, i)*((1-t)**(n-i))*(t**i)
    collapse_function = f(this.control_points.shape[collapse_axis]-1)(t)
    parts = [ collapse_function(i)*part*weight
              for i, part, weight
              in zip(*enumerate(control_vector), weights)
            ]

    ## collect result of above computation and remove the condensed axis
    retv = squeeze(sum(parts),axis=collapse_axis)
    return retv


def collapse_decasteljau(this, control_vector, t, collapse_axis, weights):
    ## The de Casteljau Algorithm
    ## condense sub-arrays with convolution 
    tail = lambda lst: lst[1:]
    convolve = lambda t: lambda left: lambda right: (1-t)*right + t*left
    while len(control_vector) > 1:
        control_vector = [ convolve(t)(left)(right)
                           for left, right
                           in zip(control_vector, tail(control_vector))
                         ]

    ## collect result of above computation and remove the condensed axis
    retv, *_ = control_vector
    retv = squeeze(retv, axis=collapse_axis)
    return retv

def Bezier(mode = Mode.CLOSED):
    class bezier(__Random__, __Function__):
        def __init__(self, control_points, collapse_axes, weights=None):
            self.control_points = control_points
            self.collapse_axes  = collapse_axes
            self.weights =      weights \
                           if   weights \
                           else [ ones(shape = self.control_points.shape[axis] - 1)
                                  for axis
                                  in  self.collapse_axes
                                ]
            breakpoint()

        def __call__(self, ts: array) -> array:
            ## Extract domain value and axis indicator.
            t, *ts = ts
            collapse_axis, *collapse_axes = self.collapse_axes
            weight, *weights = self.weights

            ## Along the given axis, gather sub-arrays from control points
            control_vectors = array_split(self.control_points, \
                    self.control_points.shape[collapse_axis], collapse_axis)

            ## collapse given dispatch
            retv = collapse_dispatch(mode)(self, control_vectors, t, collapse_axis, None)

            ## recur computation if there're more axes to compress or finished consuming
            ## the domain elements
            if collapse_axes and ts:
                collapse_axes = map(lambda x: x if x < m else x - 1, ms)
                retv = bezier(retv, collapse_axes, weights).__call__(ts)

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

    return bezier

## Perhaps this should be constructed through composition. We have a function which recieves a Bezier
## and returns a new Bezier that has been edited with the application of rational. This way we could make
## compositions with Rational and the upcoming ElevateBezier classes. Both of which edit the control_point
## forms
class RationalBezier(Bezier()):
    def __init__(self, control_points, collapse_axes, weights, axes):
        self.control_points = self.form_control_points(control_points, weights, axes)
        self.collapse_axes = collapse_axes

    @classmethod
    def random(self):
        pass

    def __call__(self, ts):
        return Bezier()(self.control_points, self.collapse_axes).__call__(ts)

    def form_control_points(self, control_points, weights, axes):
        while weights:
            weight, *weights = weights
            axis, *axes      = axes
            control_points = rational(control_points, weight, axis)
        return control_points

