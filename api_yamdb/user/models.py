from django.contrib.auth.models import AbstractUser
from django.db import models

from api.constants import (
    MAX_EMAIL_FIELD, MAX_NAME_FIELD,
    LENGTH_TEXT, HELP_TEXT_NAME
)
from .validators import UsernameValidator, validate_username


class User(AbstractUser):
    """
    Расширенная стандартная Django модель User -
    добавлены поля биография и роль пользователя.
    """

    class Role(models.TextChoices):
        USER = 'user', 'Пользователь'
        MODERATOR = 'moderator', 'Модератор'
        ADMIN = 'admin', 'Администратор'

    username = models.CharField(
        max_length=MAX_NAME_FIELD,
        unique=True,
        verbose_name='Имя пользователя',
        help_text=HELP_TEXT_NAME,
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
        help_text='Заполните Имя',
        default='Пусто'
    )
    last_name = models.CharField(
        max_length=MAX_NAME_FIELD,
        blank=True,
        null=True,
        verbose_name='Фамилия',
        help_text='Заполните Фамилию',
        default='Пусто'
    )
    email = models.EmailField(
        max_length=MAX_EMAIL_FIELD,
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
        help_text='Заполните информацию о себе',
        default='Пусто'
    )
    role = models.CharField(
        max_length=max(len(role) for role, _ in Role.choices),
        choices=Role.choices,
        default=Role.USER,
        verbose_name='Роль пользователя',
        help_text='Уровень доступа пользователя'
    )

    @property
    def is_admin(self):
        return (
            self.role == self.Role.ADMIN
            or self.is_superuser
            or self.is_staff
        )

    @property
    def is_moderator(self):
        return self.role == self.Role.MODERATOR

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id', 'username',)

    def __str__(self):
        return self.username[:LENGTH_TEXT]
