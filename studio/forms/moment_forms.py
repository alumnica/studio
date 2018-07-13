from django import forms

from alumnica_model.models import Moment, Tag, ODA
from alumnica_model.models.content import MomentType, Subject, MicroODAType


class MomentCreateForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'id': 'h5p-name'}))
    tags = forms.CharField(widget=forms.TextInput(attrs={'id': 'momento-tags',
                                                         'class': 'u-margin-bottom-small selectized'}))
    content = forms.FileField(widget=forms.FileInput(attrs={'class': 'show-for-sr', 'id': 'h5p-upload'}))

    class Meta:
        model = Moment
        fields = ['name', 'tags', 'content']

    def save_form(self, user, subject_name, oda_name, microoda_type, moment_type, h5p_url):
        cleaned_data = super(MomentCreateForm, self).clean()
        moment = super(MomentCreateForm, self).save(commit=False)
        tags = cleaned_data.get('tags').split(',')
        subject = Subject.objects.get(name=subject_name)
        oda = subject.odas.get(name=oda_name)
        microoda = oda.microodas.get(type=MicroODAType.objects.get(name=microoda_type))

        moment.folder = 'moments'
        moment.created_by = user
        moment.type = MomentType.objects.get(name=moment_type)
        moment.file_name = h5p_url
        moment.microoda = microoda
        moment.save()

        for tag_name in tags:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            tag.save()
            moment.tags.add(tag)

        moment.save()


class MomentUpdateForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'id': 'h5p-name'}))

    tags = forms.CharField(widget=forms.TextInput(attrs={'id': 'momento-tags',
                                                         'class': 'u-margin-bottom-small selectized'}))
    content = forms.FileField(required=False, widget=forms.FileInput(attrs={'class': 'show-for-sr', 'id': 'h5p-upload'}))

    class Meta:
        model = Moment
        fields = ['name', 'tags', 'content']

    def save_form(self, subject_name, oda_name, microoda_type, moment_type, h5p_url):
        cleaned_data = super(MomentUpdateForm, self).clean()
        moment = super(MomentUpdateForm, self).save(commit=False)
        tags = cleaned_data.get('tags').split(',')
        subject = Subject.objects.get(name=subject_name)
        oda = subject.odas.get(name=oda_name)
        microoda = oda.microodas.get(type=MicroODAType.objects.get(name=microoda_type))

        moment.folder = 'moments'
        moment.type = MomentType.objects.get(name=moment_type)

        if h5p_url is not None:
            moment.file_name = h5p_url
        moment.microoda = microoda
        moment.save()

        for tag_name in tags:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            if tag not in moment.tags.all():
                moment.tags.add(tag)
        for tag in moment.tags.all():
            if tag.name not in tags:
                moment.tags.remove(tag)
        moment.save()