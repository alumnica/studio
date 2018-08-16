import json
import os

import xlrd
from django import forms

from alumnica_model.models import ODA
from alumnica_model.models.content import Subject, Tag, MicroODA, Image
from alumnica_model.models.questions import *


class ODAsPositionForm(forms.Form):
    """
    Contains ODA to be positioned name
    """
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'is-hidden'}))


class ODACreateForm(forms.ModelForm):
    """
    Create new ODA object form
    """
    name = forms.CharField(widget=forms.TextInput())
    description = forms.CharField(required=False, widget=forms.TextInput(attrs={'id': 'oda-desc'}))
    tags = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'u-margin-bottom-small selectized',
                                                                         'id': 'oda-tags'}))

    active_icon = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'is-hidden image',
                                                                                 'type': 'file'}))
    completed_icon = forms.ImageField(required=False,
                                      widget=forms.FileInput(attrs={'class': 'is-hidden image', 'type': 'file'}))
    evaluation_file = forms.FileField(required=False,
                                      widget=forms.FileInput(attrs={'class': 'is-hidden', 'id': 'evaluation_file',
                                                                    'accept': '.xlsx'}))
    apli_tags = forms.CharField(required=False,
                                widget=forms.TextInput(attrs={'class': 'u-margin-bottom-small selectized',
                                                              'id': 'apli-tags'}))
    forma_tags = forms.CharField(required=False,
                                 widget=forms.TextInput(attrs={'class': 'u-margin-bottom-small selectized',
                                                               'id': 'forma-tags'}))
    activ_tags = forms.CharField(required=False,
                                 widget=forms.TextInput(attrs={'class': 'u-margin-bottom-small selectized',
                                                               'id': 'activ-tags'}))
    ejemp_tags = forms.CharField(required=False,
                                 widget=forms.TextInput(attrs={'class': 'u-margin-bottom-small selectized',
                                                               'id': 'ejemp-tags'}))
    sens_tags = forms.CharField(required=False,
                                widget=forms.TextInput(attrs={'class': 'u-margin-bottom-small selectized',
                                                              'id': 'sens-tags'}))

    class Meta:
        model = ODA
        fields = ['name', 'description', 'tags']

    def save_form(self, user, moments, subject, bloque, is_draft=False):
        oda = super(ODACreateForm, self).save(commit=False)
        cleaned_data = super(ODACreateForm, self).clean()

        tags = cleaned_data.get('tags')
        apli_tags = cleaned_data.get('apli_tags')
        forma_tags = cleaned_data.get('forma_tags')
        activ_tags = cleaned_data.get('activ_tags')
        ejemp_tags = cleaned_data.get('ejemp_tags')
        sens_tags = cleaned_data.get('sens_tags')
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
            MicroODA.objects.get_or_create(name='{}'.format(moment_object[0]),
                                           created_by=user,
                                           type=MicroODAType.objects.get(name=moment_object[0]),
                                           default_position=counter, oda=oda)
            counter += 1

        if apli_tags is not None:
            set_microodas_tags(oda.microodas.get(type=MicroODAType.objects.get(name='application')), apli_tags)
        if forma_tags is not None:
            set_microodas_tags(oda.microodas.get(type=MicroODAType.objects.get(name='formalization')), forma_tags)
        if activ_tags is not None:
            set_microodas_tags(oda.microodas.get(type=MicroODAType.objects.get(name='activation')), activ_tags)
        if ejemp_tags is not None:
            set_microodas_tags(oda.microodas.get(type=MicroODAType.objects.get(name='exemplification')), ejemp_tags)
        if sens_tags is not None:
            set_microodas_tags(oda.microodas.get(type=MicroODAType.objects.get(name='sensitization')), sens_tags)

        if active_icon is not None:
            if isinstance(active_icon, Image):
                active_icon_object = Image.objects.get(folder="ODAs", file=active_icon.file)
                active_icon_object.name = '{}-oda_active_icon'.format(oda.name)
            else:
                active_icon_object = Image.objects.create(name='{}-oda_active_icon'.format(oda.name), folder="ODAs",
                                                          file=active_icon)
                active_icon_object.file_name = os.path.basename(active_icon_object.file.name)
            active_icon_object.save()
            oda.active_icon = active_icon_object

        if completed_icon is not None:
            if isinstance(completed_icon, Image):
                completed_icon_object = Image.objects.get(folder="ODAs", file=completed_icon.file)
                completed_icon_object.name = '{}-oda_completed_icon'.format(oda.name)
            else:
                completed_icon_object = Image.objects.create(name='{}-oda_completed_icon'.format(oda.name),
                                                             folder="ODAs", file=completed_icon)
                completed_icon_object.file_name = os.path.basename(completed_icon_object.file.name)
            completed_icon_object.save()
            oda.completed_icon = completed_icon_object

        if evaluation_file is not None:
            evaluation_instance = Evaluation.objects.create(
                name='{}_evaluation'.format(oda.name),
                file=evaluation_file,
                file_name=evaluation_file.name)
            set_evaluation(evaluation_instance)
            oda.evaluation = evaluation_instance
        oda.save()
        return oda


