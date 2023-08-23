from numpy import array_split, concatenate, square

## Functor | Applicative Numpy A forms need to be constructed
## iteration -- product(*map(lambda x: list(range(x)),A.shape))
##           -- A[(slice(10),2,slice(10),1)] == A[:,2,:,1]

def condense(A, dims):
    shape = A.shape
    ranges = map(range, shape)
    slices = map(slice, shape)

    ## this is a really interesting algo. Take some time to think.

def linear_interpolate(A, collapse_axes, samples):
    for axis, sample in zip(collapse_axes, samples):
        B = array_split(A, A.shape[axis], axis)
        f = lambda a, b: lambda t: a + (t/sample)*(b - a)

        C = []
        while True:
            match B:
                case [] | [_]:
                    break
                case [a, b]:
                    C = [a, *map(f(a, b), range(1,sample)), b, *C]
                    break
                case [a, b, *B]:
                    C = [a, *map(f(a, b), range(1,sample)), *C]
                    B = [b, *B]

        A = concatenate(C, axis=axis)
    return A

def populate_average_tangents(A, collapse_to):
    for axis in [ax for ax in range(len(A.shape)) if ax != collapse_to]:
        B = array_split(A, A.shape[axis], axis)

        E = []
        while True:
            match B:
                case [] | [_] | [_,_]:
                    break
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

                    e = c - a / square(c - a).sum()
                    print(b - e, b, b + e)
                    E = [*E, b - e, b, b + e]
                    break
                case [a, b, c, *B]:
                    e = c - a / square(c - a).sum()
                    print(b - e, b, b + e)
                    E = [*E, b - e, b, b + e]
                    B = [b, c, *B]

        breakpoint()
        a, *B, c = B
        A = concatenate([a, *E, c], axis=axis)
    return A
