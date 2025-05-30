from src.atoms import dimension, List
from src.typeclass import Function, Sculpture
from src.functions.translate import Translate
from src.functions.scale import Scale
from src.functions.min import Min
from src.functions.max import Max
from src.functions.composition import Composition
from src.sculptures import Rectangle
from numpy import array

class Frame(Function):
    def __init__(self, dimensions, padding):
        self.width, self.height = dimensions
        self.padding = padding

    def __call__(self, data):
        return data

    def call_data(self, data):
        ## We expect that the embeded_dimension of the given data is two
        if dimension(data)!= 2:
            raise ValueError

        max_width, max_height = Max(0).call_data(data), Max(1).call_data(data)
        min_width, min_height = Min(0).call_data(data), Min(1).call_data(data)

        bounded_width = max_width - min_width
        bounded_height = max_height - min_height

        center_width = bounded_width / 2
        center_height = bounded_height / 2

        scale = 1 / bounded_height

        data = Sculpture(data, Translate(array([-(min_width+center_width), -(min_height+center_height)]))).sculpt()
        data = Sculpture(data, Scale(scale*(self.height-(2*self.padding)))).sculpt()
        data = Sculpture(data, Translate(array([self.width/2, self.height/2]))).sculpt()

        return List([data, Rectangle(2)([self.width, self.height])])

