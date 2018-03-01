from abc import ABC, abstractmethod
from enum import Enum


class ExerciseType(Enum):
    CATEGORIZAR = 'Categorizar'
    IMAGE_SELECTION = 'Image Selection'
    IMAGE_SORTING = 'Image Sorting'


class Exercise(ABC):
    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def description(self):
        pass

    @property
    @abstractmethod
    def type(self):
        pass

    @property
    @abstractmethod
    def exercise_solutions(self):
        pass


class ExerciseSolutionType(Enum):
    CATEGORIZAR_SOLUTION = 'Categorizar Solution'
    IMAGE_SELECTION_SOLUTION = 'Image Selection Solution'
    IMAGE_SORTING_SOLUTION = 'Image Sorting Solution'


class ExerciseSolution(ABC):
    @property
    @abstractmethod
    def exercise(self):
        pass

    @property
    @abstractmethod
    def type(self):
        pass

    @property
    @abstractmethod
    def score(self):
        pass
