from src.typeclass import Function
from src.function import Translate, Scale, Min, Max, Composition
from src.Sculpture

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

        total_width = max_width - min_width
        total_height = max_height - min_height

        if total_width > total_height:
            side, select = (self.width - 2*self.pad_width, total_width)
        else:
            side, select = (self.height - 2*self.pad_height, total_height)

        scale = 1 / select

        data = Sculpture(Translate(array([-min_width, -min_height])), data).sculpt()
        data = Sculpture(Composition([Scale(scale), Scale(side)]), data).sculpt()
        data = Sculpture(Translate(array([self.pad_width, self.pad_height])), data).sculpt()

        return List([data, Rectangle([self.width, self.height])])

