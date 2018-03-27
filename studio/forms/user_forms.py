from django import forms
from django.core.exceptions import ValidationError

from alumnica_model.alumnica_entities.users import UserType
from alumnica_model.models import AuthUser


class UserLoginForm(forms.Form):
    email = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super(UserLoginForm, self).clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        try:
            user = AuthUser.objects.get(email=email)
            if not user.check_password(password):
                error = ValidationError("Invalid password or email.", code='credentials_error')
                self.add_error('password', error)
                self.add_error('email', error)

            if not user.user_type == UserType.CONTENT_CREATOR:
                if not user.is_staff:
                    error = ValidationError("Invalid credentials", code='permission denied')
                    self.add_error('password', error)
                    self.add_error('email', error)

        except AuthUser.DoesNotExist:
            error = ValidationError("Invalid password or email.", code='credentials_error')
            self.add_error('password', error)
            self.add_error('email', error)
        return cleaned_data

    def get_user(self):
        cleaned_data = super(UserLoginForm, self).clean()
        email = cleaned_data.get('email')
        user = AuthUser.objects.get(email=email)
        return user




