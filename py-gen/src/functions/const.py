from src.typeclass import Function


class Const(Function):
    def __init__(self, item):
        self.item = item

    def __call__(self, data):
        return self.item
