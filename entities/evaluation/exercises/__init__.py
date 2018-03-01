from enum import Enum


class ExerciseType(Enum):
    CATEGORIZAR = 'Categorizar'
    IMAGE_SELECTION = 'Selección de Imágenes'
    IMAGE_SORTING = 'Ordenamiento de Imágenes'


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
    CATEGORIZAR_SOLUTION = 'Categorizar'
    IMAGE_SELECTION_SOLUTION = 'Selección de Imágenes'
    IMAGE_SORTING_SOLUTION = 'Ordenamiento de Imágenes'


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
