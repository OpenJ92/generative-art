from numpy import array_split, concatenate, square

## Functor | Applicative Numpy A forms need to be constructed
## iteration -- product(*map(lambda x: list(range(x)),A.shape))
##           -- A[(slice(10),2,slice(10),1)] == A[:,2,:,1]
##           -- A[(*(4,5,6), slice(10), *(3,), slice(4))] == A[4,5,6,:,3,:,1]

def condense(A, dims):
    shape = A.shape
    ranges = list(map(range, shape))
    slices = list(map(slice, shape))
    key = [1 if n in dims else 0 for n in range(len(shape))]

    breakpoint()
    ## this is a really interesting algo. Take some time to think.

def linear_interpolate(A, collapse_axes, samples):
    for axis, sample in zip(collapse_axes, samples):
        B = array_split(A, A.shape[axis], axis)
        f = lambda a, b: lambda t: a + (t/sample)*(b - a)

        C = []
        while True:
            match B:
                case [] | [_]:
                    raise NotImplementedError
                case [a, b]:
                    C = [a, *map(f(a, b), range(1,sample)), b, *C]
                    break
                case [a, b, *B]:
                    C = [a, *map(f(a, b), range(1,sample)), *C]
                    B = [b, *B]

        A = concatenate(C, axis=axis)
    return A

def populate_MVT(A, collapse_to, extent, flare):
    for axis in [ax for ax in range(len(A.shape)) if ax != collapse_to]:
        B = array_split(A, A.shape[axis], axis)
        C = B.copy()

        E = []
        while True:
            match B:
                case [] | [_] | [_,_]:
                    raise NotImplementedError
                case [a, b, c]:
                    # This heuristic is reasonable in the instance A is (n, m)
                    # but falls apart for beyond (n, m, ...). Perhaps we should
                    # capture the poles along collapse_to axis and scale c - a 
                    # w.r.t. projection length. i.e. (c - a) * (c - b) dot (c - a)
                    # This would make a rectangular type form over the five points.

                    # in order to do the above computation we're going to have to 
                    # store/collapse elements in the collapse_to elements:
                    #
                    #      A = apply_along_axis(lambda x: lambda _: x, collapse_to, A) 
                    #      B = apply_along_axis(lambda x: lambda _: x, collapse_to, B) 
                    # 
                    # Then applying something of an applicative functor to the two
                    # of them like so
                    #
                    #       f g <$> A <*> B
                    #
                    #   where f g a b =
                    #       let a = a None
                    #           b = b None
                    #       in g a b
                    # --------------------------------
                    #
                    # Note: in python, the provided functions in the storage step can be accessed
                    #           via a(_)

                    e = c - a
                    E = [*E, *(extent * (b - flare*e,)), *(extent * (b,)), *(extent * (b + flare*e,))]
                    break
                case [a, b, c, *B]:
                    e = c - a
                    E = [*E, *(extent * (b - flare*e,)), *(extent * (b,)), *(extent * (b + flare*e,))]
                    B = [b, c, *B]

        # We're going to finish this, but the result is not what I expected.
        # What I'm looking to do next is construct a series of cubic splines
        # and stitch them together in a new piecewise function type. 
        a, *C, c = C
        A = concatenate([a, *E, c], axis=axis)
    return A

def make_closed_MVT(A, axis, flare):
    a, ap, *A, bp = array_split(A, A.shape[axis], axis)
    c = bp - ap
    return concatenate([a, a - flare*c, ap, *A, bp, a + flare*c, a], axis=axis)

def make_closed_LNE(A, axis, t):
    a, *A, b = array_split(A, A.shape[axis], axis)
    c = b - a
    return concatenate([a + t*c, a, *A, b, b - (1 - t)*c], axis=axis)
