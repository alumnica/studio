from abc import ABC

from evaluation.exercises import Exercise, ExerciseSolution


class ImageSelectionExercise(Exercise, ABC):
    @property

    def selectable_images(self):
        pass


class SelectableImage:
    @property
    def name(self):
        pass

    @property
    def image(self):
        pass

    @property
    def is_correct(self):
        pass

    @property
    def exercise(self):
        pass


class ImageSelectionExerciseSolution(ExerciseSolution, ABC):
    @property
    def exercise(self):
        pass

    @property
    def type(self):
        pass

    @property
    def score(self):
        pass
