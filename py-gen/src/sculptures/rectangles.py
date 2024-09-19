from src.functions import Bezier, ID, Map
from src.sculptures import FlexPlane
from src.atoms import Point, Segment, List, __Meta_Data__
from src.typeclass import __Sculpture__, __Function__, __Random__

from numpy import array

class Rectangle(__Function__):
    def __init__(self, size):
        self.size = size

    def __call__(self, data: array):
        elements = [None] * self.size
        for index in range(0, self.size):
            length, width = data[2*index], data[2*index+1]
            elements[index] = List([ Segment(array([0,0]),array([length,0]))
                                   , Segment(array([length,0]),array([length, width]))
                                   , Segment(array([length, width]),array([0, width]))
                                   , Segment(array([0, width]),array([0,0]))
                                   ])
            elements[index] = __Meta_Data__(meta = {"color":index}, data = elements[index])
            ## breakpoint()
        return List(elements)

    def __call_data__(self, data):
        match data:
            case Point(l=x):
                return self.__call__(x)
            case _:
                return NotImplementedError

def Rectangles(control_points, nx, ny):
    ## control_points -- expected dimension = (l,m,n) -> n should be a mutiple of three

    rectangles = Bezier()(control_points, (1,2))

    ## This should be a __Function__ with a specialized __call_data__
    ## function which matches on Point __Data__ and calls self with the
    ## following funciton. make :: Point -> List[Segment]

    point = __Sculpture__(Point(array([1,1])), ID())
    data  = __Sculpture__(FlexPlane(point, nx, ny).sculpt(), Map(rectangles))
    data  = __Sculpture__(data.sculpt(), Map(Rectangle(control_points.shape[-1] // 3))).sculpt()

    breakpoint()
