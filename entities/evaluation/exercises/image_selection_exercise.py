from abc import ABC, abstractmethod

from evaluation.exercises import Exercise, ExerciseSolution


class ImageSelectionExercise(Exercise, ABC):
    @property
    @abstractmethod
    def selectable_images(self):
        pass


class SelectableImage(ABC):
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
    def is_correct(self):
        pass

    @property
    @abstractmethod
    def exercise(self):
        pass


class ImageSelectionExerciseSolution(ExerciseSolution, ABC):
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
