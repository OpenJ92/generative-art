from abc import ABC, abstractmethod
from numpy import linspace

from src.atoms import List

class __Kinetic__:
    def __init__(self, sculpture, __funciton__: Function, __time__: __Function__, samples: int):
        self.sculpture = __sculpture__
        self.function  = __function__
        self.__time__      = __time__
        self.samples       = samples

    ## psudo-code (Here we supply a list of frames with sculpture data. The intent is to take
    ## user defined __time__ [0,1] -> Real transform defined [0,1] and function :: Real -> A 
    ## to populate the input of sculpture :: A -> Sculpture. with 
    ## sculpture A :: Sculpture, we call the method sculpt (sculpt $ __sculpture__ A to 
    ## produce our frame. We append the frame for our given time and append to frames. return
    ## to the caller
    def sculpt():
        frames = List([])
        for time in linspace(0, 1, self.samples):
            _time = self.__time__(time)
            _input = self.function(_time)
            frames.append(self.sculpture(_input).sculpt())
        return frames


class Kinetic:
    def __init__(self, frames, timeFunction, kineticFunction, timeData, kineticData):
        """
        frames :: Int
        timeFunction :: Float -> a
        timeData :: Float -> a
        kineticFunction :: a -> Function
        kineticData :: a -> Data
        """
        self.frames = frames
        self.timeFunction = timeFunction
        self.kineticFunction = kineticFunction
        self.timeData = timeData
        self.kineticData = kineticData

    def sculpt(self):
        samples = linspace(0,1,self.frames)
        sculptures = List([])
        for sample in samples:
            function = self.kineticFunction(self.timeFunction(sample))
            data = self.kineticData(self.timeData(sample))

            sculpture = Sculpture(data, function).sculpt()
            sculptures.elements.append(sculpture)

        return sculptures

