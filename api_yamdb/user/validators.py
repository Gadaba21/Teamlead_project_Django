from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

from api.constanst import RESOLVED_NAME_MSG


def validate_username(value):
    if value.lower() == 'me':
        raise ValidationError('Имя пользователя \'me\' использовать нельзя!')

    regex_validator = RegexValidator(
        regex=r'^[\w.@+-]+\Z',
        message=_(RESOLVED_NAME_MSG)
    )
    regex_validator(value)
    return value
