from django import forms
from alumnica_model.models import AmbitModel


class CreateAmbitoForm(forms.ModelForm):
    class Meta:
        model = AmbitModel
        fields = ['is_published_field', 'name_field', 'tags_field', 'position_field',
                  'background_image_field']

    def save_form(self, user, color):
        ambit = super(CreateAmbitoForm, self).save(commit=False)
        ambit.created_by = user
        ambit.save()