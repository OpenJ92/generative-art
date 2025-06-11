from abc import ABC, abstractmethod

class Executor(ABC):
    @abstractmethod
    def sculpt(self):
        raise NotImplementedError

