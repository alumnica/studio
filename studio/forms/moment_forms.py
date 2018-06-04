from django import forms

from alumnica_model.models import Moment, Tag


class MomentCreateForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'id': 'h5p-name'}))
    tags = forms.CharField(widget=forms.TextInput(attrs={'id':'momento-tags',
                                                         'class':'u-margin-bottom-small selectized'}))
    content = forms.FileField(widget=forms.FileInput(attrs={'class': 'show-for-sr', 'id': 'h5p-upload'}))

    class Meta:
        model = Moment
        fields = ['name', 'tags', 'content']

    def save_form(self, user):
        cleaned_data = super(MomentCreateForm, self).clean()
        moment = super(MomentCreateForm, self).save(commit=False)
        tags = cleaned_data.get('tags').split(',')
        moment.folder = 'moments'
        moment.created_by = user
        moment.save()

        for tag_name in tags:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            tag.save()
            moment.tags.add(tag)

        moment.save()