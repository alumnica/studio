from django.db import models

from entities.ratings import LearnerODARating, LearnerMicroODARating
from studio.models import LearnerModel, ODAModel


class LearnerODARatingModel(LearnerODARating, models.Model):
    @property
    def learner(self):
        return self.learner_field

    @property
    def oda(self):
        return self.oda_field

    @property
    def rating(self):
        return self.rating_field

    learner_field = models.ForeignKey(LearnerModel, on_delete=models.CASCADE, verbose_name='alumno')
    oda_field = models.ForeignKey(ODAModel, on_delete=models.CASCADE, verbose_name='ODA')
    rating_field = models.DemicalField(max_digits=100, decimal_places=2, verbose_name='calificación')

    class Meta:
        verbose_name = 'calificación de ODA del alumno'
        verbose_name_plural = 'calificaciones de ODA del alumno'

class LearnerMicroODARatingModel(LearnerMicroODARating, models.Model):
    @property
    def learner(self):
        return self.learner_field

    @property
    def microoda(self):
        return self.microoda_field

    @property
    def rating(self):
        return self.rating_field

    learner_field = models.ForeignKey(LearnerModel, on_delete=models.CASCADE, verbose_name='alumno')
    microoda_field = models.ForeignKey(MicroODAModel, on_delete=models.CASCADE, verbose_name='microODA')
    rating_field = models.DemicalField(max_digits=100, decimal_places=2, verbose_name='calificación')

    class Meta:
        verbose_name = 'calificación de microODA del alumno'
        verbose_name_plural = 'calificaciones de microODA del alumno'