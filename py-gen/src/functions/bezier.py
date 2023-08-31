from numpy import array, array_split, squeeze, stack, concatenate

from src.typeclass.__function__ import __Function__
from src.typeclass.__sculpture__ import __Sculpture__
from src.functions.hypercube import HyperCube, Mode
from src.atoms import Segment, List

class Bezier(__Function__):
    def __init__(self, control_points: array, collapse_axes: array):
        self.control_points = control_points
        self.collapse_axes = collapse_axes

    def __call__(self, ts: array) -> array:
        ## The de Casteljau Algorithm
        ## Extract domain value and axis indicator.
        t, *ts = ts
        m, *ms = self.collapse_axes

        ## Along the given axis, gather sub-arrays from control points
        scp = array_split(self.control_points, self.control_points.shape[m], m)

        ## condense sub-arrays with convolution 
        while len(scp) > 1: scp = [self.convolve(t,p,c) for p, c in zip(scp, scp[1:])]

        ## collect result of above computation and remove the condensed axis
        retv, *_ = scp
        retv = squeeze(retv, axis=m)

        ## recur computation if there're more axes to compress or finished consuming
        ## the domain elements
        if ms and ts:
            ms = map(lambda x: x if x < m else x - 1, ms)
            retv = Bezier(retv, ms).__call__(ts)

        return retv

    def convolve(self, t, slice_one, slice_two):
        return (1-t)*slice_one + t*slice_two

    def ID(dim):
        HCD = HyperCube(Mode.BEZIER)(dim)
        data = __Sculpture__(Segment(array([0]), array([1])), HCD).sculpt()

        def dfs(data):
            match data:
                case List(elements=[Segment(l=l, m=m), *_]):
                    return stack(list(map(lambda seg: stack([seg.l, seg.m]), data.elements)))
                case List(elements=[List(), *_]):
                    return stack(list(map(dfs, data.elements)))

        id_control_points = dfs(data)
        id_collapse_axes = range(dim)[::-1]

        return Bezier(id_control_points, id_collapse_axes)

    def WithTangents(control_points, tangent_construction_policy, collapse_axes):
        ## I think we need to make a new folder with numpy helper functions. Particularly
        ## for injecting tangents and interpolation operations. These will be array_split 
        ## compose concatenate operations in general. (As I think...).
        raise NotImplementedError

class FUNCBezier(__Function__):
    def __init__(self, control_points: array, collapse_axes: array):
        f = vectorize(lambda x: lambda _: x)
        functional_points = f(control_points)
        self.control_points = functional_points
        self.collapse_axes = collapse_axes
        self.function = self.construct_function()

    def construct_function(self):

        t, *ts = ts
        m, *ms = self.collapse_axes

    ## We have to consider how this works exactly.
    def functional_convolve(self, t, func1, func2):
        return lambda t: lambda q: (1 - t)*func1(q) + lambda q: t*func2(q)