class ODAUpdateForm(forms.ModelForm):
    """
    Update existing ODA object form
    """
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'oda-name'}))
    description = forms.CharField(required=False, widget=forms.TextInput(attrs={'id': 'oda-desc'}))
    tags = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'u-margin-bottom-small selectized',
                                                                         'id':
                                                                             'oda-tags'}))

    active_icon = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'is-hidden', 'type': 'file'}))
    completed_icon = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'is-hidden',
                                                                                    'type': 'file'}))
    evaluation_file = forms.FileField(required=False,
                                      widget=forms.FileInput(attrs={'class': 'is-hidden', 'id': 'evaluation_file',
                                                                    'accept': '.xlsx'}))
    apli_tags = forms.CharField(required=False,
                                widget=forms.TextInput(attrs={'class': 'u-margin-bottom-small selectized',
                                                              'id': 'apli-tags'}))
    forma_tags = forms.CharField(required=False,
                                 widget=forms.TextInput(attrs={'class': 'u-margin-bottom-small selectized',
                                                               'id': 'forma-tags'}))
    activ_tags = forms.CharField(required=False,
                                 widget=forms.TextInput(attrs={'class': 'u-margin-bottom-small selectized',
                                                               'id': 'activ-tags'}))
    ejemp_tags = forms.CharField(required=False,
                                 widget=forms.TextInput(attrs={'class': 'u-margin-bottom-small selectized',
                                                               'id': 'ejemp-tags'}))
    sens_tags = forms.CharField(required=False,
                                widget=forms.TextInput(attrs={'class': 'u-margin-bottom-small selectized',
                                                              'id': 'sens-tags'}))

    class Meta:
        model = ODA
        fields = ['name', 'description', 'tags']

    def save_form(self, user, moments, subject, bloque, evaluation, is_draft=False):
        cleaned_data = super(ODAUpdateForm, self).clean()

        tags = cleaned_data.get('tags')
        apli_tags = cleaned_data.get('apli_tags')
        forma_tags = cleaned_data.get('forma_tags')
        activ_tags = cleaned_data.get('activ_tags')
        ejemp_tags = cleaned_data.get('ejemp_tags')
        sens_tags = cleaned_data.get('sens_tags')
        completed_icon = cleaned_data.get('completed_icon')
        active_icon = cleaned_data.get('active_icon')
        evaluation_file = cleaned_data.get('evaluation_file')
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
                if tag not in oda.tags.all():
                    oda.tags.add(tag)
            for tag in oda.tags.all():
                if tag.name not in tags:
                    oda.tags.remove(tag)

        for moment_object in moments:

            try:
                microoda = MicroODA.objects.get(type=MicroODAType.objects.get(name=moment_object[0]), oda=oda)
                microoda.name = '{}_oda_{}'.format(oda.name, moment_object[0])
                microoda.save()
            except MicroODA.DoesNotExist:
                microoda = MicroODA.objects.create(name='{}'.format(moment_object[0]),
                                                   type=MicroODAType.objects.get(moment_object[0]),
                                                   created_by=user, oda=oda)

            moments_names = moment_object[1].split(',')

            for moment in microoda.activities.all():
                if moment.name not in moments_names:
                    microoda.activities.remove(moment)
                microoda.save()

            set_microodas_tags(oda.microodas.get(type=MicroODAType.objects.get(name='application')), apli_tags)
            set_microodas_tags(oda.microodas.get(type=MicroODAType.objects.get(name='formalization')), forma_tags)
            set_microodas_tags(oda.microodas.get(type=MicroODAType.objects.get(name='activation')), activ_tags)
            set_microodas_tags(oda.microodas.get(type=MicroODAType.objects.get(name='exemplification')), ejemp_tags)
            set_microodas_tags(oda.microodas.get(type=MicroODAType.objects.get(name='sensitization')), sens_tags)

        if active_icon is not None:
            if isinstance(active_icon, Image):
                active_icon_object = Image.objects.get(folder="ODAs", file=active_icon.file)
                active_icon_object.name = '{}-oda_active_icon'.format(oda.name)
            else:
                active_icon_object = Image.objects.create(name='{}-oda_active_icon'.format(oda.name), folder="ODAs",
                                                          file=active_icon)
                active_icon_object.file_name = os.path.basename(active_icon_object.file.name)
            active_icon_object.save()
            oda.active_icon = active_icon_object

        if completed_icon is not None:
            if isinstance(completed_icon, Image):
                completed_icon_object = Image.objects.get(folder="ODAs", file=completed_icon.file)
                completed_icon_object.name = '{}-oda_completed_icon'.format(oda.name)
            else:
                completed_icon_object = Image.objects.create(name='{}-oda_completed_icon'.format(oda.name),
                                                             folder="ODAs", file=completed_icon)
                completed_icon_object.file_name = os.path.basename(completed_icon_object.file.name)
            completed_icon_object.save()
            oda.completed_icon = completed_icon_object

        if evaluation_file is not None:
            if oda.evaluation is None:
                evaluation_instance = Evaluation.objects.create(
                    name='{}_evaluation'.format(oda.name),
                    file=evaluation_file,
                    file_name=evaluation_file.name)
            else:
                evaluation_instance = oda.evaluation

            set_evaluation(evaluation_instance)
            oda.evaluation = evaluation_instance
        oda.temporal = is_draft
        if is_draft:
            oda.zone = 0
        oda.save()

        return oda


