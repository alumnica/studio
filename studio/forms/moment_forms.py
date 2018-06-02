from django import forms

from alumnica_model.models import Moment


class MomentCreateForm(forms.ModelForm):
    tags = forms.CharField(widget=forms.TextInput(attrs={'id':'momento-tags',
                                                         'class':'u-margin-bottom-small selectized'}))

    class Meta:
        model = Moment
        fields = ['name', 'tags', 'content']