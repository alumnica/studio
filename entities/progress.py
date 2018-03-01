from abc import ABC, abstractmethod


class LearnerProgressInODA(ABC):
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
    def microoda_in_progress(self):
        pass

    @abstractmethod
    def get_score(self):
        pass

    @abstractmethod
    def is_complete(self):
        pass


class LearnerProgressInMicroODA(ABC):
    @property
    @abstractmethod
    def learner(self):
        pass

    @property
    @abstractmethod
    def microoda(self):
        pass

    @abstractmethod
    def get_score(self):
        pass

    @abstractmethod
    def is_complete(self):
        pass
