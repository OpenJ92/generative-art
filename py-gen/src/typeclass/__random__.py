from abc import ABC, abstractmethod


class Random(ABC):
    @classmethod
    @abstractmethod
    def random():
        raise NotImplementedError
