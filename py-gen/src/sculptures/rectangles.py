from src.functions import Bezier, ID, Composition, Translate
from src.functions.map import Map
from src.functions.zipapply import ZipApply
from src.sculptures import FlexPlane
from src.atoms import Point, Segment, List, Meta_Data
from src.typeclass import Sculpture, Function, Random

from collections import defaultdict
from numpy import array

class Rectangle(Function):
    def __init__(self, size):
        self.size = size

    def __call__(self, data: array):
        elements = [None] * (self.size // 2)
        for index in range(0, self.size // 2):
            length, width = data[2*index], data[2*index+1]
            elements[index] = List([ Segment(array([0,0]),array([length,0]))
                                   , Segment(array([length,0]),array([length, width]))
                                   , Segment(array([length, width]),array([0, width]))
                                   , Segment(array([0, width]),array([0,0]))
                                   ])
            elements[index] = Meta_Data(meta={"stroke":index},data=elements[index])
        return List(elements)

    ## We should consider taking the contents of __call__ and supplying them within
    ## call_data. Recall, that __call__ represent transformations of spacial information
    ## and call_data represent transformations of Data information. Rectangle is
    ## taking the spacial information of array and CONSTRUCTING Data. 
    def call_data(self, data):
        match data:
            case Point(l=x):
                return self.__call__(x)
            case _:
                return NotImplementedError

class Rectangles(Sculpture, Random):
    ## control_points -- expected dimension = (l,m,n) -> n should be a mutiple of two
    def __init__(self, control_points, nx, ny):
        self.control_points = control_points
        self.nx = nx
        self.ny = ny

    def sculpt(self):
        information = Bezier()(self.control_points, (1,2))

        points = FlexPlane(Sculpture(Point(array([1,1])), ID()), self.nx, self.ny).sculpt()
        function = Composition([Map(information), Map(Rectangle(self.control_points.shape[-1]))])
        data  = Sculpture(points, function).sculpt()

        translates = []
        for point in points.elements:
            translates.append(Translate(point.l))

        rectangles = Sculpture(data, ZipApply(translates)).sculpt()

        color_rectangles = defaultdict(list)
        for batch in rectangles.elements:
            for color in batch.elements:
                color_rectangles[color.meta['stroke']].append(color)

        rectangles = []
        for color in color_rectangles.values():
            rectangles.append(List(color))

        return List(rectangles)

    def random(cls):
        raise NotImplementedError


# class Motion_Rectangles(__Kinetic__, Random):
#     def __init__(self):
#         pass
# 
#     def random(cls):
#         raise NotImplementedError

