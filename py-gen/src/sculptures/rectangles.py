from src.functions import Bezier, ID, Map, Composition
from src.sculptures import FlexPlane
from src.atoms import Point, Segment, List, __Meta_Data__
from src.typeclass import __Sculpture__, __Function__, __Random__

from numpy import array

class Rectangle(__Function__):
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
            elements[index] = __Meta_Data__(meta={"color":index},data=elements[index])
        return List(elements)

    ## We should consider taking the contents of __call__ and supplying them within
    ## __call_data__. Recall, that __call__ represent transformations of spacial information
    ## and __call_data__ represent transformations of __Data__ information. Rectangle is
    ## taking the spacial information of array and CONSTRUCTING __Data__. 
    def __call_data__(self, data):
        match data:
            case Point(l=x):
                return self.__call__(x)
            case _:
                return NotImplementedError

def Rectangles(control_points, nx, ny):
    ## control_points -- expected dimension = (l,m,n) -> n should be a mutiple of two

    information = Bezier()(control_points, (1,2))

    points = FlexPlane(__Sculpture__(Point(array([1,1])), ID()), nx, ny).sculpt()
    function = Composition([Map(information), Map(Rectangle(control_points.shape[-1]))])

    data  = __Sculpture__(points, function).sculpt()
    return data

