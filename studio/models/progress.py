from django.db import models

from entities.progress import LearnerProgressInODA, LearnerProgressInMicroODA
from studio.models import LearnerModel, MicroODAModel, ODAModel


class LearnerProgressInODAModel(LearnerProgressInODA, models.Model):
    @property
    def learner(self):
        return self.learner_field

    @property
    def oda(self):
        return self.oda_field

    @property
    def microoda_in_progress(self):
        return self.microoda_in_progress_field

    @property
    def get_score(self):
        return self.get_score_field

    @property
    def is_complete(self):
        return self.is_complete_field

    learner_field = models.ForeignKey(LearnerModel, on_delete=models.CASCADE, verbose_name='alumno')
    oda_field = models.ForeignKey(ODAModel, on_delete=models.CASCADE, verbose_name='ODA')
    microoda_in_progress_field = models.ForeignKey(MicroODAModel, on_delete=models.CASCADE, null=True, blank=True,
                                                   verbose_name='microODA en progreso')
    get_score_field = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='obtener puntuación')
    is_complete_field = models.BooleanField(verbose_name='¿es completo?')

    class Meta:
        verbose_name = 'progreso del alumno en ODA'
        verbose_name_plural = 'progresos del alumno en ODA'

    def __str__(self):
        return str(self.name)


class LearnerProgressInMicroODAModel(LearnerProgressInMicroODA, models.Model):
    @property
    def learner(self):
        return self.learner_field

    @property
    def microoda(self):
        return self.microoda_field

    @property
    def get_score(self):
        return self.get_score_field

    @property
    def is_complete(self):
        return self.is_complete_field

    learner_field = models.ForeignKey(LearnerModel, on_delete=models.CASCADE, verbose_name='alumno')
    microoda_field = models.ForeignKey(MicroODAModel, on_delete=models.CASCADE, verbose_name='microODA')
    get_score_field = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='obtener puntuación')
    is_complete_field = models.BooleanField(verbose_name='¿es completo?')

    class Meta:
        verbose_name = 'progreso del alumno en microODA'
        verbose_name_plural = 'progresos del alumno en microODA'

    def __str__(self):
        return str(self.name)
