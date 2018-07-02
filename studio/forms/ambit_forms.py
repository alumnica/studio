import os

from django import forms

from alumnica_model.models import Ambit
from alumnica_model.models.content import Tag, Subject, Image, Program
from alumnica_model.validators import unique_ambit_name_validator, file_size


class CreateAmbitForm(forms.ModelForm):
    name = forms.CharField(required=False, max_length=50, widget=forms.TextInput(attrs={'class': 'text_number'}),
                           validators=[unique_ambit_name_validator])

    ap = forms.ImageField(required=False, validators=[file_size], widget=forms.FileInput(attrs={'name': 'ap',
                                                                                                'id': 'ambito-u',
                                                                                                'class': 'is-hidden',
                                                                                                'type': 'file'}))

    class Meta:
        model = Ambit
        fields = ['name']

    def save_form(self, user, subjects, tags, color):
        cleaned_data = super(CreateAmbitForm, self).clean()
        ambit = super(CreateAmbitForm, self).save(commit=False)
        ambit.created_by = user
        ambit.color = color

        image = cleaned_data.get('ap')
        if isinstance(image, Image):
            image_model = Image.objects.get(folder="ambits", file=image.file)
            image_model.name = '{}-ambit_image'.format(ambit.name)
            image_model.save()
        else:
            image_model = Image.objects.create(name='{}-ambit_image'.format(ambit.name),
                                               folder="ambits", file=image)

        image_model.file_name = os.path.basename(image_model.file.name)
        image_model.save()
        ambit.background_image = image_model
        ambit.program = Program.objects.get(name="Primaria")
        ambit.save()

        for tag_name in tags:
            tag, created = Tag.objects.get_or_create(name=tag_name)

            tag.temporal = False
            tag.save()
            ambit.tags.add(tag)

        if subjects is not None:
            subjects = subjects.split(',')
            for subject_name in subjects:
                try:
                    subject_model = Subject.objects.get(name=subject_name)
                    ambit.subjects.add(subject_model)
                except Subject.DoesNotExist:
                    pass
        all_subjects_finalized = True
        for subject in ambit.subjects.all():
            if subject.temporal:
                all_subjects_finalized = False
                break

        ambit.is_draft = not all_subjects_finalized
        ambit.is_published = all_subjects_finalized
        if ambit.position == 0:
            ambit.position = Ambit.objects.all().count()
        ambit.save()

        return ambit, all_subjects_finalized

    def save_as_draft(self, user, subjects, tags, color):
        cleaned_data = super(CreateAmbitForm, self).clean()
        ambit = super(CreateAmbitForm, self).save(commit=False)
        ambit.created_by = user
        ambit.program = Program.objects.get(name="Primaria")
        ambit.color = color

        if cleaned_data.get('ap') is not None:
            image = cleaned_data.get('ap')
            if isinstance(image, Image):
                image_model = Image.objects.get(folder="ambits", file=image.file)
                image_model.name = '{}-ambit_image'.format(ambit.name)
                image_model.save()
            else:
                image_model = Image.objects.create(name='{}-ambit_image'.format(ambit.name),
                                                   folder="ambits", file=image)

            image_model.file_name = os.path.basename(image_model.file.name)
            image_model.save()

            ambit.background_image = image_model
        ambit.save()
        for tag_name in tags:
            tag, created = Tag.objects.get_or_create(name=tag_name)

            tag.temporal = True
            tag.save()
            ambit.tags.add(tag)

        if subjects is not None:
            subjects = subjects.split(',')
            for subject_name in subjects:
                try:
                    subject_model = Subject.objects.get(name=subject_name)
                    ambit.subjects.add(subject_model)
                except Subject.DoesNotExist:
                    pass

        ambit.save()


class UpdateAmbitForm(forms.ModelForm):
    name = forms.CharField(required=False, max_length=50, widget=forms.TextInput(attrs={'class': 'text_number'}))

    ap = forms.ImageField(required=False, validators=[file_size], widget=forms.FileInput(attrs={'name': 'ap',
                                                                                                'id': 'ambito-u',
                                                                                                'class': 'is-hidden',
                                                                                                'type': 'file'}))

    class Meta:
        model = Ambit
        fields = ['name']

    def save_form(self, subjects, tags, color):
        cleaned_data = super(UpdateAmbitForm, self).clean()
        ambit = Ambit.objects.get(name=cleaned_data.get('name'))
        ambit.color = color

        image = cleaned_data.get('ap')

        if image is not None:
            if isinstance(image, Image):
                image_model = Image.objects.get(folder="ambits", file=image.file)
                image_model.name = '{}-ambit_image'.format(ambit.name)
                image_model.save()
            else:
                image_model = Image.objects.create(name='{}-ambit_image'.format(ambit.name),
                                                   folder="ambits", file=image)
            image_model.file_name = os.path.basename(image_model.file.name)
            image_model.save()
            image_model.save()
            ambit.background_image = image_model
        ambit.save()

        for tag_name in tags:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            if tag not in ambit.tags.all():
                ambit.tags.add(tag)
        for tag in ambit.tags.all():
            if tag.name not in tags:
                ambit.tags.remove(tag)

        if subjects is not None:
            subjects = subjects.split(',')
            for subject_name in subjects:
                try:
                    subject_model = Subject.objects.get(name=subject_name)
                    ambit.subjects.add(subject_model)
                except Subject.DoesNotExist:
                    pass
        for subject in ambit.subjects.all():
            if subject.name not in subjects:
                ambit.subjects.remove(subject)

        all_subjects_finalized = True
        for subject in ambit.subjects.all():
            if subject.temporal:
                all_subjects_finalized = False
                break

        ambit.is_draft = not all_subjects_finalized
        ambit.is_published = all_subjects_finalized
        if ambit.position == 0:
            ambit.position = Ambit.objects.all().count()
        ambit.save()

        return ambit, all_subjects_finalized

    def save_as_draft(self, subjects, tags, color):
        cleaned_data = super(UpdateAmbitForm, self).clean()
        ambit = Ambit.objects.get(name=cleaned_data.get('name'))
        ambit.color = color

        if cleaned_data.get('ap') is not None:
            image = cleaned_data.get('ap')
            if isinstance(image, Image):
                image_model = Image.objects.get(folder="ambits", file=image.file)
                image_model.name = '{}-ambit_image'.format(ambit.name)
                image_model.save()
            else:
                image_model = Image.objects.create(name='{}-ambit_image'.format(ambit.name),
                                                   folder="ambits", file=image)

            image_model.file_name = os.path.basename(image_model.file.name)
            image_model.save()
            ambit.background_image = image_model
        ambit.save()
        for tag_name in tags:
            tag, created = Tag.objects.get_or_create(name=tag_name)

            tag.temporal = True
            tag.save()
            ambit.tags.add(tag)

        if subjects is not None:
            subjects = subjects.split(',')
            for subject_name in subjects:
                try:
                    subject_model = Subject.objects.get(name=subject_name)
                    ambit.subjects.add(subject_model)
                except Subject.DoesNotExist:
                    pass
        ambit.is_draft = True
        ambit.save()
