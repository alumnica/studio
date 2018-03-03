from django.db import models

from alumnica_entities.geometry import Point2D


class Point2DModel(Point2D, models.Model):

    @property
    def x(self):
        return self.x_field

    def y(self):
        return self.y_field

    x_field = models.DecimalField(max_digits=8, decimal_places=4, verbose_name='coordenada x')
    y_field = models.DecimalField(max_digits=8, decimal_places=4, verbose_name='coordenada y')

    class Meta:
        verbose_name = 'coordenadas'
        verbose_name_plural = 'par de coordenadas'

    def __str__(self):
        return '{0},{1}'.format(self.x_field, self.y_field)
