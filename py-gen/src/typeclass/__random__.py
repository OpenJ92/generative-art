from abc import ABC, abstractmethod


class __Random__(ABC):
    @classmethod
    @abstractmethod
    def random():
        raise NotImplementedError
