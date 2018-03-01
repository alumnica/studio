from django.db import models

from entities.content_organization.presentation import Theme


class ThemeModel(Theme, models.Model):
    @property
    def name(self):
        return self.name_field

    @property
    def primary_color(self):
        return self.primary_color_field

    @property
    def secondary_color(self):
        return self.secondary_color_field

    @property
    def background_image(self):
        return self.background_image_field

    name_field = models.CharField(max_length=100, verbose_name='nombre')
    primary_color_field = models.CharField(max_length=6, verbose_name='color primario')
    secondary_color_field = models.CharField(max_length=6, verbose_name='color secundario')
    background_image_field = models.ImageField(verbose_name='imagen de fondo')

    class Meta:
        verbose_name = 'tema'
        verbose_name_plural = 'temas'

    def __str__(self):
        return str(self.name)