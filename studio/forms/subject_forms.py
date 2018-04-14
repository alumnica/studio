
from django import forms
from django.core.exceptions import ValidationError

from alumnica_model.models import SubjectModel, TagModel
from alumnica_model.models.content import ImageModel


class SubjectForm(forms.ModelForm):
    tags_field = forms.CharField(widget=forms.TextInput(attrs={'id': 'materias-tags', 'name': 'tags-materias'}))

    class Meta:
        model = SubjectModel
        fields = ['name_field', 'ambit_field', 'number_of_sections_field', 'tags_field']

    def clean(self):
        cleaned_data = super(SubjectForm, self).clean()
        name_subject = cleaned_data.get('name_field')

        if SubjectModel.objects.filter(name_field=name_subject).exists():
            error = ValidationError("Subject already exists.", code='subject_error')
            self.add_error('name_field', error)

        ambit = cleaned_data.get('ambit_field')
        if ambit.subjects.count() > 3:
            error = ValidationError("This ambit already has 4 subjects assigned.", code='subject_error')
            self.add_error('name_field', error)

        return cleaned_data

    #def save_form(self, user, image):
    def save_form(self, user):
        cleaned_data = super(SubjectForm, self).clean()
        subject = super(SubjectForm, self).save(commit=False)
        subject.created_by = user.profile
        subject.save()
        tags = cleaned_data.get('tags_field').split(',')
        for tag_name in tags:
            tag, created = TagModel.objects.get_or_create(name_field=tag_name)
            subject.tags_field.add(tag)

        #if image is not None:
         #   subject.background_image = image

        subject.save()
        return subject


class UpdateSubjectForm(forms.ModelForm):
    tags_field = forms.CharField(widget=forms.TextInput(attrs={'id': 'materias-tags', 'name': 'tags-materias'}))

    class Meta:
        model = SubjectModel
        fields = ['name_field', 'ambit_field', 'number_of_sections_field', 'tags_field']



    def save_form(self):
        cleaned_data = super(UpdateSubjectForm, self).clean()
        subject = super(UpdateSubjectForm, self).save(commit=False)
        tags = cleaned_data.get('tags_field').split(',')
        for tag_name in tags:
            tag, created = TagModel.objects.get_or_create(name_field=tag_name)
            if tag not in subject.tags:
                subject.tags_field.add(tag)
        for tag in subject.tags:
            if tag.name not in tags:
                subject.tags_field.remove(tag)

        #if image is not None:
         #   subject.background_image = image

        subject.save()
        return subject



class ImageModelForm(forms.ModelForm):
    class Meta:
        model = ImageModel
        exclude = ['temporal_field']


class BaseImageModelFormset(forms.BaseFormSet):

    def __init__(self, *args, **kwargs):
        if 'form_instances' in kwargs.keys():
            self.form_instances = kwargs.pop('form_instances')
        else:
            self.form_instances = []

        super(BaseImageModelFormset, self).__init__(*args, **kwargs)


    def get_form_kwargs(self, index):
        kwargs = super(BaseImageModelFormset, self).get_form_kwargs(index)
        if len(self.form_instances) > index:
            kwargs['instance'] = self.form_instances[index]
        return kwargs

class SubjectSectionsForm(forms.ModelForm):
    class Meta:
        model = SubjectModel
        fields = ['name_field', 'number_of_sections_field']
