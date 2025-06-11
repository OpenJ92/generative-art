from src.typeclass import Function
from src.executors import Sculpture
from src.atoms import List
from src.functions.translate import Translate
from src.functions.zipapply import ZipApply

from numpy import array

class Tile(Function):
    def __init__(self, tiling, sizes):
        self.width, self.height = tiling
        self.frame_width, self.frame_height = sizes

    def __call__(self, data):
        return data

    def call_data(self, data):
        match data:
            case List():
                return self.operate(data)
            case _:
                raise ValueError

    def operate(self, data):
        translates = []
        for w in range(self.width):
            for h in range(self.height):
                translate = Translate(array([w*self.frame_width, h*self.frame_height]))
                translates.append(translate)

        return Sculpture(data, ZipApply(translates)).sculpt()
