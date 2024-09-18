from src.functions import Bezier, ID, Map
from src.sculptures import FlexPlane
from src.atoms import Point, Segment, List
from src.typeclass.__sculpture__ import __Sculpture__

from numpy import array

def Rectangles(control_points, nx, ny):
    ## control_points -- expected dimension = (l,m,n) -> n should be a mutiple of three

    rectangles = Bezier()(control_points, (1,2))

    ## This should be a __Function__ with a specialized __call_data__
    ## function which matches on Point __Data__ and calls self with the
    ## following funciton. make :: Point -> List[Segment]
    def make(vector):
        size, elements = control_points.shape[-1] // 3, []
        for index in range(0, 2*size, 2):
            length, width = vector[index], vector[index+1]
            elements.append(List([ Segment(array([0,0]))
                                 , Segment(array([length,0]))
                                 , Segment(array([0, width]))
                                 , Segment(array([length, width]))
                                 ]))
            breakpoint()

        return elements

    point = __Sculpture__(Point(array([1,1])), ID())
    data  = __Sculpture__(FlexPlane(point, nx, ny).sculpt(), Map(rectangles))
    data  = __Sculpture__(data.sculpt(), Map(make))

    breakpoint()
