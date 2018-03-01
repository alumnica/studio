from abc import ABC

from content_organization.structures import MicroODA
from progress import LearnerProgressInMicroODA


class WikiReto(MicroODA, ABC):
    @property
    def learners_progress(self):
        pass

    @property
    def positive_exercise(self):
        pass

    @property
    def negative_exercise(self):
        pass


class LearnerProgressInWikiReto(LearnerProgressInMicroODA, ABC):
    @property
    def wikireto(self):
        pass

    @property
    def given_definition(self):
        pass

    @property
    def positive_exercise_solution(self):
        pass

    @property
    def negative_exercise_solution(self):
        pass
