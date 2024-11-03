from django.contrib.auth.models import AbstractUser
from django.db import models

from api.constanst import (
    MAX_EMAIL_FIELD, MAX_NAME_FIELD, LENGTH_TEXT, MAX_VALUE, HELP_TEXT_NAME
)
from user.validators import UsernameValidator, validate_username


class User(AbstractUser):
    """
    Расширенная стандартная Django модель User -
    добавлены поля биография и роль пользователя.
    """

    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLES = (
        (USER, 'Пользователь'),
        (ADMIN, 'Администратор'),
        (MODERATOR, 'Модератор')
    )

    username = models.CharField(
        max_length=MAX_NAME_FIELD,
        unique=True,
        verbose_name='Имя пользователя',
        help_text=(HELP_TEXT_NAME),
        validators=(UsernameValidator(), validate_username,),
        error_messages={
            'unique': 'Пользователь с таким именем уже существует!',
        },
    )
    first_name = models.CharField(
        max_length=MAX_NAME_FIELD,
        blank=True,
        null=True,
        verbose_name='Имя',
        help_text='Заполните Имя'
    )
    last_name = models.CharField(
        max_length=MAX_NAME_FIELD,
        blank=True,
        null=True,
        verbose_name='Фамилия',
        help_text='Заполните Фамилию'
    )
    email = models.EmailField(
        max_length=MAX_EMAIL_FIELD,
        blank=True,
        unique=True,
        verbose_name='Электронная почта',
        help_text='Введите свой email',
        error_messages={
            'unique': 'Пользователь с таким email уже существует!',
        },
    )
    bio = models.TextField(
        blank=True,
        null=True,
        verbose_name='Биография',
        help_text='Заполните информацию о себе'
    )
    role = models.CharField(
        max_length=LENGTH_TEXT,
        choices=ROLES,
        default=USER,
        verbose_name='Роль пользователя',
        help_text='Уровень доступа пользователя'
    )
    confirmation_code = models.CharField(
        max_length=MAX_VALUE,
        null=True,
        blank=True,
        verbose_name="Код потдверждения",
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id', 'username',)

    def __str__(self):
        return self.username[:LENGTH_TEXT]
