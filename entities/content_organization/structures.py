from abc import ABC, abstractmethod


class World(ABC):
    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def description(self):
        pass

    @property
    @abstractmethod
    def subworlds(self):
        pass


class Subworld(ABC):
    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def description(self):
        pass

    @property
    @abstractmethod
    def theme(self):
        pass

    @property
    @abstractmethod
    def world(self):
        pass

    @property
    @abstractmethod
    def odas(self):
        pass


class ODA(ABC):
    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def description(self):
        pass

    @property
    @abstractmethod
    def icon(self):
        pass

    @property
    @abstractmethod
    def subworld(self):
        pass

    @property
    @abstractmethod
    def micro_odas(self):
        pass

    @abstractmethod
    def is_complete(self):
        pass


class MicroODA(ABC):
    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def description(self):
        pass

    @property
    @abstractmethod
    def type(self):
        pass

    @property
    @abstractmethod
    def default_position(self):
        pass

    @property
    @abstractmethod
    def learners_progress(self):
        pass
