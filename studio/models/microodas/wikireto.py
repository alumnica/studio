from django.db import models

from alumnica_entities.microodas.wikireto import WikiReto, LearnerProgressInWikiReto


class WikiRetoModel(WikiReto, models.Model):
    @property
    def learners_progress(self):
        raise NotImplementedError()

    @property
    def positive_exercise(self):
        return ...

    @property
    def negative_exercise(self):
        return ...

    class Meta:
        verbose_name = 'wikireto'
        verbose_name_plural = 'wikiretos'

    def __str__(self):
        return str(self.name)


class LearnerProgressInWikiRetoModel(LearnerProgressInWikiReto, models.Model):
    @property
    def wikireto(self):
        return ...

    @property
    def given_definition(self):
        return ...

    @property
    def positive_exercise_solution(self):
        return ...

    @property
    def negative_exercise_solution(self):
        return ...

    class Meta:
        verbose_name = 'progreso del alumno en el wikireto'
        verbose_name_plural = 'el progreso de los alumnos en el wikireto'

    def __str__(self):
        return str(self.name)
