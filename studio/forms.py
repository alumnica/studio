from django import forms
from django.contrib.auth.models import User

from alumnica_entities.users import UserType
from studio.models.users import UserModel


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['username', 'email' ,'password']


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserModel
        fields=['last_name_field']

