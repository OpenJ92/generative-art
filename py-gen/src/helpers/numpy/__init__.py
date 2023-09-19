from numpy import array_split, concatenate, square

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

def populate_MVT(A, collapse_to, flare):
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
                    E = [ *E, (b - flare*e), b, (b + flare*e)]
                    break
                case [a, b, c, *B]:
                    e = c - a
                    E = [ *E, (b - flare*e), b, (b + flare*e)]
                    B = [b, c, *B]

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
    return concatenate([a + t*c, a, *A, b, a + t*c], axis=axis)

def degree_elevation(A, degree, axis):
    pass

