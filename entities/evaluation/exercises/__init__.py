from enum import Enum


class ExerciseType(Enum):
    CATEGORIZAR = 'Categorizar'
    IMAGE_SELECTION = 'Image Selection'
    IMAGE_SORTING = 'Image Sorting'


class Exercise:
    @property

    def name(self):
        pass

    @property
    def description(self):
        pass

    @property
    def type(self):
        pass

    @property
    def exercise_solutions(self):
        pass


class ExerciseSolutionType(Enum):
    CATEGORIZAR_SOLUTION = 'Categorizar Solution'
    IMAGE_SELECTION_SOLUTION = 'Image Selection Solution'
    IMAGE_SORTING_SOLUTION = 'Image Sorting Solution'


class ExerciseSolution:
    @property
    def exercise(self):
        pass

    @property
    def type(self):
        pass

    @property
    def score(self):
        pass
