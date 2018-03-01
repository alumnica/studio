from abc import ABC, abstractmethod

from content_organization.structures import MicroODA
from progress import LearnerProgressInMicroODA


class MiniJuego(MicroODA, ABC):
    @property
    @abstractmethod
    def game_scenes(self):
        pass

    @property
    @abstractmethod
    def learners_progress_in_minijuego(self):
        pass


class MiniJuegoScene(ABC):
    @property
    @abstractmethod
    def sequence(self):
        pass

    @property
    @abstractmethod
    def scene_items(self):
        pass


class MiniJuegoSceneItems(ABC):
    @property
    @abstractmethod
    def correct_positioning_message(self):
        pass

    @property
    @abstractmethod
    def incorrect_positioning_message(self):
        pass

    @property
    @abstractmethod
    def image(self):
        pass

    @property
    @abstractmethod
    def correct_row_index(self):
        pass

    @property
    @abstractmethod
    def correct_column_index(self):
        pass

    @abstractmethod
    def is_correctly_positioned(self):
        pass


class LearnerProgressInMiniJuego(LearnerProgressInMicroODA, ABC):
    @property
    @abstractmethod
    def minijuego(self):
        pass
