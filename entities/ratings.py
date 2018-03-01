from abc import ABC, abstractmethod


class LearnerODARating(ABC):
    @property
    @abstractmethod
    def learner(self):
        pass

    @property
    @abstractmethod
    def oda(self):
        pass

    @property
    @abstractmethod
    def rating(self):
        pass


class LearnerMicroODARating(ABC):
    @property
    @abstractmethod
    def learner(self):
        pass

    @property
    @abstractmethod
    def oda(self):
        pass

    @property
    @abstractmethod
    def rating(self):
        pass
