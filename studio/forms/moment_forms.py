from django import forms

from alumnica_model.models import Moment, Tag
from alumnica_model.models.content import MomentType, Subject, MicroODAType, Content, answerCorrect
#from alumnica_model.models.h5p import H5Package


class ContentForm(forms.ModelForm):
    url_h5p = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'id': 'url_h5p'}))
    library_h5p = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'id': 'library_h5p'}))
    text = forms.CharField(max_length=1000, widget=forms.Textarea(attrs={'id': 'text_free'}))
    
    question = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'id': 'question'}))
    answer1 = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'id': 'answer1'}))
    answer2 = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'id': 'answer2'}))
    answer3 = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'id': 'answer3'}))
    correct_answer = forms.ChoiceField(widget=forms.Select(attrs={'id': 'correct_answer'}))
    positive_retro = forms.CharField(max_length=350, widget=forms.TextInput(attrs={'id': 'positive_retro'}))
    negative_retro = forms.CharField(max_length=350, widget=forms.TextInput(attrs={'id': 'negative_retro'}))

    coordenada1 = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'id': 'coordenada1'}))
    coordenada2 = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'id': 'coordenada2'}))
    coordenada3 = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'id': 'coordenada3'}))
    coordenada4 = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'id': 'coordenada4'}))

    content = forms.FileField(required=False,
                              widget=forms.FileInput(attrs={'class': 'show-for-sr', 'id': 'content'}))

    class Meta:
        model = Content
        fields = ['url_h5p', 'library_h5p', 'content', 'text', 'question', 'answer1', 'answer2', 'answer3', 'correct_answer',
                'positive_retro', 'negative_retro', 'coordenada1', 'coordenada2', 'coordenada3', 'coordenada4']

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

        cleaned_data = super(MomentCreateForm, self).clean()
        moment = super(MomentCreateForm, self).save(commit=False)
        tags = cleaned_data.get('tags').split(',')
        subject = Subject.objects.get(name=subject_name)
        oda = subject.odas.get(name=oda_name)
        microoda = oda.microodas.get(type=MicroODAType.objects.get(name=microoda_type))

        moment.folder = 'Momentos'
        moment.created_by = user
        moment.type = moment_type 
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

    def save_form(self, user, subject_name, oda_name, microoda_type, moment_type, content_id):
        cleaned_data = super(MomentUpdateForm, self).clean()
        moment = super(MomentUpdateForm, self).save(commit=False)
        tags = cleaned_data.get('tags').split(',')
        subject = Subject.objects.get(name=subject_name)
        oda = subject.odas.get(name=oda_name)
        microoda = oda.microodas.get(type=MicroODAType.objects.get(name=microoda_type))

        moment.folder = 'Momentos'
        moment.update_by = user
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
