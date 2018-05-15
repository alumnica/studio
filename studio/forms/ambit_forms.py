from django import forms
from django.core.exceptions import ValidationError

from alumnica_model.models import AmbitModel
from alumnica_model.models.content import TagModel, SubjectModel, ImageModel, ProgramModel
from alumnica_model.validators import unique_ambit_name_validator, file_size


class CreateAmbitForm(forms.ModelForm):
    name_field = forms.CharField(required=False, max_length=50, widget=forms.TextInput(attrs={'class': 'text_number'}),
                                 validators=[unique_ambit_name_validator])

    ap = forms.ImageField(required=False, validators=[file_size], widget=forms.FileInput(attrs={'name': 'ap',
                                                                                                'id': 'ambito-u',
                                                                                                'class': 'is-hidden',
                                                                                                'type': 'file'}))

    class Meta:
        model = AmbitModel
        fields = ['name_field']

    def save_form(self, user, subjects, tags, color):
        cleaned_data = super(CreateAmbitForm, self).clean()
        ambit = super(CreateAmbitForm, self).save(commit=False)
        ambit.created_by = user
        ambit.color = color

        image = cleaned_data.get('ap')
        if isinstance(image, ImageModel):
            image_model = ImageModel.objects.get(name_field="ambits", file_field=image.file_field)
        else:
            image_model = ImageModel.objects.create(name_field="ambits", file_field=image)

        image_model.temporal_field = False
        ambit.background_image = image_model
        ambit.program = ProgramModel.objects.get(name_field="Primaria")
        ambit.save()

        for tag_name in tags:
            tag, created = TagModel.objects.get_or_create(name_field=tag_name)

            tag.temporal = False
            tag.save()
            ambit.tags_field.add(tag)

        if subjects is not None:
            subjects = subjects.split(',')
            for subject_name in subjects:
                try:
                    subject_model = SubjectModel.objects.get(name_field=subject_name)
                    ambit.subjects_field.add(subject_model)
                except SubjectModel.DoesNotExist:
                    pass
        ambit.is_draft_field = False
        ambit.save()

    def save_as_draft(self, user, subjects, tags, color):
        cleaned_data = super(CreateAmbitForm, self).clean()
        ambit = super(CreateAmbitForm, self).save(commit=False)
        ambit.created_by = user
        ambit.program = ProgramModel.objects.get(name_field="Primaria")
        ambit.color = color

        if cleaned_data.get('ap') is not None:
            image = cleaned_data.get('ap')
            if isinstance(image, ImageModel):
                image_model = ImageModel.objects.get(name_field="ambits", file_field=image.file_field)
            else:
                image_model = ImageModel.objects.create(name_field="ambits", file_field=image)

            ambit.background_image = image_model
        ambit.save()
        for tag_name in tags:
            tag, created = TagModel.objects.get_or_create(name_field=tag_name)

            tag.temporal = True
            tag.save()
            ambit.tags_field.add(tag)

        if subjects is not None:
            subjects = subjects.split(',')
            for subject_name in subjects:
                try:
                    subject_model = SubjectModel.objects.get(name_field=subject_name)
                    ambit.subjects_field.add(subject_model)
                except SubjectModel.DoesNotExist:
                    pass

        ambit.save()

class UpdateAmbitForm(forms.ModelForm):
    name_field = forms.CharField(required=False, max_length=50, widget=forms.TextInput(attrs={'class': 'text_number'}))

    ap = forms.ImageField(required=False, validators=[file_size], widget=forms.FileInput(attrs={'name': 'ap',
                                                                                                'id': 'ambito-u',
                                                                                                'class': 'is-hidden',
                                                                                                'type': 'file'}))
    class Meta:
        model = AmbitModel
        fields = ['name_field']

    def save_form(self, subjects, tags, color):
        cleaned_data = super(UpdateAmbitForm, self).clean()
        ambit = AmbitModel.objects.get(name_field=cleaned_data.get('name_field'))
        ambit.color = color

        image = cleaned_data.get('ap')

        if image is not None:
            if isinstance(image, ImageModel):
                image_model = ImageModel.objects.get(name_field="ambits", file_field=image.file_field)
            else:
                image_model = ImageModel.objects.create(name_field="ambits", file_field=image)
            image_model.temporal = False
            image_model.save()
            ambit.background_image = image_model
        ambit.save()

        for tag_name in tags:
            tag, created = TagModel.objects.get_or_create(name_field=tag_name)
            if tag not in ambit.tags:
                ambit.tags_field.add(tag)
        for tag in ambit.tags:
            if tag.name not in tags:
                ambit.tags_field.remove(tag)

        if subjects is not None:
            subjects = subjects.split(',')
            for subject_name in subjects:
                try:
                    subject_model = SubjectModel.objects.get(name_field=subject_name)
                    ambit.subjects_field.add(subject_model)
                except SubjectModel.DoesNotExist:
                    pass
        for subject in ambit.subjects:
            if subject.name not in subjects:
                ambit.subjects_field.remove(subject)
        ambit.is_draft_field = False
        ambit.save()

    def save_as_draft(self, subjects, tags, color):
        cleaned_data = super(UpdateAmbitForm, self).clean()
        ambit = AmbitModel.objects.get(name_field=cleaned_data.get('name_field'))
        ambit.color = color

        if cleaned_data.get('ap') is not None:
            image = cleaned_data.get('ap')
            if isinstance(image, ImageModel):
                image_model = ImageModel.objects.get(name_field="ambits", file_field=image.file_field)
            else:
                image_model = ImageModel.objects.create(name_field="ambits", file_field=image)

            image_model.save()
            ambit.background_image = image_model
        ambit.save()
        for tag_name in tags:
            tag, created = TagModel.objects.get_or_create(name_field=tag_name)

            tag.temporal = True
            tag.save()
            ambit.tags_field.add(tag)

        if subjects is not None:
            subjects = subjects.split(',')
            for subject_name in subjects:
                try:
                    subject_model = SubjectModel.objects.get(name_field=subject_name)
                    ambit.subjects_field.add(subject_model)
                except SubjectModel.DoesNotExist:
                    pass
        ambit.is_draft_field = True
        ambit.save()


def verify_ambits_position(new_ambit):
    ambits_list_raw = AmbitModel.objects.all().exclude(pk=new_ambit.pk)
    ambits_list = ['na']*30
    position = new_ambit.position_field

    for ambit in ambits_list_raw:
        ambits_list[ambit.position - 1] = ambit

    first_section = ambits_list[0:position-1]
    second_section = ambits_list[position-1:]
    counter = 1
    try:
        second_section_space = second_section.index('na')

        for ambit in second_section[0:second_section_space+1]:
            if isinstance(ambit, AmbitModel):
                ambit.position_field = position + counter
                ambit.save()
            counter += 1

    except ValueError:
        first_section_space = [i for i,x in enumerate(first_section) if x == 'na']
        AmbitModel(second_section[0]).position_field = position-counter
        AmbitModel(second_section[0]).save()
        for ambit in first_section[first_section_space[len(first_section_space)-1]-1:]:
            if isinstance(ambit, AmbitModel):
                counter += 1
                ambit.position_field = position - counter
                ambit.save()


