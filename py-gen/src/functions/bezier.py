from numpy import array, array_split, squeeze, stack, concatenate, ones
from numpy.random import rand
from functools import reduce, partial
from math import comb
from enum import Enum

from src.typeclass.__function__ import __Function__
from src.typeclass.__sculpture__ import __Sculpture__
from src.typeclass.__random__ import __Random__
from src.functions.hypercube import HyperCube
from src.functions.hypercube import Mode as HCMode
from src.functions.sphere import Sphere
from src.atoms import Segment, List


class Mode(Enum):
    CLOSED = 0
    DECASTELJAU = 1


def collapse_dispatch(mode):
    match mode:
        case Mode.CLOSED:
            return collapse_closed
        case Mode.DECASTELJAU:
            return collapse_decasteljau


def bernstein(n, t, i):
    combinations = comb(n, i)
    bernstein_basis = ((1 - t) ** (n - i)) * (t**i)
    ## print(n, t, i, bernstein_basis, combinations, (1-t)**(n-i), t**i)
    return combinations * bernstein_basis


def collapse_closed(this, control_vector, t, collapse_axis, weights):
    ## Bernstein Closed Form
    n = this.control_points.shape[collapse_axis] - 1
    total_weight = [bernstein(n, t, i) * weight for i, weight in enumerate(weights)]

    if sum(total_weight) == 0:
        breakpoint()

    parts = []
    for i, (part, weight) in enumerate(zip(control_vector, weights)):
        parts = [*parts, (bernstein(n, t, i) * part * weight) / sum(total_weight)]

    retv = squeeze(sum(parts), axis=collapse_axis)
    return retv


def collapse_decasteljau(this, control_vector, t, collapse_axis, weights):
    ## The de Casteljau Algorithm - Unweighted
    tail = lambda lst: lst[1:]
    interpolate = lambda t: lambda left: lambda right: (1 - t) * right + t * left
    while len(control_vector) > 1:
        control_vector = [
            interpolate(t)(left)(right)
            for left, right in zip(control_vector, tail(control_vector))
        ]

    retv, *_ = control_vector
    retv = squeeze(retv, axis=collapse_axis)
    return retv


def Bezier(mode=Mode.CLOSED):
    class bezier(__Random__, __Function__):
        def __init__(self, control_points, collapse_axes, weights=None):
            self.control_points = control_points
            self.collapse_axes = collapse_axes
            self.weights = (
                weights
                if weights
                else [
                    ones(shape=self.control_points.shape[axis])
                    for axis in self.collapse_axes
                ]
            )

        def __call__(self, ts: array) -> array:
            ## Extract domain value and axis indicator.
            t, *ts = ts
            collapse_axis, *collapse_axes = self.collapse_axes
            weight, *weights = self.weights

            ## Along the given axis, gather sub-arrays from control points
            control_vectors = array_split(
                self.control_points,
                self.control_points.shape[collapse_axis],
                collapse_axis,
            )

            ## collapse given dispatch
            collapse = collapse_dispatch(mode)(
                self, control_vectors, t, collapse_axis, weight
            )

            ## recur computation if there're more axes to compress or finished consuming
            ## the domain elements
            if collapse_axes and ts:
                u_collapse_axes = list(
                    map(lambda x: x if x < collapse_axis else x - 1, collapse_axes)
                )
                collapse = bezier(collapse, u_collapse_axes).__call__(ts)

            return collapse

        def update_with_random_weights(self):
            shape = self.control_points.shape
            weights = []
            for axis in self.collapse_axes:
                weights = [
                    *weights,
                    Sphere()(
                        rand(
                            shape[axis] - 1,
                        )
                    ),
                ]
            self.weights = weights
            return self

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
                        return stack(
                            list(map(lambda seg: stack([seg.l, seg.m]), data.elements))
                        )
                    case List(elements=[List(), *_]):
                        return stack(list(map(dfs, data.elements)))

            id_control_points = dfs(data)
            id_collapse_axes = range(dim)[::-1]

            return cls(id_control_points, id_collapse_axes)

    return bezier
