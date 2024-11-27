from abc import ABC, abstractmethod


class __Composite__(ABC):
    # From class object produce Data object.
    @abstractmethod
    def composite(self):
        pass
