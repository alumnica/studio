from abc import ABC, abstractmethod

from evaluation.exercises import Exercise, ExerciseSolution


class ImageSortingExercise(Exercise, ABC):
    @property
    @abstractmethod
    def sortable_images(self):
        pass


class SortableImage(ABC):
    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def image(self):
        pass

    @property
    @abstractmethod
    def correct_sequence(self):
        pass

    @property
    @abstractmethod
    def score(self):
        pass

    @property
    @abstractmethod
    def exercise(self):
        pass


class ImageSortingExerciseSolution(ExerciseSolution, ABC):
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
