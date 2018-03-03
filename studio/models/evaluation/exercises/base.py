from django.db import models

from alumnica_entities.evaluation.exercises import Exercise, ExerciseType, ExerciseSolution, ExerciseSolutionType


class ExerciseModel(Exercise, models.Model):
    EXERCISE_TYPES = (
        (ExerciseType.CATEGORIZAR.value, ExerciseType.CATEGORIZAR.value),
        (ExerciseType.IMAGE_SELECTION.value, ExerciseType.IMAGE_SELECTION.value),
        (ExerciseType.IMAGE_SORTING.value, ExerciseType.IMAGE_SORTING.value),
    )

    @property
    def name(self):
        return self.name_field

    @property
    def description(self):
        return self.description_field

    @property
    def type(self):
        return self.type_field

    @property
    def exercise_solutions(self):
        return None

    name_field = models.CharField(max_length=100, verbose_name='nombre')
    description_field = models.TextField(blank=True, verbose_name='descripción')
    type_field = models.CharField(max_length=50, choices=EXERCISE_TYPES, verbose_name='tipo')

    class Meta:
        verbose_name = 'ejercicio'
        verbose_name_plural = 'ejercicios'

    def __str__(self):
        return str(self.name)


class ExerciseSolutionModel(ExerciseSolution, models.Model):
    EXERCISE_SOLUTION_TYPES = (
        (ExerciseSolutionType.CATEGORIZAR_SOLUTION.value, ExerciseSolutionType.CATEGORIZAR_SOLUTION.value),
        (ExerciseSolutionType.IMAGE_SELECTION_SOLUTION.value, ExerciseSolutionType.IMAGE_SELECTION_SOLUTION.value),
        (ExerciseSolutionType.IMAGE_SORTING_SOLUTION.value, ExerciseSolutionType.IMAGE_SORTING_SOLUTION.value),
    )

    @property
    def exercise(self):
        return self.exercise_field

    @property
    def type(self):
        return self.type_field

    @property
    def score(self):
        return self.score_field

    exercise_field = models.ForeignKey(ExerciseModel, on_delete=models.CASCADE, verbose_name='ejercicio')
    type_field = models.CharField(max_length=30, choices=EXERCISE_SOLUTION_TYPES, verbose_name='tipo de solución')
    score_field = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='puntuación')

    class Meta:
        verbose_name = 'solución del ejercicio'
        verbose_name_plural = 'soluciones del ejercicio'

    def __str__(self):
        return '{} {}'.format(self.exercise, self.score)
