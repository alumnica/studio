from abc import ABC, abstractmethod

from content_organization.structures import MicroODA
from progress import LearnerProgressInMicroODA


class Organizador(MicroODA, ABC):
    @property
    @abstractmethod
    def text(self):
        pass

    @property
    @abstractmethod
    def learners_progress_in_organizador(self):
        pass


class LearnerProgressInOrganizador(LearnerProgressInMicroODA, ABC):
    @property
    @abstractmethod
    def chosen_words(self):
        pass

    @property
    @abstractmethod
    def chosen_diagram_type(self):
        pass


class OrganizadorDiagramType(ABC):
    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def diagram_assets(self):
        pass


class OrganizadorDiagramTypeAssets(ABC):
    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def image(self):
        pass
