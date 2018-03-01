from django.db import models

from entities.microodas.enigma_comic import EnigmaComic, EnigmaComicScene, EnigmaComicSceneType, \
    EngimaComicClickableArea, EnigmaComicStaticScene, EnigmaComicS360Scene
from studio.models import MicroODAModel
from studio.models.evaluation.exercises import ExerciseModel
from studio.models.geometry import Point2DModel


class EnigmaComicModel(MicroODAModel, EnigmaComic):
    @property
    def exercise(self):
        return self.exercise_field

    @property
    def learners_progress_in_enigma_comic(self):
        return None

    @property
    def comic_scenes(self):
        return None

    exercise_field = models.ForeignKey(ExerciseModel, on_delete=models.PROTECT, verbose_name='ejercicio')

    class Meta:
        verbose_name = 'cómic Enigma'
        verbose_name_plural = 'cómics Enigma'

    def __str__(self):
        return str(self.name)


class EnigmaComicSceneModel(EnigmaComicScene, models.Model):
    SCENE_TYPES = (
        (EnigmaComicSceneType.STATIC_SCENE.value, EnigmaComicSceneType.STATIC_SCENE.value),
        (EnigmaComicSceneType.SCENE_360.value, EnigmaComicSceneType.SCENE_360.value),
    )

    @property
    def type(self):
        return self.type_field

    @property
    def sequence(self):
        return self.sequence_field

    @property
    def clickable_areas(self):
        return None

    def render(self):
        pass

    type_field = models.CharField(max_length=20, choices=SCENE_TYPES, verbose_name='tipo de escena')
    sequence_field = models.PositiveSmallIntegerField(default=0, verbose_name='número de secuencia')
    enigma_comic_field = models.ForeignKey(EnigmaComicModel, on_delete=models.CASCADE, verbose_name='cómic Enigma')

    class Meta:
        verbose_name = 'escena de cómic Enigma'
        verbose_name_plural = 'escenas de cómic Enigma'
        abstract = True

    def __str__(self):
        return '{} - {}'.format(self.enigma_comic_field.name, self.type)


class EnigmaComicClickableAreaModel(EngimaComicClickableArea, models.Model):
    @property
    def point0(self):
        return self.point0_field

    @property
    def point1(self):
        return self.point1_field

    @property
    def text(self):
        return self.text_field

    @property
    def is_correct(self):
        return self.is_correct_field

    point0_field = models.ForeignKey(Point2DModel, on_delete=models.PROTECT, related_name='points_as_x',
                                     verbose_name='punto 0')
    point1_field = models.ForeignKey(Point2DModel, on_delete=models.PROTECT, related_name='points_as_y',
                                     verbose_name='punto 1')
    text_field = models.TextField(verbose_name='texto')
    is_correct_field = models.BooleanField(default=False, verbose_name='es correcta')

    class Meta:
        verbose_name = 'área cliqueable de un cómic Enigma'
        verbose_name_plural = 'áreas cliqueables de un cómic Enigma'

    def __str__(self):
        return self.text_field


class EngimaComicStaticSceneModel(EnigmaComicSceneModel, EnigmaComicStaticScene):
    @property
    def background_scene(self):
        return self.background_scene_field

    background_scene_field = models.ImageField(verbose_name='imagen de fondo')

    class Meta:
        verbose_name = 'escena estática de un cómic Enigma'
        verbose_name_plural = 'escenas estáticas de un cómic Enigma'


class EnigmaComicS360SceneModel(EnigmaComicSceneModel, EnigmaComicS360Scene):
    @property
    def image_360(self):
        return self.image_360_field

    image_360_field = models.ImageField(verbose_name='imagen 360')

    class Meta:
        verbose_name = 'escena 360 de un cómic Enigma'
        verbose_name_plural = 'escenas 360 de un cómic Enigma'
