from abc import ABC

from content_organization.structures import MicroODA
from progress import LearnerProgressInMicroODA


class EnigmaComic(MicroODA, ABC):
    @property
    def exercise(self):
        pass

    @property
    def learners_progress_in_enigma_comic(self):
        pass

    @property
    def comic_scenes(self):
        pass


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


class EnigmaComicStaticScene(EnigmaComicScene, ABC):
    @property
    def background_scene(self):
        pass


class EnigmaComicS360Scene(EnigmaComicScene, ABC):
    @property
    def image_360(self):
        pass


class LearnerProgressInEnigmaComic(LearnerProgressInMicroODA, ABC):
    @property
    def enigma_comic(self):
        pass

    @property
    def exercise_solution(self):
        pass
