from enum import Enum

from entities.content_organization.structures import MicroODA
from entities.progress import LearnerProgressInMicroODA


class EnigmaComic(MicroODA):
    @property
    def exercise(self):
        pass

    @property
    def learners_progress_in_enigma_comic(self):
        pass

    @property
    def comic_scenes(self):
        pass


class EnigmaComicSceneType(Enum):
    STATIC_SCENE = 'Escena estática'
    SCENE_360 = 'Escena 360'


class EnigmaComicScene:
    @property
    def type(self):
        pass

    @property
    def sequence(self):
        pass

    @property
    def clickable_areas(self):
        pass

    def render(self):
        pass


class EngimaComicClickableArea:
    @property
    def point0(self):
        pass

    @property
    def point1(self):
        pass

    @property
    def text(self):
        pass

    @property
    def is_correct(self):
        pass


class EnigmaComicStaticScene(EnigmaComicScene):
    @property
    def background_scene(self):
        pass


class EnigmaComicS360Scene(EnigmaComicScene):
    @property
    def image_360(self):
        pass


class LearnerProgressInEnigmaComic(LearnerProgressInMicroODA):
    @property
    def enigma_comic(self):
        pass

    @property
    def exercise_solution(self):
        pass
