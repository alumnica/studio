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
        ambit.is_draft = False
        ambit.save()

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
        for subject in ambit.subjects:
            if subject.name not in subjects:
                ambit.subjects.remove(subject)
        ambit.is_draft = False
        ambit.save()

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


def verify_ambits_position(new_ambit):
    ambits_list_raw = Ambit.objects.all().exclude(pk=new_ambit.pk)
    ambits_list = ['na'] * 30
    position = new_ambit.position

    for ambit in ambits_list_raw:
        ambits_list[ambit.position - 1] = ambit

    first_section = ambits_list[0:position - 1]
    second_section = ambits_list[position - 1:]
    counter = 1
    try:
        second_section_space = second_section.index('na')

        for ambit in second_section[0:second_section_space + 1]:
            if isinstance(ambit, Ambit):
                ambit.position = position + counter
                ambit.save()
            counter += 1

    except ValueError:
        first_section_space = [i for i, x in enumerate(first_section) if x == 'na']
        Ambit(second_section[0]).position = position - counter
        Ambit(second_section[0]).save()
        for ambit in first_section[first_section_space[len(first_section_space) - 1] - 1:]:
            if isinstance(ambit, Ambit):
                counter += 1
                ambit.position = position - counter
                ambit.save()
