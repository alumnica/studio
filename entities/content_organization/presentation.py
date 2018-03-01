from abc import ABC, abstractmethod


class Theme(ABC):
    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def primary_color(self):
        pass

    @property
    @abstractmethod
    def secondary_color(self):
        pass

    @property
    @abstractmethod
    def background_image(self):
        pass
