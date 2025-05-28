from src.typeclass import Function
from src.function import Translate, Max

class Frame(Function):
    def __init__(self, dimensions, padding):
        self.width, self.height = dimensions
        self.pad_width, self.pad_height = padding

    def __call__(self, data):
        return data

    def __call_data__(self, data):
        ## We expect that the embeded_dimension of the given data is two
        if data.embeded_dimension != 2:
            raise ValueError

        max_width, max_height = Max(0).call_data(data), Max(1).call_data(data)
        min_width, min_height = Min(0).call_data(data), Min(1).call_data(data)
