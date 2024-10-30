import re

from django.core.exceptions import ValidationError


def valid_username(name):
    forbidden_name = re.sub(r'[\w.@+-]', '', 'me')
    if name in forbidden_name:
        raise ValidationError(
            f'Имя пользователя не может быть "me", '
            f'содержать символы: {forbidden_name} или быть пустым!'
        )
    return name
