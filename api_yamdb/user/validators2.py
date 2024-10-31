import re
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


class CustomUsernameValidator(RegexValidator):
    regex = r'^[\w.@+-]+\Z'
    message = _(
        'Введите корректное имя пользователя. Допустимы только латинские буквы, '
        'цифры и символы @/./+/-/_'
    )
    flags = 0

    def __call__(self, value):
        super().__call__(value)
        if value == "me":
            raise ValidationError('Имя пользователя "me" использовать нельзя!')







# from django.contrib.auth.validators import ASCIIUsernameValidator
# from django.core.exceptions import ValidationError


# class CustomUsernameValidator(ASCIIUsernameValidator):
#     def __call__(self, value):
#         # Проверяем сначала на запрещенные символы с помощью регулярного выражения
#         super().__call__(value)

#         # Добавляем проверку на имя "me"
#         if value == "me":
#             raise ValidationError('Имя пользователя "me" использовать нельзя!')