from abc import ABC, abstractmethod
from numpy import linspace

from src.typeclass import Function, Sculpture
from src.atoms import List

class __Kinetic__:
    def __init__(self, sculpture, __funciton__: Function, __time__: __Function__, samples: int):
        self.sculpture = __sculpture__
        self.__function__  = __function__
        self.__time__      = __time__
        self.samples       = samples

    ## psudo-code (Here we supply a list of frames with sculpture data. The intent is to take
    ## user defined __time__ [0,1] -> Real transform defined [0,1] and __function__ :: Real -> A 
    ## to populate the input of sculpture :: A -> Sculpture. with 
    ## sculpture A :: Sculpture, we call the method sculpt (sculpt $ __sculpture__ A to 
    ## produce our frame. We append the frame for our given time and append to frames. return
    ## to the caller
    def sculpt():
        frames = List([])
        for time in linspace(0, 1, self.samples):
            _time = self.__time__(time)
            _input = self.__function__(_time)
            frames.append(self.sculpture(_input).sculpt())
        return frames

