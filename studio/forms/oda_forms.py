import json
import os
import xlrd
from django import forms
from django.core.exceptions import ValidationError
from alumnica_model.models import ODA
from alumnica_model.models.content import Subject, Tag, MicroODA, Image, DICT_MOMENTS, Reference
from alumnica_model.models.questions import *


class ODAsPositionForm(forms.Form):
    """
    Contains ODA to be positioned name
    """
    name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'is-hidden'}))


class ODACreateForm(forms.ModelForm):
    """
    Create new ODA object form
    """
    name = forms.CharField(widget=forms.TextInput())
    description = forms.CharField(required=False, widget=forms.TextInput(attrs={'id': 'oda-desc'}))
    learning_objective = forms.CharField(required=False, widget=forms.TextInput(attrs={'id': 'oda-learning_objective'}))
    tags = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'u-margin-bottom-small selectized',
                                                                         'id': 'oda-tags'}))
    references = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'u-margin-bottom-small selectized',
                                                                         'id': 'oda-references'}))

    active_icon = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'is-hidden image',
                                                                                 'type': 'file'}))
    completed_icon = forms.ImageField(required=False,
                                      widget=forms.FileInput(attrs={'class': 'is-hidden image', 'type': 'file'}))
    
    img_oda = forms.ImageField(required=False,
                                      widget=forms.FileInput(attrs={'class': 'is-hidden image', 'type': 'file'}))
    img_portada = forms.ImageField(required=False,
                                      widget=forms.FileInput(attrs={'class': 'is-hidden image', 'type': 'file'}))

    evaluation_file = forms.FileField(required=False,
                                      widget=forms.FileInput(attrs={'class': 'is-hidden', 'id': 'evaluation_file',
                                                                    'accept': '.xlsx'}))
    apli_tags = forms.CharField(required=False,
                                widget=forms.TextInput(attrs={'class': 'u-margin-bottom-small selectized',
                                                              'id': 'apli-tags'}))
    apli_description = forms.CharField(required=False, widget=forms.TextInput(attrs={'id': 'apli-desc'}))
    apli_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'id': 'apli-name'}))

    
    forma_tags = forms.CharField(required=False,
                                 widget=forms.TextInput(attrs={'class': 'u-margin-bottom-small selectized',
                                                               'id': 'forma-tags'}))
    forma_description = forms.CharField(required=False, widget=forms.TextInput(attrs={'id': 'forma-desc'}))
    forma_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'id': 'forma-name'}))

    
    activ_tags = forms.CharField(required=False,
                                 widget=forms.TextInput(attrs={'class': 'u-margin-bottom-small selectized',
                                                               'id': 'activ-tags'}))
    activ_description = forms.CharField(required=False, widget=forms.TextInput(attrs={'id': 'activ-desc'}))
    activ_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'id': 'activ-name'}))

    
    ejemp_tags = forms.CharField(required=False,
                                 widget=forms.TextInput(attrs={'class': 'u-margin-bottom-small selectized',
                                                               'id': 'ejemp-tags'}))
    ejemp_description = forms.CharField(required=False, widget=forms.TextInput(attrs={'id': 'ejemp-desc'}))
    ejemp_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'id': 'ejemp-name'}))

    
    sens_tags = forms.CharField(required=False,
                                widget=forms.TextInput(attrs={'class': 'u-margin-bottom-small selectized',
                                                              'id': 'sens-tags'}))
    sens_description = forms.CharField(required=False, widget=forms.TextInput(attrs={'id': 'sens-desc'}))
    sens_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'id': 'sens-name'}))

    class Meta:
        model = ODA
        fields = ['name', 'description', 'learning_objective', 'tags', 'references']

    def clean(self):
        cleaned_data = super(ODACreateForm, self).clean()
        evaluation_file = cleaned_data.get('evaluation_file')
        if evaluation_file is not None:
            file_read = evaluation_file.read()
            workbook = xlrd.open_workbook(file_contents=file_read)

            if len(workbook.sheet_names()) < 6:
                error = ValidationError("Archivo inválido", code='file_error')
                self.add_error('evaluation_file', error)
            else:
                relationship_questions = get_json_from_excel(file_read, 1)

                for question_data in relationship_questions:
                    columns_name = ['mODA', 'Enunciado', 'Opciones', 'Respuestas', 'DescripcionOK', 'DescripcionNOK']

                    for element in columns_name:
                        if element not in question_data:
                            error = ValidationError("Archivo inválido", code='file_error')
                            self.add_error('evaluation_file', error)
                            return cleaned_data

                multiple_option_questions = get_json_from_excel(file_read, 2)
                for question_data in multiple_option_questions:
                    columns_name = ['mODA', 'Enunciado', 'RespuestaOK', 'RespuestasNOK', 'DescripcionOK',
                                    'DescripcionNOK']

                    for element in columns_name:
                        if element not in question_data:
                            error = ValidationError("Archivo inválido", code='file_error')
                            self.add_error('evaluation_file', error)
                            return cleaned_data

                multiple_answer_questions = get_json_from_excel(file_read, 3)
                for question_data in multiple_answer_questions:
                    columns_name = ['mODA', 'Enunciado', 'RespuestasOK', 'RespuestasNOK', 'DescripcionOK',
                                    'DescripcionNOK']

                    for element in columns_name:
                        if element not in question_data:
                            error = ValidationError("Archivo inválido", code='file_error')
                            self.add_error('evaluation_file', error)
                            return cleaned_data

                numeric_questions = get_json_from_excel(file_read, 4)
                for question_data in numeric_questions:
                    columns_name = ['mODA', 'Enunciado', 'LimiteMenor', 'LimiteMayor', 'DescripcionOK',
                                    'DescripcionNOK']

                    for element in columns_name:
                        if element not in question_data:
                            error = ValidationError("Archivo inválido", code='file_error')
                            self.add_error('evaluation_file', error)
                            return cleaned_data

                pull_down_list_questions = get_json_from_excel(file_read, 5)
                for question_data in pull_down_list_questions:
                    columns_name = ['mODA', 'Enunciado', 'Opciones', 'Respuestas', 'DescripcionOK', 'DescripcionNOK']

                    for element in columns_name:
                        if element not in question_data:
                            error = ValidationError("Archivo inválido", code='file_error')
                            self.add_error('evaluation_file', error)
                            return cleaned_data
        return cleaned_data

    def save_form(self, user, moments, subject, bloque, is_draft=False):
        oda = super(ODACreateForm, self).save(commit=False)
        cleaned_data = super(ODACreateForm, self).clean()
        tags = cleaned_data.get('tags')
        references = cleaned_data.get('references')
        apli_tags = cleaned_data.get('apli_tags')
        apli_description = cleaned_data.get('apli_description')
        apli_name = cleaned_data.get('apli_name')
        forma_tags = cleaned_data.get('forma_tags')
        forma_description = cleaned_data.get('forma_description')
        forma_name = cleaned_data.get('forma_name')
        activ_tags = cleaned_data.get('activ_tags')
        activ_description = cleaned_data.get('activ_description')
        activ_name = cleaned_data.get('activ_name')
        ejemp_tags = cleaned_data.get('ejemp_tags')
        ejemp_description = cleaned_data.get('ejemp_description')
        ejemp_name = cleaned_data.get('ejemp_name')
        sens_tags = cleaned_data.get('sens_tags')
        sens_description = cleaned_data.get('sens_description')
        sens_name = cleaned_data.get('sens_name')
        completed_icon = cleaned_data.get('completed_icon')
        active_icon = cleaned_data.get('active_icon')
        img_oda = cleaned_data.get('img_oda')
        img_portada = cleaned_data.get('img_portada')
        evaluation_file = cleaned_data.get('evaluation_file')
        learning_objective=cleaned_data.get('learning_objective')
        oda.learning_objective =learning_objective

        oda.created_by = user
        oda.temporal = is_draft
        oda.save()



        if subject is not None:
            subject_model = Subject.objects.get(name=subject)
            subject_model.odas.add(oda)
            subject_model.save()

        if bloque is not None:
            oda.section = bloque

        if tags is not None and tags != '':
            tags = tags.split(',')
            for tag_name in tags:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                oda.tags.add(tag)

        if references is not None and references != '':
            references = references.split('|')
            for reference_name in references:
                reference, created = Reference.objects.get_or_create(name=reference_name)
                oda.references.add(tag)

        counter = 1
        for moment_object in moments:
            MicroODA.objects.get_or_create(name='{}'.format(moment_object[0]),
                                           created_by=user,
                                           type=MicroODAType.objects.get(name=moment_object[0]),
                                           default_position=counter, oda=oda)
            counter += 1

        set_microodas_tags(oda.microodas.get(type=MicroODAType.objects.get(name='application')), apli_tags, apli_description, apli_name)
        set_microodas_tags(oda.microodas.get(type=MicroODAType.objects.get(name='formalization')), forma_tags, forma_description, forma_name)
        set_microodas_tags(oda.microodas.get(type=MicroODAType.objects.get(name='activation')), activ_tags, activ_description, activ_name)
        set_microodas_tags(oda.microodas.get(type=MicroODAType.objects.get(name='exemplification')), ejemp_tags, ejemp_description, ejemp_name)
        set_microodas_tags(oda.microodas.get(type=MicroODAType.objects.get(name='sensitization')), sens_tags, sens_description, sens_name)


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

        if img_oda is not None:
            if isinstance(img_oda, Image):
                img_oda_object = Image.objects.get(folder="ODAs", file=img_oda.file)
                img_oda_object.name = '{}-img_oda'.format(oda.name)
            else:
                img_oda_object = Image.objects.create(name='{}-img_oda'.format(oda.name), folder="ODAs",
                                                          file=img_oda)
                img_oda_object.file_name = os.path.basename(img_oda_object.file.name)
            img_oda_object.save()
            oda.img_oda = img_oda_object

        if img_portada is not None:
            if isinstance(img_portada, Image):
                img_portada_object = Image.objects.get(folder="ODAs", file=img_portada.file)
                img_portada_object.name = '{}-img_portada'.format(oda.name)
            else:
                img_portada_object = Image.objects.create(name='{}-img_portada'.format(oda.name), folder="ODAs",
                                                          file=img_portada)
                img_portada_object.file_name = os.path.basename(img_portada_object.file.name)
            img_portada_object.save()
            oda.img_portada = img_portada_object

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
                file_name="oda_" + str (oda.id) + "_" + evaluation_file.name)
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
    learning_objective = forms.CharField(required=False, widget=forms.TextInput(attrs={'id': 'oda-learning_objective'}))
    tags = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'u-margin-bottom-small selectized',
                                                                         'id':
                                                                             'oda-tags'}))

    references = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'u-margin-bottom-small selectized',
                                                                         'id':
                                                                             'oda-references'}))


    active_icon = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'is-hidden', 'type': 'file'}))
    
    img_oda = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'is-hidden image', 'type': 'file'}))
    img_portada = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'is-hidden image', 'type': 'file'}))

    completed_icon = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'is-hidden',
                                                                                    'type': 'file'}))
    evaluation_file = forms.FileField(required=False,
                                      widget=forms.FileInput(attrs={'class': 'is-hidden', 'id': 'evaluation_file',
                                                                    'accept': '.xlsx'}))
    apli_tags = forms.CharField(required=False,
                                widget=forms.TextInput(attrs={'class': 'u-margin-bottom-small selectized',
                                                              'id': 'apli-tags'}))
    apli_description = forms.CharField(required=False, widget=forms.TextInput(attrs={'id': 'apli-desc'}))
    apli_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'id': 'apli-name'}))

    
    forma_tags = forms.CharField(required=False,
                                 widget=forms.TextInput(attrs={'class': 'u-margin-bottom-small selectized',
                                                               'id': 'forma-tags'}))
    forma_description = forms.CharField(required=False, widget=forms.TextInput(attrs={'id': 'forma-desc'}))
    forma_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'id': 'forma-name'}))

    
    activ_tags = forms.CharField(required=False,
                                 widget=forms.TextInput(attrs={'class': 'u-margin-bottom-small selectized',
                                                               'id': 'activ-tags'}))
    activ_description = forms.CharField(required=False, widget=forms.TextInput(attrs={'id': 'activ-desc'}))
    activ_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'id': 'activ-name'}))

    
    ejemp_tags = forms.CharField(required=False,
                                 widget=forms.TextInput(attrs={'class': 'u-margin-bottom-small selectized',
                                                               'id': 'ejemp-tags'}))
    ejemp_description = forms.CharField(required=False, widget=forms.TextInput(attrs={'id': 'ejemp-desc'}))
    ejemp_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'id': 'ejemp-name'}))

    
    sens_tags = forms.CharField(required=False,
                                widget=forms.TextInput(attrs={'class': 'u-margin-bottom-small selectized',
                                                              'id': 'sens-tags'}))
    sens_description = forms.CharField(required=False, widget=forms.TextInput(attrs={'id': 'sens-desc'}))
    sens_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'id': 'sens-name'}))

    class Meta:
        model = ODA
        fields = ['name', 'description', 'learning_objective', 'tags', 'references']

    def clean(self):
        cleaned_data = super(ODAUpdateForm, self).clean()
        evaluation_file = cleaned_data.get('evaluation_file')
        if evaluation_file is not None:
            file_read = evaluation_file.read()
            workbook = xlrd.open_workbook(file_contents=file_read)

            if len(workbook.sheet_names()) < 6:
                error = ValidationError("Archivo inválido", code='file_error')
                self.add_error('evaluation_file', error)
            else:
                relationship_questions = get_json_from_excel(file_read, 1)

                for question_data in relationship_questions:
                    columns_name = ['mODA', 'Enunciado', 'Opciones', 'Respuestas', 'DescripcionOK', 'DescripcionNOK']

                    for element in columns_name:
                        if element not in question_data:
                            error = ValidationError("Archivo inválido", code='file_error')
                            self.add_error('evaluation_file', error)
                            return cleaned_data

                multiple_option_questions = get_json_from_excel(file_read, 2)
                for question_data in multiple_option_questions:
                    columns_name = ['mODA', 'Enunciado', 'RespuestaOK', 'RespuestasNOK', 'DescripcionOK',
                                    'DescripcionNOK']

                    for element in columns_name:
                        if element not in question_data:
                            error = ValidationError("Archivo inválido", code='file_error')
                            self.add_error('evaluation_file', error)
                            return cleaned_data

                multiple_answer_questions = get_json_from_excel(file_read, 3)
                for question_data in multiple_answer_questions:
                    columns_name = ['mODA', 'Enunciado', 'RespuestasOK', 'RespuestasNOK', 'DescripcionOK',
                                    'DescripcionNOK']

                    for element in columns_name:
                        if element not in question_data:
                            error = ValidationError("Archivo inválido", code='file_error')
                            self.add_error('evaluation_file', error)
                            return cleaned_data

                numeric_questions = get_json_from_excel(file_read, 4)
                for question_data in numeric_questions:
                    columns_name = ['mODA', 'Enunciado', 'LimiteMenor', 'LimiteMayor', 'DescripcionOK',
                                    'DescripcionNOK']

                    for element in columns_name:
                        if element not in question_data:
                            error = ValidationError("Archivo inválido", code='file_error')
                            self.add_error('evaluation_file', error)
                            return cleaned_data

                pull_down_list_questions = get_json_from_excel(file_read, 5)
                for question_data in pull_down_list_questions:
                    columns_name = ['mODA', 'Enunciado', 'Opciones', 'Respuestas', 'DescripcionOK', 'DescripcionNOK']

                    for element in columns_name:
                        if element not in question_data:
                            error = ValidationError("Archivo inválido", code='file_error')
                            self.add_error('evaluation_file', error)
                            return cleaned_data
        return cleaned_data

    def save_form(self, user, moments, subject, bloque, evaluation, is_draft=False):
        cleaned_data = super(ODAUpdateForm, self).clean()
        tags = cleaned_data.get('tags')
        references = cleaned_data.get('references')
        apli_tags = cleaned_data.get('apli_tags')
        apli_description = cleaned_data.get('apli_description')
        apli_name = cleaned_data.get('apli_name')
        forma_tags = cleaned_data.get('forma_tags')
        forma_description = cleaned_data.get('forma_description')
        forma_name = cleaned_data.get('forma_name')
        activ_tags = cleaned_data.get('activ_tags')
        activ_description = cleaned_data.get('activ_description')
        activ_name = cleaned_data.get('activ_name')
        ejemp_tags = cleaned_data.get('ejemp_tags')
        ejemp_description = cleaned_data.get('ejemp_description')
        ejemp_name = cleaned_data.get('ejemp_name')
        sens_tags = cleaned_data.get('sens_tags')
        sens_description = cleaned_data.get('sens_description')
        sens_name = cleaned_data.get('sens_name')
        completed_icon = cleaned_data.get('completed_icon')
        active_icon = cleaned_data.get('active_icon')
        img_oda = cleaned_data.get('img_oda')
        img_portada = cleaned_data.get('img_portada')
        evaluation_file = cleaned_data.get('evaluation_file')
        oda = super(ODAUpdateForm, self).save(commit=False)
        learning_objective=cleaned_data.get('learning_objective')
        oda.learning_objective =learning_objective

        if subject is not None:
            subject_model = Subject.objects.get(name=subject)
            subject_model.odas.add(oda)
            subject_model.save()

        if bloque is not None:
            oda.section = bloque

        if tags is not None and tags != '':
            tags = tags.split(',')
            for tag_name in tags:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                if tag not in oda.tags.all():
                    oda.tags.add(tag)
            for tag in oda.tags.all():
                if tag.name not in tags:
                    oda.tags.remove(tag)

        if references is not None and references != '':
            references = references.split('|')
            for reference_name in references:
                reference, created = Reference.objects.get_or_create(name=reference_name)
                if reference not in oda.references.all():
                    oda.references.add(reference)
            for reference in oda.references.all():
                if reference.name not in references:
                    oda.references.remove(reference)

        for moment_object in moments:

            try:
                microoda = MicroODA.objects.get(type=MicroODAType.objects.get(name=moment_object[0]), oda=oda)
                microoda.name = '{}_oda_{}'.format(oda.name, moment_object[0])
                microoda.save()
            except MicroODA.DoesNotExist:
                microoda = MicroODA.objects.create(name='{}'.format(moment_object[0]),
                                                   type=MicroODAType.objects.get(moment_object[0]),
                                                   created_by=user, oda=oda)

            moments_names = moment_object[1].split('|')

            for moment in microoda.activities.all():
                if moment.name not in moments_names:
                    microoda.activities.remove(moment)
                microoda.save()

            position = 0
            for moment_name in moments_names:
                if len(moment_name) > 0:
                    momento = microoda.activities.filter(name=moment_name).first()
                    momento.default_position = position
                    momento.save()
                    position += 1

            set_microodas_tags(oda.microodas.get(type=MicroODAType.objects.get(name='application')), apli_tags, apli_description, apli_name)
            set_microodas_tags(oda.microodas.get(type=MicroODAType.objects.get(name='formalization')), forma_tags, forma_description, forma_name)
            set_microodas_tags(oda.microodas.get(type=MicroODAType.objects.get(name='activation')), activ_tags, activ_description, activ_name)
            set_microodas_tags(oda.microodas.get(type=MicroODAType.objects.get(name='exemplification')), ejemp_tags, ejemp_description, ejemp_name)
            set_microodas_tags(oda.microodas.get(type=MicroODAType.objects.get(name='sensitization')), sens_tags, sens_description, sens_name)

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

        if img_oda is not None:
            if isinstance(img_oda, Image):
                img_oda_object = Image.objects.get(folder="ODAs", file=img_oda.file)
                img_oda_object.name = '{}-img_oda'.format(oda.name)
            else:
                img_oda_object = Image.objects.create(name='{}-img_oda'.format(oda.name), folder="ODAs",
                                                          file=img_oda)
                img_oda_object.file_name = os.path.basename(img_oda_object.file.name)
            img_oda_object.save()
            oda.img_oda = img_oda_object

        if img_portada is not None:
            if isinstance(img_portada, Image):
                img_portada_object = Image.objects.get(folder="ODAs", file=img_portada.file)
                img_portada_object.name = '{}-img_portada'.format(oda.name)
            else:
                img_portada_object = Image.objects.create(name='{}-img_portada'.format(oda.name), folder="ODAs",
                                                          file=img_portada)
                img_portada_object.file_name = os.path.basename(img_portada_object.file.name)
            img_portada_object.save()
            oda.img_portada = img_portada_object

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
            #if oda.evaluation is None:
            evaluation_instance = Evaluation.objects.create(
                name='{}_evaluation'.format(oda.name),
                file=evaluation_file,
                file_name="oda_" + str (oda.id) + "_" + evaluation_file.name)
            #else:
             #   evaluation_instance = oda.evaluation

            set_evaluation(evaluation_instance)
            oda.evaluation = evaluation_instance
        oda.temporal = is_draft
        if is_draft:
            oda.zone = 0
        oda.save()

        return oda


def set_microodas_tags(microoda, tags, desc, name):
    """
    Adds tags to each MicroODA
    :param microoda: MicroODA object
    :param tags: Tags string separated by comma
    """
    if desc is not None:
        microoda.description=desc 
        microoda.save()
    if name is not None:
        microoda.name=name 
        microoda.save()

    if tags is not None and tags != '':
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

    if worksheet.nrows == 0:
        return 'Sheet without rows'

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

    evaluation.file.close()
