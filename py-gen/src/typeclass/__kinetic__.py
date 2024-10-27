from abc import ABC, abstractmethod
from numpy import linspace

from src.typeclass import __Function__, __Sculpture__
from src.atoms import List

class __Kinetic__:
    def __init__(self, __sculpture__, __funciton__: __Function__, __time__: __Function__, samples: int):
        self.__sculpture__ = __sculpture__
        self.__function__  = __function__
        self.__time__      = __time__
        self.samples       = samples

    ## psudo-code (Here we supply a list of frames with sculpture data. The intent is to take
    ## user defined __time__ [0,1] -> Real transform defined [0,1] and __function__ :: Real -> A 
    ## to populate the input of __sculpture__ :: A -> __Sculpture__. with 
    ## __sculpture__ A :: __Sculpture__, we call the method sculpt (sculpt $ __sculpture__ A to 
    ## produce our frame. We append the frame for our given time and append to frames. return
    ## to the caller
    def sculpt():
        frames = List([])
        for time in linspace(0, 1, self.samples):
            _time = self.__time__(time)
            _input = self.__function__(_time)
            frames.append(self.__sculpture__(_input).sculpt())
        return frames

