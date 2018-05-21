import os

from django import forms
from django.core.exceptions import ValidationError

from alumnica_model.models import Subject, Tag
from alumnica_model.models.content import Image, Ambit
from alumnica_model.validators import validate_image_extension, file_size


class SubjectForm(forms.ModelForm):
    tags = forms.CharField(required=False, max_length=60, widget=forms.TextInput(attrs={'id': 'materias-tags',
                                                                                        'name': 'tags-materias'}))
    mp = forms.ImageField(required=False, validators=[validate_image_extension, file_size],
                          widget=forms.FileInput(attrs={'name': 'mp', 'id': 'materia-u', 'class': 'show-for-sr',
                                                        'type': 'file'}))

    class Meta:
        model = Subject
        fields = ['name', 'ambit', 'tags']

    def __init__(self, *args, **kwargs):
        super(SubjectForm, self).__init__(*args, **kwargs)
        self.fields['ambit'].required = False
        self.fields['ambit'].queryset = Ambit.objects.filter(id__in=[ambit.id for ambit in
                                                                     Ambit.objects.filter(is_draft=False)
                                                                     if ambit.subjects.count() < 4])

    def clean(self):
        cleaned_data = super(SubjectForm, self).clean()
        name_subject = cleaned_data.get('name')

        if Subject.objects.filter(name=name_subject).exists():
            error = ValidationError("Subject already exists.", code='subject_error')
            self.add_error('name', error)
            return cleaned_data

        return cleaned_data

    def save_form(self, user, is_draft=False):
        cleaned_data = super(SubjectForm, self).clean()
        background_image = cleaned_data.get('mp')

        subject = super(SubjectForm, self).save(commit=False)
        subject.created_by = user

        if background_image is not None:
            if isinstance(background_image, Image):
                subject.background_image = Image.objects.get(folder=background_image.folder, file=background_image.file)
                subject.background_image.name = '{}-subject_background_image'.format(subject.name)
                subject.background_image.save()
            else:
                new_image = Image.objects.create(
                    name='{}-subject_background_image'.format(subject.name),
                    file=background_image,
                    folder='subjects'
                )
                subject.background_image = new_image

        subject.save()

        tags = cleaned_data.get('tags')
        if tags:
            tags = tags.split(',')

        for tag_name in tags:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            subject.tags.add(tag)

        subject.temporal = is_draft
        subject.save()
        return subject


class UpdateSubjectForm(forms.ModelForm):
    tags = forms.CharField(required=False,
                           widget=forms.TextInput(attrs={'id': 'materias-tags', 'name': 'tags-materias'}))
    mp = forms.ImageField(required=False, widget=forms.FileInput(attrs={'name': 'mp', 'id': 'materia-u',
                                                                        'class': 'show-for-sr', 'type': 'file'}))

    class Meta:
        model = Subject
        fields = ['name', 'ambit', 'tags']

    def __init__(self, *args, **kwargs):
        super(UpdateSubjectForm, self).__init__(*args, **kwargs)
        subject = kwargs['instance']
        self.fields['ambit'].required = False
        self.fields['ambit'].queryset = Ambit.objects.filter(id__in=[ambit.id for ambit in
                                                                     Ambit.objects.filter(is_draft=False)
                                                                     if
                                                                     ambit.subjects.count() < 4 or ambit == subject.ambit])

    def save_form(self, is_draft=False):
        cleaned_data = super(UpdateSubjectForm, self).clean()
        background_image = cleaned_data.get('mp')
        subject = super(UpdateSubjectForm, self).save(commit=False)

        tags = cleaned_data.get('tags')

        if tags is not None and tags is not '':
            tags = tags.split(',')

        tag = None
        for tag_name in tags:
            tag, created = Tag.objects.get_or_create(name=tag_name)

        if tag not in subject.tags.all():
            subject.tags.add(tag)

        for tag in subject.tags.all():
            if tag.name not in tags:
                subject.tags.remove(tag)

        if background_image is not None:
            if isinstance(background_image, Image):
                subject.background_image = Image.objects.get(folder=background_image.folder, file=background_image.file)
                subject.background_image.name = '{}-subject_background_image'.format(subject.name)
                subject.background_image.save()
            else:
                new_image = Image.objects.create(
                    name='{}-subject_background_image'.format(subject.name),
                    file=background_image,
                    folder='subjects'
                )

        new_image.file_name = os.path.basename(new_image.filename)
        new_image.save()

        subject.background_image = new_image
        subject.temporal = is_draft
        subject.save()
        return subject


class ImageForm(forms.ModelForm):
    file = forms.ImageField(required=False, validators=[file_size],
                            widget=forms.FileInput(attrs={'class': 'show-for-sr upload_section', 'type': 'file'}))

    class Meta:
        model = Image
        fields = ['file']


class BaseImageFormset(forms.BaseFormSet):
    def __init__(self, *args, **kwargs):
        if 'form_instances' in kwargs.keys():
            self.form_instances = kwargs.pop('form_instances')
        else:
            self.form_instances = []

        super(BaseImageFormset, self).__init__(*args, **kwargs)

    def get_form_kwargs(self, index):
        kwargs = super(BaseImageFormset, self).get_form_kwargs(index)

        if len(self.form_instances) > index:
            kwargs['instance'] = self.form_instances[index]

        return kwargs
