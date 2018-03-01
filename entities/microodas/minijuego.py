from abc import ABC

from content_organization.structures import MicroODA
from progress import LearnerProgressInMicroODA


class MiniJuego(MicroODA, ABC):
    @property

    def game_scenes(self):
        pass

    @property

    def learners_progress_in_minijuego(self):
        pass


class MiniJuegoScene:
    @property
    def sequence(self):
        pass

    @property
    def scene_items(self):
        pass


class MiniJuegoSceneItems:
    @property
    def correct_positioning_message(self):
        pass

    @property
    def incorrect_positioning_message(self):
        pass

    @property
    def image(self):
        pass

    @property
    def correct_row_index(self):
        pass

    @property
    def correct_column_index(self):
        pass

    def is_correctly_positioned(self):
        pass


class LearnerProgressInMiniJuego(LearnerProgressInMicroODA, ABC):
    @property
    def minijuego(self):
        pass
