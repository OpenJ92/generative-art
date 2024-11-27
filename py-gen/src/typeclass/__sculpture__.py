from abc import ABC, abstractmethod

from src.atoms import Data
from src.typeclass.function import Function


class Sculpture:
    def __init__(self, data: Data, function: Function):
        self.data = __data__
        self.function = __function__

    def sculpt(self) -> Data:
        return self.function.call_data(self.data)


#### consider how we might reconstruct sculpture s.t. the implementation below
#### would work. Get a 'lazy' sort of construction.
## class Sculpture():
##     def __init__(self, data: Data, function: Function):
##         self.data = __data__
##         self.function = __function__
##
##     def sculpt(self) -> Data:
##         return self.function.call_data(self.data.sculpt())
