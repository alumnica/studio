from django import forms

from alumnica_model.models import Moment, Tag
from alumnica_model.models.content import MomentType, Subject, MicroODAType, Content
#from alumnica_model.models.h5p import H5Package


class ContentForm(forms.ModelForm):
    url_h5p = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'id': 'url_h5p'}))
    library_h5p = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'id': 'library_h5p'}))
    content = forms.FileField(required=False,
                              widget=forms.FileInput(attrs={'class': 'show-for-sr', 'id': 'content'}))

    class Meta:
        model = Content
        fields = ['url_h5p', 'library_h5p', 'content']

class MomentCreateForm(forms.ModelForm):
    """
    Save new Momento object form
    """
    name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'id': 'name'}))
    tags = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'id': 'momento-tags',
                                                         'class': 'u-margin-bottom-small selectized'}))
    



    class Meta:
        model = Moment
        fields = ['name', 'tags']

    def save_form(self, user, subject_name, oda_name, microoda_type, moment_type, content_id ):
        print ('In create moment')

        cleaned_data = super(MomentCreateForm, self).clean()
        moment = super(MomentCreateForm, self).save(commit=False)
        print (moment)
        tags = cleaned_data.get('tags').split(',')
        subject = Subject.objects.get(name=subject_name)
        oda = subject.odas.get(name=oda_name)
        microoda = oda.microodas.get(type=MicroODAType.objects.get(name=microoda_type))

        moment.folder = 'Momentos'
        moment.created_by = user
        moment.type = moment_type # MomentType.objects.get(name=moment_type)
        #moment.h5p_package = H5Package.objects.get(job_id=h5p_id)
        moment.microoda = microoda
        moment.content = Content.objects.get(pk=int (content_id))
        moment.save()

        for tag_name in tags:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            tag.save()
            moment.tags.add(tag)

        moment.save()


class MomentUpdateForm(forms.ModelForm):
    """
    Update existing Momento object form
    """
    name = forms.CharField(widget=forms.TextInput(attrs={'id': 'name'}))
    tags = forms.CharField(widget=forms.TextInput(attrs={'id': 'momento-tags',
                                                         'class': 'u-margin-bottom-small selectized'}))
    #content = forms.FileField(required=False,
     #                         widget=forms.FileInput(attrs={'class': 'show-for-sr', 'id': 'h5p-upload'}))
    

    class Meta:
        model = Moment
        fields = ['name', 'tags']

    def save_form(self, subject_name, oda_name, microoda_type, moment_type, h5p_id = None):
        print ('in update form')
        cleaned_data = super(MomentUpdateForm, self).clean()
        moment = super(MomentUpdateForm, self).save(commit=False)
        print (moment)
        tags = cleaned_data.get('tags').split(',')
        subject = Subject.objects.get(name=subject_name)
        oda = subject.odas.get(name=oda_name)
        microoda = oda.microodas.get(type=MicroODAType.objects.get(name=microoda_type))

        moment.folder = 'Momentos'
        moment.type = moment_type #MomentType.objects.get(name=moment_type)

        #if h5p_url is not None and h5p_url is not '':
         #   moment.h5p_package = H5Package.objects.get(job_id=h5p_url)
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
