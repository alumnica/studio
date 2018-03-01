from abc import ABC

from entities.content_organization.structures import MicroODA
from entities.progress import LearnerProgressInMicroODA


class Organizador(MicroODA, ABC):
    @property
    def text(self):
        pass

    @property
    def learners_progress_in_organizador(self):
        pass


class LearnerProgressInOrganizador(LearnerProgressInMicroODA, ABC):
    @property
    def chosen_words(self):
        pass

    @property
    def chosen_diagram_type(self):
        pass


class OrganizadorDiagramType:
    @property
    def name(self):
        pass

    @property
    def diagram_assets(self):
        pass


class OrganizadorDiagramTypeAssets:
    @property
    def name(self):
        pass

    @property
    def image(self):
        pass
