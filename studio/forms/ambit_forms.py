from django import forms
from django.core.exceptions import ValidationError

from alumnica_model.models import AmbitModel
from alumnica_model.models.content import TagModel, SubjectModel, ImageModel, ProgramModel
from alumnica_model.validators import unique_ambit_name_validator, file_size


class CreateAmbitForm(forms.ModelForm):
    name_field = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'text_number'}),
                                 validators=[unique_ambit_name_validator])
    position_field = forms.IntegerField(max_value=30)

    ap = forms.ImageField(required=False, validators=[file_size], widget=forms.FileInput(attrs={'name': 'ap',
                                                                                                'id': 'ambito-u',
                                                                                                'class': 'is-hidden',
                                                                                                'type': 'file'}))

    class Meta:
        model = AmbitModel
        fields = ['name_field', 'position_field']


    def save_form(self, user, subjects, tags, color):
        cleaned_data = super(CreateAmbitForm, self).clean()
        ambit = super(CreateAmbitForm, self).save(commit=False)
        ambit.created_by = user.profile
        ambit.color = color

        image = cleaned_data.get('ap')
        image_model = ImageModel.objects.create(name_field=("ambit_{}_background".format(ambit.name)),
                                                file_field=image)
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

        ambit.save()

class UpdateAmbitForm(forms.ModelForm):
    name_field = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'text_number'}))
    position_field = forms.IntegerField(max_value=30)

    ap = forms.ImageField(required=False, validators=[file_size], widget=forms.FileInput(attrs={'name': 'ap',
                                                                                                'id': 'ambito-u',
                                                                                                'class': 'is-hidden',
                                                                                                'type': 'file'}))


    def save_form(self, subjects, tags, color):
        cleaned_data = super(UpdateAmbitForm, self).clean()
        ambit = super(UpdateAmbitForm, self).save(commit=False)
        ambit.color = color

        image = cleaned_data.get('ap')

        if image is not None:
            image_model, created = ImageModel.objects.get_or_create(name_field=("ambit_{}_background".format(ambit.name)),
                                                file_field=image)
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

        ambit.save()

    class Meta:
        model = AmbitModel
        fields = ['name_field', 'position_field']
