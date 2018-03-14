from django import forms

from alumnica_model.models import AuthUser, LearnerModel, DataAnalystModel, ContentCreatorModel, AdministratorModel

class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password=forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = AuthUser
        fields = ['username','password']

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

    def __init__(self, *args, **kwargs):
        super(LearnerForm, self).__init__(*args, **kwargs)
        self.fields['experience_points_field'].required = False

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
