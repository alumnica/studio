from abc import ABC, abstractmethod

from content_organization.structures import MicroODA
from progress import LearnerProgressInMicroODA


class WikiReto(MicroODA, ABC):
    @property
    @abstractmethod
    def learners_progress(self):
        pass

    @property
    @abstractmethod
    def positive_exercise(self):
        pass

    @property
    @abstractmethod
    def negative_exercise(self):
        pass


class LearnerProgressInWikiReto(LearnerProgressInMicroODA, ABC):
    @property
    @abstractmethod
    def wikireto(self):
        pass

    @property
    @abstractmethod
    def given_definition(self):
        pass

    @property
    @abstractmethod
    def positive_exercise_solution(self):
        pass

    @property
    @abstractmethod
    def negative_exercise_solution(self):
        pass
