
from django import forms
from django.core.exceptions import ValidationError

from alumnica_model.models import SubjectModel, TagModel
from alumnica_model.models.content import ImageModel, AmbitModel
from alumnica_model.validators import validate_image_extension, file_size


class SubjectForm(forms.ModelForm):
    tags_field = forms.CharField(max_length=60, widget=forms.TextInput(attrs={'id': 'materias-tags',
                                                                              'name': 'tags-materias'}))
    mp = forms.ImageField(validators=[validate_image_extension, file_size],
                          widget=forms.FileInput(attrs={'name': 'mp', 'id': 'materia-u', 'class': 'show-for-sr',
                                                        'type': 'file'}))

    class Meta:
        model = SubjectModel
        fields = ['name_field', 'ambit_field', 'tags_field']

    def __init__(self, *args, **kwargs):
        super(SubjectForm, self).__init__(*args, **kwargs)
        self.fields['ambit_field'].queryset = AmbitModel.objects.filter(id__in=[ambit.id for ambit in
                                                   AmbitModel.objects.filter(is_published_field=True)
                                                   if ambit.subjects.count() < 4])

    def clean(self):
        cleaned_data = super(SubjectForm, self).clean()
        name_subject = cleaned_data.get('name_field')

        if SubjectModel.objects.filter(name_field=name_subject).exists():
            error = ValidationError("Subject already exists.", code='subject_error')
            self.add_error('name_field', error)
            return cleaned_data

        ambit = cleaned_data.get('ambit_field')

        if ambit.subjects.count() > 3:
            error = ValidationError("This ambit already has 4 subjects assigned.", code='subject_error')
            self.add_error('name_field', error)
            return cleaned_data

        return cleaned_data

    def save_form(self, user):
        cleaned_data = super(SubjectForm, self).clean()
        background_image = cleaned_data.get('mp')

        subject = super(SubjectForm, self).save(commit=False)
        subject.created_by = user

        if isinstance(background_image, ImageModel):
            subject.background_image_field = ImageModel.objects.get(name_field=background_image.name,
                                                                    file_field=background_image.file_field)
        else:
            new_image = ImageModel.objects.create(name_field="subjects", file_field=background_image)
            subject.background_image_field = new_image

        subject.save()
        subject.update_sections()
        tags = cleaned_data.get('tags_field').split(',')
        for tag_name in tags:
            tag, created = TagModel.objects.get_or_create(name_field=tag_name)
            subject.tags_field.add(tag)

        subject.save()
        return subject


class UpdateSubjectForm(forms.ModelForm):
    tags_field = forms.CharField(widget=forms.TextInput(attrs={'id': 'materias-tags', 'name': 'tags-materias'}))
    mp = forms.ImageField(required=False, widget=forms.FileInput(attrs={'name': 'mp', 'id': 'materia-u',
                                                                        'class': 'show-for-sr', 'type': 'file'}))


    class Meta:
        model = SubjectModel
        fields = ['name_field', 'ambit_field', 'tags_field']

    def __init__(self, *args, **kwargs):
        super(UpdateSubjectForm, self).__init__(*args, **kwargs)
        subject = kwargs['instance']
        self.fields['ambit_field'].queryset = AmbitModel.objects.filter(id__in=[ambit.id for ambit in
                                                   AmbitModel.objects.filter(is_published_field=True)
                                                   if ambit.subjects.count() < 4 or ambit == subject.ambit])

    def save_form(self):
        cleaned_data = super(UpdateSubjectForm, self).clean()
        background_image = cleaned_data.get('mp')
        subject = super(UpdateSubjectForm, self).save(commit=False)
        tags = cleaned_data.get('tags_field').split(',')
        for tag_name in tags:
            tag, created = TagModel.objects.get_or_create(name_field=tag_name)
            if tag not in subject.tags:
                subject.tags_field.add(tag)
        for tag in subject.tags:
            if tag.name not in tags:
                subject.tags_field.remove(tag)
        if background_image is not None:
            if isinstance(background_image, ImageModel):
                subject.background_image_field = ImageModel.objects.get(name_field=background_image.name,
                                                                        file_field=background_image.file_field)
            else:
                new_image = ImageModel.objects.create(name_field="subjects", file_field=background_image)

                subject.background_image_field = new_image

        subject.save()
        subject.update_sections()
        return subject


class ImageModelForm(forms.ModelForm):
    file_field = forms.ImageField(validators=[file_size], widget=forms.FileInput(attrs={'class': 'show-for-sr',
                                                                                        'type': 'file'}))

    class Meta:
        model = ImageModel
        fields = ['file_field']


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
