from django import forms

from alumnica_model.models import AuthUser, LearnerModel, DataAnalystModel, ContentCreatorModel, AdministratorModel


class UserForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = AuthUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2','user_type']


class LearnerForm(forms.ModelForm):
    class Meta:
        model = LearnerModel
        fields = ['experience_points_field']

class DataAnalystForm(forms.ModelForm):
    class Meta:
        model = DataAnalystModel
        exclude = ['auth_user_field']

class ContentCreatorForm(forms.ModelForm):
    class Meta:
        model = ContentCreatorModel
        exclude = ['auth_user_field']

class AdministratorForm(forms.ModelForm):
    class Meta:
        model = AdministratorModel
        exclude = ['auth_user_field']
