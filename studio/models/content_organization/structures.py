from django.db import models

from entities.content_organization.presentation import Theme
from entities.content_organization.structures import World, Subworld, ODA, MicroODA, MicroODAType


class WorldModel(World, models.Model):
    @property
    def name(self):
        return self.name_field

    @property
    def description(self):
        return self.description_field

    @property
    def subworlds(self):
        return self.subworldmodel_set.all()

    name_field = models.CharField(max_length=150, verbose_name='nombre')
    description_field = models.TextField(blank=True, verbose_name='descripción')

    class Meta:
        verbose_name = 'mundo'
        verbose_name_plural = 'mundos'

    def __str__(self):
        return str(self.name)


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


class SubworldModel(Subworld, models.Model):
    @property
    def name(self):
        return self.name_field

    @property
    def description(self):
        return self.description_field

    @property
    def theme(self):
        return self.theme_field

    @property
    def world(self):
        return self.world_field

    @property
    def odas(self):
        return

    name_field = models.CharField(max_length=100, verbose_name='nombre')
    description_field = models.TextField(blank=True, verbose_name='descripción')
    theme_field = models.ForeignKey(ThemeModel, on_delete=models.PROTECT, verbose_name='tema')
    world_field = models.ForeignKey(WorldModel, on_delete=models.CASCADE, verbose_name='mundo')

    class Meta:
        verbose_name = 'submundo'
        verbose_name_plural = 'submundos'

    def __str__(self):
        return str(self.name)


class ODAModel(ODA, models.Model):

    @property
    def name(self):
        return self.name_field

    @property
    def description(self):
        return self.description_field

    @property
    def icon(self):
        return self.icon_field

    @property
    def subworld(self):
        return self.subworld_field

    @property
    def micro_odas(self):
        return []

    name_field = models.CharField(max_length=100, verbose_name='nombre')
    description_field = models.TextField(blank=True, verbose_name='descripción')
    icon_field = models.ImageField(verbose_name='ícono')
    subworld_field = models.ForeignKey(SubworldModel, on_delete=models.CASCADE, verbose_name='submundo')

    def is_complete(self):
        return False


class MicroODAModel(MicroODA, models.Model):
    MICROODA_TYPES = (
        (MicroODAType.INTERACTIVE_VIDEO, MicroODAType.INTERACTIVE_VIDEO),
        (MicroODAType.WIKIRETO, MicroODAType.WIKIRETO),
        (MicroODAType.ENIGMA_COMIC, MicroODAType.ENIGMA_COMIC),
        (MicroODAType.MINI_JUEGO, MicroODAType.MINI_JUEGO),
        (MicroODAType.ORGANIZADOR, MicroODAType.ORGANIZADOR),
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
    def default_position(self):
        return self.default_position_field

    @property
    def learners_progress(self):
        return []

    @property
    def oda(self):
        return self.oda_field

    name_field = models.CharField(max_length=100, verbose_name='nombre')
    description_field = models.TextField(blank=True, verbose_name='descripción')
    type_field = models.CharField(max_length=10, choices=MICROODA_TYPES, verbose_name='tipo')
    default_position_field = models.PositiveSmallIntegerField(default=0, verbose_name='posición por defecto')
    oda_field = models.ForeignKey(ODAModel, on_delete=models.CASCADE, verbose_name='ODA')

    class Meta:
        verbose_name = 'microODA'
        verbose_name_plural = 'microODAs'
        abstract = True

    def __str__(self):
        return self.name
