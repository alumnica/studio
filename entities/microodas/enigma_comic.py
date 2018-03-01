from abc import ABC, abstractmethod

from content_organization.structures import MicroODA
from progress import LearnerProgressInMicroODA


class EnigmaComic(MicroODA, ABC):
    @property
    @abstractmethod
    def exercise(self):
        pass

    @property
    @abstractmethod
    def learners_progress_in_enigma_comic(self):
        pass

    @property
    @abstractmethod
    def comic_scenes(self):
        pass


class EnigmaComicScene(ABC):
    @property
    @abstractmethod
    def type(self):
        pass

    @property
    @abstractmethod
    def sequence(self):
        pass

    @property
    @abstractmethod
    def clickable_areas(self):
        pass

    @abstractmethod
    def render(self):
        pass


class EngimaComicClickableArea(ABC):
    @property
    @abstractmethod
    def point0(self):
        pass

    @property
    @abstractmethod
    def point1(self):
        pass

    @property
    @abstractmethod
    def text(self):
        pass

    @property
    @abstractmethod
    def is_correct(self):
        pass


class EnigmaComicStaticScene(EnigmaComicScene, ABC):
    @property
    @abstractmethod
    def background_scene(self):
        pass


class EnigmaComicS360Scene(EnigmaComicScene, ABC):
    @property
    @abstractmethod
    def image_360(self):
        pass


class LearnerProgressInEnigmaComic(LearnerProgressInMicroODA, ABC):
    @property
    @abstractmethod
    def enigma_comic(self):
        pass

    @property
    @abstractmethod
    def exercise_solution(self):
        pass
