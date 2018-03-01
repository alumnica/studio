from abc import ABC

from evaluation.exercises import Exercise, ExerciseSolution


class CategorizarExercise(Exercise, ABC):
    @property

    def categories(self):
        pass

    @property

    def exercise_solutions(self):
        pass


class CategorizarExerciseCategory:
    @property
    def name(self):
        pass

    @property
    def elements(self):
        pass


class CategorizableElement:
    @property
    def name(self):
        pass

    @property
    def image(self):
        pass

    @property
    def category(self):
        pass


class CategorizarExerciseSolution(ExerciseSolution, ABC):
    @property
    def exercise(self):
        pass

    @property
    def type(self):
        pass

    @property
    def score(self):
        pass
