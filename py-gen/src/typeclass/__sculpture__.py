from abc import ABC, abstractmethod

from src.atoms import __Data__
from src.typeclass.__function__ import Function


class Sculpture:
    def __init__(self, __data__: __Data__, __function__: Function):
        self.__data__ = __data__
        self.__function__ = __function__

    def sculpt(self) -> __Data__:
        return self.__function__.__call_data__(self.__data__)


#### consider how we might reconstruct sculpture s.t. the implementation below
#### would work. Get a 'lazy' sort of construction.
## class Sculpture():
##     def __init__(self, __data__: __Data__, __function__: Function):
##         self.__data__ = __data__
##         self.__function__ = __function__
##
##     def sculpt(self) -> __Data__:
##         return self.__function__.__call_data__(self.__data__.sculpt())
