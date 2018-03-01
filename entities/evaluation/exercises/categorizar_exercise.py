from abc import ABC, abstractmethod

from evaluation.exercises import Exercise, ExerciseSolution


class CategorizarExercise(Exercise, ABC):
    @property
    @abstractmethod
    def categories(self):
        pass

    @property
    @abstractmethod
    def exercise_solutions(self):
        pass


class CategorizarExerciseCategory(ABC):
    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def elements(self):
        pass


class CategorizableElement(ABC):
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
    def category(self):
        pass


class CategorizarExerciseSolution(ExerciseSolution, ABC):
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
