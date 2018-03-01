from django.db import models

from entities.microodas.minijuego import MiniJuego, MiniJuegoScene, MiniJuegoSceneItem
from studio.models import MicroODAModel


class MiniJuegoModel(MicroODAModel, MiniJuego):
    @property
    def game_scenes(self):
        return self.minijuegoscenemodel_set.all()

    @property
    def learners_progress_in_minijuego(self):
        return None


class MiniJuegoSceneModel(MiniJuegoScene, models.Model):
    @property
    def sequence(self):
        return self.sequence_field

    @property
    def scene_items(self):
        return self.minijuegosceneitemmodel_set.all()

    sequence_field = models.PositiveSmallIntegerField(default=0, verbose_name='número de secuencia')
    minijuego_field = models.ForeignKey(MiniJuegoModel, on_delete=models.CASCADE, verbose_name='miniJuego')

    class Meta:
        verbose_name = 'escena de MiniJuego'
        verbose_name_plural = 'escenas de MiniJuegos'


class MiniJuegoSceneItemModel(MiniJuegoSceneItem, models.Model):
    @property
    def correct_positioning_message(self):
        return self.correct_positioning_message_field

    @property
    def incorrect_positioning_message(self):
        return self.incorrect_positioning_message_field

    @property
    def image(self):
        return self.image_field

    @property
    def correct_row_index(self):
        return self.correct_row_index_field

    @property
    def correct_column_index(self):
        return self.correct_column_index_field

    def is_correctly_positioned(self):
        return False

    correct_positioning_message_field = models.TextField(blank=True, verbose_name='mensaje de éxito')
    incorrect_positioning_message_field = models.TextField(blank=True, verbose_name='mensaje de error')
    image_field = models.ImageField(verbose_name='imagen del sprite')
    correct_row_index_field = models.SmallIntegerField(default=-1, verbose_name='índice de fila correcta')
    correct_column_index_field = models.SmallIntegerField(default=-1, verbose_name='índice de columna correcta')
    scene_field = models.ForeignKey(MiniJuegoSceneModel, on_delete=models.CASCADE, verbose_name='escena del MiniJuego')

    class Meta:
        verbose_name = 'item de escena de 0MiniJuego'
        verbose_name_plural = 'items de escena de MiniJuego'

# class LearnerProgressInMiniJuegoModel(LearnerProgressInMicroODAModel, LearnerProgressInMiniJuego):
#     @property
#     def minijuego(self):
#         pass
