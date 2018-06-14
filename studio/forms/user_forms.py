from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError

from alumnica_model.models import AuthUser, users
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _


class UserLoginForm(forms.Form):
    email = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super(UserLoginForm, self).clean()
        email = cleaned_data.get('email').lower()
        password = cleaned_data.get('password')
        try:
            user = AuthUser.objects.get(email=email)
            if not user.check_password(password):
                error = ValidationError(_("Invalid password or email."), code='credentials_error')
                self.add_error('password', error)
                self.add_error('email', error)

            if not user.user_type == users.TYPE_CONTENT_CREATOR:
                if not user.user_type == users.TYPE_SUPERVISOR:
                    error = ValidationError(_("Invalid credentials"), code='permission denied')
                    self.add_error('password', error)
                    self.add_error('email', error)

        except AuthUser.DoesNotExist:
            error = ValidationError(_("Invalid password or email."), code='credentials_error')
            self.add_error('password', error)
            self.add_error('email', error)
        return cleaned_data

    def get_user(self):
        cleaned_data = super(UserLoginForm, self).clean()
        email = cleaned_data.get('email').lower()
        user = AuthUser.objects.get(email=email)
        return user


class AuthUserCreateForm(forms.ModelForm):
    class Meta:
        model = AuthUser
        fields = ['email']

    def save(self, commit=True):
        user = super(AuthUserCreateForm, self).save(commit=False)
        user.email = user.email.lower()
        user.set_password(self.cleaned_data.get('password'))
        if commit:
            user.save()
        return user


class CustomUserAdmin(UserAdmin):
    # The forms to add and change user instances
    add_form = AuthUserCreateForm
    list_display = ("email",)
    ordering = ("email",)

    fieldsets = (
        (None, {'fields': ('email', 'password', 'first_name', 'last_name')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'first_name', 'last_name', 'is_superuser', 'is_staff', 'is_active',
                       'user_type')}
         ),
    )

    filter_horizontal = ()


admin.site.unregister(AuthUser)
admin.site.register(AuthUser, CustomUserAdmin)
