from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


class UsernameValidator(RegexValidator):
    regex = r'^[\w.@+-]+\Z'
    message = _(
        'Введите корректное имя пользователя. '
        'Допустимы только латинские буквы, цифры и символы @/./+/-/_'
    )
    flags = 0

    def __call__(self, value):
        super().__call__(value)

        if value == "me":
            raise ValidationError('Имя пользователя "me" использовать нельзя!')
