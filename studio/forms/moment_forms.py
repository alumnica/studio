from django import forms

from alumnica_model.models import Moment


class MomentCreateForm(forms.ModelForm):
    tags = forms.CharField(widget=forms.TextInput(attrs={'id':'momento-tags',
                                                         'class':'u-margin-bottom-small selectized'}))
    content = forms.FileField(widget=forms.FileInput(attrs={'class': 'show-for-sr', 'id': 'h5p-upload'}))

    class Meta:
        model = Moment
        fields = [ 'tags', 'content']