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

    def __call__(self, ts):
        ## perhaps we need to reconstruct ts s.t. the compenents match the number of times
        ## we need to apply that component to self.function. There's some sense that the 
        ## function we build is waiting for the t to fill. At last, we'll supply a None 
        ## at the end to unpack the numbers hidden in f. for example

        ## control_points.shape = (1,4,2,3)
        ## ts = (1,2,3,4)

        ## becomes:

        ##     ts_augment = (1,2,2,2,2,3,3,4,4,4,None)
        ##
        ## and we return self.function(ts_augment)
        ## We'll need a apply function function which takes the elements of ts_augment and
        ## applys them one at a time

        return self.function(ts)

    def construct_function(self):
        pass

    ## We have to consider how this works exactly. Will this run faster than what we have in 
    ## the proper Bezier __Function__?
    def functional_convolve(self, t, func1, func2):
        return lambda t: lambda q: (1 - t)*func1(q) + t*func2(q)


