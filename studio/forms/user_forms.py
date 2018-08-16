import csv

from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.utils.encoding import smart_str
from django.utils.translation import gettext_lazy as _

from alumnica_model.models import AuthUser, users
from alumnica_model.models.users import TYPE_CONTENT_CREATOR, TYPE_SUPERVISOR, ContentCreator, Supervisor, Learner


class UserLoginForm(forms.Form):
    """
    Contains email and password field to identify an AuthUser object
    """
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


class CreateUserForm(forms.ModelForm):
    """
    Create new AuthUser object form
    """
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = AuthUser
        fields = ['email', 'password', 'first_name', 'last_name', 'user_type']

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.fields['user_type'].choices = ((TYPE_CONTENT_CREATOR, _(TYPE_CONTENT_CREATOR)),
                                            (TYPE_SUPERVISOR, _(TYPE_SUPERVISOR)))

    def clean(self):
        cleaned_data = super(CreateUserForm, self).clean()
        email = cleaned_data.get('email')
        if AuthUser.objects.filter(email=email).exists():
            error = ValidationError(_("User with email already exists."), code='email_error')
            self.add_error('email', error)
            return cleaned_data
        return cleaned_data

    def save(self, commit=True):
        user = super(CreateUserForm, self).save(commit=False)
        user.email = user.email.lower()
        user.set_password(self.cleaned_data.get('password'))
        if commit:
            user.save()
        return user


class UpdateUserForm(forms.ModelForm):
    """
    Update existing AuthUser object form
    """
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = AuthUser
        fields = ['email', 'password', 'first_name', 'last_name', 'user_type']

    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)
        self.fields['user_type'].choices = ((TYPE_CONTENT_CREATOR, _(TYPE_CONTENT_CREATOR)),
                                            (TYPE_SUPERVISOR, _(TYPE_SUPERVISOR)))

    def clean(self):
        cleaned_data = super(UpdateUserForm, self).clean()
        user = super(UpdateUserForm, self).save(commit=False)
        email = cleaned_data.get('email')
        if AuthUser.objects.filter(email=email).exists() and AuthUser.objects.get(email=email) != user:
            error = ValidationError(_("User with email already exists."), code='email_error')
            self.add_error('email', error)
            return cleaned_data
        return cleaned_data

    def save(self, commit=True):
        user = super(UpdateUserForm, self).save(commit=False)
        user_original = AuthUser.objects.get(pk=user.pk)
        user.email = user.email.lower()
        new_password = self.cleaned_data.get('password')
        if new_password is not None:
            user.set_password(self.cleaned_data.get('password'))
        if commit:
            if user.user_type != user_original.user_type:
                user_original.profile.delete()
                if user.user_type == TYPE_CONTENT_CREATOR:
                    obj = ContentCreator.objects.create(auth_user=user_original)
                elif user.user_type == TYPE_SUPERVISOR:
                    obj = Supervisor.objects.create(auth_user=user_original)
            user.save()
        return user


class AuthUserCreateForm(forms.ModelForm):
    """
    Creates a new AuthUser object via Django administrator
    """
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
    """
    Adds fields to AuthUserCreateForm in Django administrator
    """
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


def DownloadLearnerUsers(modeladmin, request, queryset):
    """
Creates CSV file containing query objects
    :param queryset: Objects set
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=learners.csv'
    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8'))  # BOM (optional...Excel needs it to open UTF-8 file properly)
    writer.writerow([
        smart_str(u"Name"),
        smart_str(u"Email"),
        smart_str(u"Birthday"),
        smart_str(u"Learning Style"),
    ])
    for obj in queryset:
        writer.writerow([
            smart_str('{} {}'.format(obj.auth_user.first_name, obj.auth_user.last_name)),
            smart_str(obj.auth_user.email),
            smart_str(obj.birth_date),
            smart_str(obj.learning_style),
        ])
    return response


DownloadLearnerUsers.short_description = u"Export CSV"


class DownloadLearnerFile(admin.ModelAdmin):
    """
    Adds Export CSV action to Learner model view in Django administrator
    """
    actions = [DownloadLearnerUsers]


admin.site.unregister(AuthUser)
admin.site.unregister(Learner)
admin.site.register(Learner, DownloadLearnerFile)
admin.site.register(AuthUser, CustomUserAdmin)
