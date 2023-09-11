
class Barycentric(__Function__):
    def __init__(self, points):
        self.points = points

    def __call__(self, ts):
        ts = Sphere()(ts).square()
