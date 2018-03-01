from enum import Enum


class LearnerEvaluation:
    @property

    def learner(self):
        pass

    @property

    def score(self):
        pass

    @property

    def rating_given_by_learner(self):
        pass


class QuestionTypes(Enum):
    MULTIPLE_CHOICE = 'Multiple Choice'
    OPEN_ENDED = 'Open Ended'


class Question:
    @property
    def text(self):
        pass

    @property
    def type(self):
        pass

    @property
    def microoda(self):
        pass

    @property
    def evaluation(self):
        pass

    @property
    def possible_answers(self):
        pass

    @property
    def given_answers(self):
        pass


class PossibleAnswer:
    @property
    def question(self):
        pass

    @property
    def text(self):
        pass

    @property
    def is_correct(self):
        pass


class AnswerGivenByLearner:
    @property
    def answer(self):
        pass

    @property
    def is_correct(self):
        pass

    @property
    def question(self):
        pass

    @property
    def evaluation(self):
        pass
