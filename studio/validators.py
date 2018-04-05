from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def unique_ambit_name_validator(value):
    from alumnica_model.models import AmbitModel
    if AmbitModel.objects.filter(name_field__iexact=value).exists():
        raise ValidationError(_('An Ambit with the name "{}", already exists'.format(value)), code='non_unique_field')
