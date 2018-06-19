import os
import xlrd
import json
from django import forms
from alumnica_model.models import ODA
from alumnica_model.models.content import Subject, Tag, Moment, MicroODA, Image, Evaluation
from alumnica_model.models.questions import *


class ODAsSectionForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'is-hidden'}))

    class Meta:
        model = Subject
        fields = ['name']


class ODAsPositionForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'is-hidden'}))


class ODAsPreviewForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'is-hidden'}))


class ODACreateForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput())
    tags = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'u-margin-bottom-small selectized',
                                                                         'id': 'oda-tags'}))
    active_icon = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'is-hidden image',
                                                                                 'type': 'file'}))
    completed_icon = forms.ImageField(required=False,
                                      widget=forms.FileInput(attrs={'class': 'is-hidden image', 'type': 'file'}))
    evaluation_file = forms.FileField(required=False, widget=forms.FileInput(attrs={'id': 'evaluation_file',
                                                                                    'accept': '.xlsx'}))

    class Meta:
        model = ODA
        fields = ['name', 'tags']

    def save_form(self, user, moments, subject, bloque, evaluation, is_draft=False):

        oda = super(ODACreateForm, self).save(commit=False)
        cleaned_data = super(ODACreateForm, self).clean()
        tags = cleaned_data.get('tags')
        completed_icon = cleaned_data.get('completed_icon')
        active_icon = cleaned_data.get('active_icon')
        evaluation_file = cleaned_data.get('evaluation_file')

        oda.created_by = user
        oda.temporal = is_draft
        oda.save()

        if subject is not None:
            subject_model = Subject.objects.get(name=subject)
            subject_model.odas.add(oda)
            subject_model.save()

        if bloque is not None:
            oda.section = bloque

        if tags is not None and tags is not '':
            tags = tags.split(',')
            for tag_name in tags:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                oda.tags.add(tag)
        counter = 1
        for moment_object in moments:

            microoda, created = MicroODA.objects.get_or_create(name='odas',
                                                               created_by=user,
                                                               type=moment_object[0],
                                                               default_position=counter, oda=oda)
            counter += 1

            if moment_object[1] is not None and moment_object[1] is not '':

                moments_names = moment_object[1].split(',')

                for moment_name in moments_names:
                    moment = Moment.objects.get(name=moment_name)
                    microoda.activities.add(moment)
            microoda.save()

        if active_icon is not None:
            if isinstance(active_icon, Image):
                    active_icon_object = Image.objects.get(folder="odas", file=active_icon.file)
                    active_icon_object.name = '{}-oda_active_icon'.format(oda.name)
            else:
                active_icon_object = Image.objects.create(name='{}-oda_active_icon'.format(oda.name), folder="ambits",
                                                          file=active_icon)
                active_icon_object.file_name = os.path.basename(active_icon_object.file.name)
            active_icon_object.save()
            oda.active_icon = active_icon_object

        if completed_icon is not None:
            if isinstance(completed_icon, Image):
                completed_icon_object = Image.objects.get(folder="odas", file=completed_icon.file)
                completed_icon_object.name = '{}-oda_completed_icon'.format(oda.name)
            else:
                completed_icon_object = Image.objects.create(name='{}-oda_completed_icon'.format(oda.name),
                                                             folder="ambits", file=completed_icon)
                completed_icon_object.file_name = os.path.basename(completed_icon_object.file.name)
            completed_icon_object.save()
            oda.completed_icon = completed_icon_object
        if evaluation is not None and evaluation is not '':
            oda.evaluation = Evaluation.objects.get(name=evaluation)

        if evaluation_file is not None:
            evaluation_object = self.set_evaluation(oda, evaluation_file)
            oda.evaluation = evaluation_object
        oda.save()
        return oda

    def set_evaluation(self, oda, file):
        evaluation = Evaluation.objects.create(name='{}_evaluation'.format(oda.name), file=file, file_name=file.name)
        file.seek(0)
        file_read = file.read()
        relationship_questions = get_json_from_excel(file_read, 0)
        for question_data in relationship_questions:
            question = RelationShipQuestion.objects.create(questions=question_data['Preguntas'],
                                                           answers=question_data['Respuestas'], evaluation=evaluation)

        multiple_option_questions = get_json_from_excel(file_read, 1)
        for question_data in multiple_option_questions:
            question = MultipleOptionQuestion.objects.create(question=question_data['Pregunta'],
                                                             correct_answer=question_data['RespuestaOK'],
                                                             incorrect_answers=question_data['RespuestasNOK'],
                                                             evaluation=evaluation)

        multiple_answer_questions = get_json_from_excel(file_read, 2)
        for question_data in multiple_answer_questions:
            question = MultipleAnswerQuestion.objects.create(question=question_data['Pregunta'],
                                                             correct_answers=question_data['RespuestasOK'],
                                                             incorrect_answers=question_data['RespuestasNOK'],
                                                             evaluation=evaluation)

        numeric_questions = get_json_from_excel(file_read, 3)
        for question_data in numeric_questions:
            question = NumericQuestion.objects.create(question=question_data['Pregunta'],
                                                      min_limit=question_data['LimiteMenor'],
                                                      max_limit=question_data['LimiteMayor'],
                                                      evaluation=evaluation)

        pull_down_list_questions = get_json_from_excel(file_read, 4)
        for question_data in pull_down_list_questions:
            question = PullDownListQuestion.objects.create(questions=question_data['Preguntas'],
                                                           answers=question_data['Respuestas'], evaluation=evaluation)

        return evaluation


class ODAUpdateForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'oda-name'}))
    tags = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'u-margin-bottom-small selectized',
                                                                         'id':
                                                                             'oda-tags'}))

    active_icon = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'is-hidden', 'type': 'file'}))
    completed_icon = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'is-hidden',
                                                                                    'type': 'file'}))
    evaluation_file = forms.FileField(required=False, widget=forms.FileInput(attrs={'id': 'evaluation_file',
                                                                                    'accept': '.xlsx'}))

    class Meta:
        model = ODA
        fields = ['name', 'tags']

    def save_form(self, user, moments, subject, bloque, evaluation,  is_draft=False):
        cleaned_data = super(ODAUpdateForm, self).clean()
        tags = cleaned_data.get('tags')
        completed_icon = cleaned_data.get('completed_icon')
        active_icon = cleaned_data.get('active_icon')
        oda = super(ODAUpdateForm, self).save(commit=False)

        if subject is not None:
            subject_model = Subject.objects.get(name=subject)
            subject_model.odas.add(oda)
            subject_model.save()

        if bloque is not None:
            oda.section = bloque

        if tags is not None and tags is not '':
            tags = tags.split(',')
            for tag_name in tags:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                oda.tags.add(tag)

        for moment_object in moments:

            if moment_object[1] is not '' or None:

                moments_names = moment_object[1].split(',')

                try:
                    microoda = MicroODA.objects.get(name='odas', type=moment_object[0], oda=oda)
                except MicroODA.DoesNotExist:
                    microoda = MicroODA.objects.create(name='odas', type=moment_object[0],
                                                       created_by=user, oda=oda)

                for moment_name in moments_names:
                    moment = Moment.objects.get(name=moment_name)
                    microoda.activities.add(moment)
                    microoda.save()

                for moment in microoda.activities.all():
                    if moment.name not in moments_names:
                        microoda.activities.remove(moment)
                    microoda.save()

        if active_icon is not None:
            if isinstance(active_icon, Image):
                    active_icon_object = Image.objects.get(folder="odas", file=active_icon.file)
                    active_icon_object.name = '{}-oda_active_icon'.format(oda.name)
            else:
                active_icon_object = Image.objects.create(name='{}-oda_active_icon'.format(oda.name), folder="ambits",
                                                          file=active_icon)
                active_icon_object.file_name = os.path.basename(active_icon_object.file.name)
            active_icon_object.save()
            oda.active_icon = active_icon_object

        if completed_icon is not None:
            if isinstance(completed_icon, Image):
                completed_icon_object = Image.objects.get(folder="odas", file=completed_icon.file)
                completed_icon_object.name = '{}-oda_completed_icon'.format(oda.name)
            else:
                completed_icon_object = Image.objects.create(name='{}-oda_completed_icon'.format(oda.name),
                                                             folder="ambits", file=completed_icon)
                completed_icon_object.file_name = os.path.basename(completed_icon_object.file.name)
            completed_icon_object.save()
            oda.completed_icon = completed_icon_object

        if evaluation is not None and evaluation is not '':
            oda.evaluation = Evaluation.objects.get(name=evaluation)
        oda.temporal = is_draft
        oda.save()

        return oda


def get_json_from_excel(file, sheet_name):
    workbook = xlrd.open_workbook(file_contents=file)
    worksheet = workbook.sheet_by_index(sheet_name)

    data = []
    keys = [v.value for v in worksheet.row(0)]
    for row_number in range(worksheet.nrows):
        if row_number == 0:
            continue
        row_data = {}
        for col_number, cell in enumerate(worksheet.row(row_number)):
            row_data[keys[col_number]] = cell.value
        data.append(row_data)

    json_output = json.loads(json.dumps(data))
    return json_output
