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

# user.validators.py:

# import re
# from django.core.exceptions import ValidationError
# from django.core import validators
# from django.utils.translation import gettext_lazy as _

# class CustomUsernameValidator(validators.RegexValidator):
#     regex = r'^[\w.@+-]+\Z'
#     message = _(
#         'Введите корректное имя пользователя. Допустимы только латинские буквы, '
#         'цифры и символы @/./+/-/_'
#     )
#     flags = re.ASCII  # Установите на 0 для поддержки юникода
    
#     def __call__(self, value):
#         # Проверяем сначала на запрещенные символы с помощью регулярного выражения
#         super().__call__(value)
        
#         # Добавляем проверку на имя "me"
#         if value == "me":
#             raise ValidationError('Имя пользователя "me" использовать нельзя!')

# Пример использования валидатора в модели
# from django.db import models

# class User(models.Model):
#     username = models.CharField(
#         max_length=150,
#         unique=True,
#         validators=[CustomUsernameValidator()],
#     )
