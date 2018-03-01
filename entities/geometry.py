from abc import ABC, abstractmethod


class Point2D(ABC):
    @property
    @abstractmethod
    def x(self):
        pass

    @property
    @abstractmethod
    def y(self):
        pass
