from abc import ABC

from evaluation.exercises import Exercise, ExerciseSolution


class ImageSortingExercise(Exercise, ABC):
    @property

    def sortable_images(self):
        pass


class SortableImage:
    @property
    def name(self):
        pass

    @property
    def image(self):
        pass

    @property
    def correct_sequence(self):
        pass

    @property
    def score(self):
        pass

    @property
    def exercise(self):
        pass


class ImageSortingExerciseSolution(ExerciseSolution, ABC):
    @property
    def exercise(self):
        pass

    @property
    def type(self):
        pass

    @property
    def score(self):
        pass
