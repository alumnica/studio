from django.core.exceptions import ValidationError
from django import forms

from alumnica_model.models import SubjectModel, ODAModel
from alumnica_model.models.content import ODAInSubjectModel


class ODAModelForm(forms.ModelForm):
    oda_name = forms.CharField(max_length=120)
    class Meta:
        model = ODAInSubjectModel
        fields = ['oda_name', 'active_icon_field', 'completed_icon_field']


class BaseODAModelFormset(forms.BaseFormSet):

    def __init__(self, *args, **kwargs):
        if 'form_instances' in kwargs.keys():
            self.form_instances = kwargs.pop('form_instances')
        else:
            self.form_instances = []

        super(BaseODAModelFormset, self).__init__(*args, **kwargs)


    def get_form_kwargs(self, index):
        kwargs = super(BaseODAModelFormset, self).get_form_kwargs(index)
        if len(self.form_instances) > index:
            kwargs['instance'] = self.form_instances[index]
        return kwargs



class ODAsPositionForm(forms.Form):
    section_field = forms.CharField()
    subject_field = forms.CharField()
