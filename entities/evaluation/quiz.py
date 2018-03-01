from abc import ABC, abstractmethod
from enum import Enum


class LearnerEvaluation(ABC):
    @property
    @abstractmethod
    def learner(self):
        pass

    @property
    @abstractmethod
    def score(self):
        pass

    @property
    @abstractmethod
    def rating_given_by_learner(self):
        pass


class QuestionTypes(Enum):
    MULTIPLE_CHOICE = 'Multiple Choice'
    OPEN_ENDED = 'Open Ended'


class Question(ABC):
    @property
    @abstractmethod
    def text(self):
        pass

    @property
    @abstractmethod
    def type(self):
        pass

    @property
    @abstractmethod
    def microoda(self):
        pass

    @property
    @abstractmethod
    def evaluation(self):
        pass

    @property
    @abstractmethod
    def possible_answers(self):
        pass

    @property
    @abstractmethod
    def given_answers(self):
        pass


class PossibleAnswer(ABC):
    @property
    @abstractmethod
    def question(self):
        pass

    @property
    @abstractmethod
    def text(self):
        pass

    @property
    @abstractmethod
    def is_correct(self):
        pass


class AnswerGivenByLearner(ABC):
    @property
    @abstractmethod
    def answer(self):
        pass

    @property
    @abstractmethod
    def is_correct(self):
        pass

    @property
    @abstractmethod
    def question(self):
        pass

    @property
    @abstractmethod
    def evaluation(self):
        pass
