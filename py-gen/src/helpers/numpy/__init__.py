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

## Extent is imaterial here having found RationalBezier. Look to reconstruct here.
## What's more, there is a way to make any n-order into an n+m order according to 
## wiki. Look to reimplement here and make RationalBezier in bezier file
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
                    e = c - a
                    E = [ *E
                        , extent * (b - flare*e)
                        , extent *  b
                        , extent * (b + flare*e)
                        ]

                    break
                case [a, b, c, *B]:
                    e = c - a
                    E = [ *E
                        , extent * (b - flare*e)
                        , extent * b
                        , extent * (b + flare*e)
                        ]
                    B = [b, c, *B]

        # We're going to finish this, but the result is not what I expected.
        # What I'm looking to do next is construct a series of cubic splines
        # and stitch them together in a new piecewise function type. 
        a, *C, c = C
        A = concatenate([extent * a, *E, extent * c], axis=axis)
        ## A = concatenate([a, *E, c], axis=axis)
        print(A)
    return A

## Perhaps we need to include extent and flare to this function with initial values 1. Then we can
## use it in a poulate_closed_MVT function which has an awareness of the extent/flare used on the
## original MDA. Here we cant figure b/c of that unknown. We're assuming those values are one.
def make_closed_MVT(A, axis, flare):
    a, ap, *A, bp = array_split(A, A.shape[axis], axis)
    c = bp - ap
    return concatenate([a, a - flare*c, ap, *A, bp, a + flare*c, a], axis=axis)

def make_closed_LNE(A, axis, t):
    a, *A, b = array_split(A, A.shape[axis], axis)
    c = b - a
    return concatenate([a + t*c, a, *A, b, a + t*c], axis=axis)

# Should we be weighting the first and last components of the bezier ndarray?
## This is incorrect. This process has to happen at evaluation time. See Wiki: Rational Bezier

## There's an odd thing about this evaluation thing. There's got to be a way to capture the
## RationalBezier form in the tensor control_points. 
def rational(A, weights, axis):
    if A.shape[axis] != len(weights):
        raise ValueError(f"Shape of A in axis: {axis} not equal to length of weights: {len(weights)}")
    splitA = array_split(A, A.shape[axis], axis)
    weightedA = [weight*split for weight, split in zip(weights, splitA)]
    return concatenate(weightedA, axis=axis)

def degree_elevation(A, degree, axis):
    pass

