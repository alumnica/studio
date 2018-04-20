from django import forms

from alumnica_model.models import ODAModel
from alumnica_model.models.content import ODAInSubjectModel, ImageModel, SubjectModel
from alumnica_model.validators import file_size


class ODAModelForm(forms.Form):
    oda_name = forms.CharField(required=True, max_length=120)
    active_icon_field = forms.ImageField(validators=[file_size], widget=forms.FileInput(attrs={'class': 'is-hidden', 'type': 'file'}))
    completed_icon_field = forms.ImageField(validators=[file_size], widget=forms.FileInput(attrs={'class': 'is-hidden', 'type': 'file'}))

    def save_form(self, user, section):
        cleaned_data = self.clean()
        oda_name = cleaned_data.get('oda_name')

        active_image = cleaned_data.get('active_icon_field')
        if ImageModel.objects.all().filter(name_field=active_image.name).exists():
            active_icon = ImageModel.objects.get(name_field=active_image.name)
        else:
            active_icon = ImageModel.objects.create(
                name_field=("oda_{}_section{}_active_icon".format(oda_name, section)), file_field=active_image)

        completed_image = cleaned_data.get('completed_icon_field')
        if ImageModel.objects.all().filter(name_field=completed_image.name).exists():
            completed_icon = ImageModel.objects.get(name_field=completed_image.name)
        else:
            completed_icon = ImageModel.objects.create(
                name_field=("oda_{}_section{}_completed_icon".format(oda_name, section)), file_field=completed_image)

        oda, oda_created = ODAModel.objects.get_or_create(name_field=oda_name, created_by_field=user)


        oda_in_subject, created = ODAInSubjectModel.objects.get_or_create(oda_field=oda, section_field=section,
                                                                          active_icon_field=active_icon,
                                                                          completed_icon_field = completed_icon)
        if not created:
            oda_in_subject.active_icon_field = active_icon
            oda_in_subject.completed_icon_field = completed_icon

        oda_in_subject.save()
        return oda_in_subject


class BaseODAModelFormset(forms.BaseFormSet):

    def __init__(self, *args, **kwargs):
        super(BaseODAModelFormset, self).__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = False


class ODAsSectionView(forms.ModelForm):
    name_field = forms.CharField(widget=forms.TextInput(attrs={'class': 'is-hidden'}))

    class Meta:
        model = SubjectModel
        fields = ['name_field']


class ODAsPositionForm(forms.Form):
    subject_field = forms.CharField(widget=forms.TextInput(attrs={'class': 'is-hidden'}))


class ODAsPreviewForm(forms.Form):
    subject_field = forms.CharField(widget=forms.TextInput(attrs={'class': 'is-hidden'}))
