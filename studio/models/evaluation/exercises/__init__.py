from django.db import models

from entities.evaluation.exercises import Exercise, ExerciseType, ExerciseSolution, ExerciseSolutionType


class ExerciseModel(Exercise, models.Model):
    EXERCISE_TYPES = (
        (ExerciseType.CATEGORIZAR, ExerciseType.CATEGORIZAR),
        (ExerciseType.IMAGE_SELECTION, ExerciseType.IMAGE_SELECTION),
        (ExerciseType.IMAGE_SORTING, ExerciseType.IMAGE_SORTING),
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
    type_field = models.CharField(max_length=20, choices=EXERCISE_TYPES,verbose_name='tipo')

    class Meta:
        verbose_name = 'ejercicio'
        verbose_name_plural = 'ejercicios'
        abstract = True

    def __str__(self):
        return self.name

class ExerciseSolutionModel(ExerciseSolution, models.Model):
    EXERCISESOLUTION_TYPES = (
        (ExerciseSolutionType.CATEGORIZAR_SOLUTION, ExerciseSolutionType.CATEGORIZAR_SOLUTION),
        (ExerciseSolutionType.IMAGE_SELECTION_SOLUTION, ExerciseSolutionType.IMAGE_SELECTION_SOLUTION),
        (ExerciseSolutionType.IMAGE_SORTING_SOLUTION, ExerciseSolutionType.IMAGE_SORTING_SOLUTION),
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
    type_field = models.CharField(max_length=30, choices=EXERCISESOLUTION_TYPES,verbose_name='tipo de solución')
    score_field = models.DecimalField(verbose_name='puntuación')

    class Meta:
        verbose_name = 'solución del ejercicio'
        verbose_name_plural = 'soluciones del ejercicio'
        abstract = True

    def __str__(self):
        return str(self.name)