def set_microodas_tags(microoda, tags):
    """
    Adds tags to each MicroODA
    :param microoda: MicroODA object
    :param tags: Tags string separated by comma
    """
    if tags is not None and tags is not '':
        tags = tags.split(',')
        for tag_name in tags:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            if tag not in microoda.tags.all():
                microoda.tags.add(tag)
    for tag in microoda.tags.all():
        if tag.name not in tags:
            microoda.tags.remove(tag)
    microoda.save()


def get_json_from_excel(file, sheet_name):
    """
    Gets data stored in excel file as json
    :param file: File name
    :param sheet_name: Excel sheet name
    """
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


def set_evaluation(evaluation):
    """
    Creates Question objects from file and assigns them to an Evaluation object
    :param evaluation: Evaluation object
    """
    file_read = evaluation.file.read()

    relationship_questions = get_json_from_excel(file_read, 1)
    relationship_questions_instances = []

    for question_data in relationship_questions:
        question, created = RelationShipQuestion.objects.get_or_create(
            microoda=MicroODAType.objects.get(pk=question_data['mODA']),
            sentence=question_data['Enunciado'],
            options=question_data['Opciones'],
            answers=question_data['Respuestas'],
            evaluation=evaluation)
        question.success_description = question_data['DescripcionOK']
        question.fail_description = question_data['DescripcionNOK']
        question.save()
        relationship_questions_instances.append(question)

    for question_in_evaluation in evaluation.relationship_questions.all():
        if question_in_evaluation not in relationship_questions_instances:
            question_in_evaluation.delete()

    multiple_option_questions = get_json_from_excel(file_read, 2)
    multiple_option_questions_instances = []

    for question_data in multiple_option_questions:
        question, created = MultipleOptionQuestion.objects.get_or_create(
            microoda=MicroODAType.objects.get(pk=question_data['mODA']),
            sentence=question_data['Enunciado'],
            correct_answer=question_data['RespuestaOK'],
            incorrect_answers=question_data['RespuestasNOK'],
            evaluation=evaluation)
        question.success_description = question_data['DescripcionOK']
        question.fail_description = question_data['DescripcionNOK']
        question.save()
        multiple_option_questions_instances.append(question)

    for question_in_evaluation in evaluation.multiple_option_questions.all():
        if question_in_evaluation not in multiple_option_questions_instances:
            question_in_evaluation.delete()

    multiple_answer_questions = get_json_from_excel(file_read, 3)
    multiple_answer_questions_instances = []

    for question_data in multiple_answer_questions:
        question, created = MultipleAnswerQuestion.objects.get_or_create(
            microoda=MicroODAType.objects.get(pk=question_data['mODA']),
            sentence=question_data['Enunciado'],
            correct_answers=question_data['RespuestasOK'],
            incorrect_answers=question_data['RespuestasNOK'],
            evaluation=evaluation)
        question.success_description = question_data['DescripcionOK']
        question.fail_description = question_data['DescripcionNOK']
        question.save()
        multiple_answer_questions_instances.append(question)

    for question_in_evaluation in evaluation.multiple_answer_questions.all():
        if question_in_evaluation not in multiple_answer_questions_instances:
            question_in_evaluation.delete()

    numeric_questions = get_json_from_excel(file_read, 4)
    numeric_questions_instances = []

    for question_data in numeric_questions:
        question, created = NumericQuestion.objects.get_or_create(
            microoda=MicroODAType.objects.get(pk=question_data['mODA']),
            sentence=question_data['Enunciado'],
            min_limit=question_data['LimiteMenor'],
            max_limit=question_data['LimiteMayor'],
            evaluation=evaluation)
        question.success_description = question_data['DescripcionOK']
        question.fail_description = question_data['DescripcionNOK']
        question.save()
        numeric_questions_instances.append(question)

    for question_in_evaluation in evaluation.numeric_questions.all():
        if question_in_evaluation not in numeric_questions_instances:
            question_in_evaluation.delete()

    pull_down_list_questions = get_json_from_excel(file_read, 5)
    pull_down_list_questions_instances = []

    for question_data in pull_down_list_questions:
        question, created = PullDownListQuestion.objects.get_or_create(
            microoda=MicroODAType.objects.get(pk=question_data['mODA']),
            sentence=question_data['Enunciado'],
            options=question_data['Opciones'],
            answers=question_data['Respuestas'],
            evaluation=evaluation)
        question.success_description = question_data['DescripcionOK']
        question.fail_description = question_data['DescripcionNOK']
        question.save()
        pull_down_list_questions_instances.append(question)

    for question_in_evaluation in evaluation.pull_down_list_questions.all():
        if question_in_evaluation not in pull_down_list_questions_instances:
            question_in_evaluation.delete()
