from django import forms
from django.core.exceptions import ValidationError

from alumnica_model.models import AmbitModel
from alumnica_model.models.content import ImageModel, TagModel, SubjectModel


class CreateAmbitForm(forms.ModelForm):
    background_image_field = forms.CharField()
    class Meta:
        model = AmbitModel
        fields = ['is_published_field', 'name_field', 'position_field',
                  'background_image_field']

    def clean(self):
        cleaned_data = super(CreateAmbitForm, self).clean()
        subjects = cleaned_data.get('subjects')
        for subject in subjects:
            if not SubjectModel.objects.exists(name=subject):
                error = ValidationError("Subject does not exist.", code='subject_error')
                self.add_error('name_field', error)
        return cleaned_data

    def save_form(self, user):
        cleaned_data = super(CreateAmbitForm, self).clean()
        subjects = cleaned_data.get('subjects')
        tags = cleaned_data.get('tags')
        color = cleaned_data.get('colors')

        ambit = super(CreateAmbitForm, self).save(commit=False)
        ambit.created_by = user
        ambit.color = color
        for tag_name in tags:
            tag_model = TagModel.objects.get(name=tag_name)
            if not tag_model is None:
                tag_model = TagModel.objects.create(name=tag_name, ambit=ambit)
            ambit.tags.add(tag_model)

        for subject_name in subjects:
            subject_model = SubjectModel.objects.get(name=subject_name)
            ambit.subjects.add(subject_model)

        ambit.save()

class AmbitForm(forms.ModelForm):
    class Meta:
        model = AmbitModel
        fields = ['name_field', 'is_published_field', 'position_field', 'subjects_field', 'tags_field']
