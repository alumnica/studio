from django.db import models

from entities.evaluation.quiz import LearnerEvaluation, QuestionTypes, PossibleAnswer, AnswerGivenByLearner
from studio.models import LearnerModel, MicroODAModel


class LearnerEvaluationModel(LearnerEvaluation, models.Model):
    @property
    def learner(self):
        return self.leaner_field

    @property
    def score(self):
        return self.score_field

    @property
    def rating_given_by_leaner(self):
        return self.rating_given_by_leaner_field

    learner_field = models.ForeignKey(LearnerModel, on_delete=models.CASCADE, verbose_name='alumno')
    score_field = models.DecimalField(max_digits=11, decimal_places=2, verbose_name='puntuación')
    rating_given_by_leaner_field = models.Decimal(max_digits=100, decimal_places=2, verbose_name='calificación')

    class Meta:
        verbose_name = 'evaluación del alumno'
        verbose_name_plural = 'evaluaciones del alumno'


class QuestionModel(QuestionTypes, models.Model):
    QUESTION_TYPES = (
        (QuestionTypes.MULTIPLE_CHOICE, QuestionTypes.MULTIPLE_CHOICE),
        (QuestionTypes.OPEN_ENDED, QuestionTypes.OPEN_ENDED),
    )

    @property
    def text(self):
        return self.text_field

    @property
    def type(self):
        return self.type_field

    @property
    def microoda(self):
        return self.microoda_field

    @property
    def evaulation(self):
        return self.evaluation_field

    @property
    def possible_answers(self):
        return self.possibleanswermodel_set.all()

    @property
    def given_answers(self):
        return self.answersgivenbylearnermodel.set.all()

    text_field = models.CharField(max_length=200, verbose_name='texto')
    type_field = models.CharField(max_length=20, choices=QUESTION_TYPES, verbose_name='tipo')
    microoda_field = models.ForeignKey(MicroODAModel, on_delete=models.CASCADE, verbose_name='microODA')
    evaluation_field = models.ForeignKey(LearnerEvaluationModel, on_delete=models.CASCADE, verbose_name='evaluación')

    class Meta:
        verbose_name = 'pregunta'
        verbose_name_plural = 'preguntas'


class PossibleAnswerModel(PossibleAnswer, models.Model):
    @property
    def question(self):
        return self.question_field

    @property
    def text(self):
        return self.text_field

    @property
    def is_correct(self):
        return self.is_correct_field

    question_field = models.ForeignKey(QuestionModel, on_delete=models.CASCADE, verbose_name='pregunta')
    text_field = models.CharField(max_length=200, verbose_name='texto')
    is_correct_field = models.BooleanField(verbose_name='¿es correcto?')

    class Meta:
        verbose_name = 'respuesta posible'
        verbose_name_plural = 'respuestas posibles'


class AnswerGivenByLearnerModel(AnswerGivenByLearner, models.Model):
    @property
    def answer(self):
        return self.answer_field

    @property
    def is_correct(self):
        return self.is_correct

    @property
    def question(self):
        return self.question_field

    @property
    def evaluation(self):
        return self.evaluation_field

    answer_field = models.CharField(max_length=200, verbose_name='respuesta')
    is_correct = models.BooleanField(verbose_name='¿es correcto?')
    question_field = models.ForeignKey(QuestionModel, on_delete=models.CASCADE, verbose_name='pregunta')
    evaluation_field = models.ForeignKey(LearnerEvaluationModel, on_delete=models.CASCADE, verbose_name='evaluación')

    class Meta:
        verbose_name = 'respuesta proporcionada por alumno'
        verbose_name_plural = 'respuestas proporcionadas por alumno'
