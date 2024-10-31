from django.contrib.auth.models import AbstractUser
from django.db import models

from api.constanst import MAX_EMAIL_FIELD, MAX_NAME_FIELD, LENGTH_TEXT
from user.validators import valid_username


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
        verbose_name='Имя пользователя',
        unique=True,
        validators=(valid_username,),
        error_messages={
            'unique': 'Пользователь с таким именем уже существует!',
        },
    )
    first_name = models.CharField(
        max_length=MAX_NAME_FIELD,
        blank=True,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=MAX_NAME_FIELD,
        blank=True,
        verbose_name='Фамилия'
    )
    email = models.EmailField(
        max_length=MAX_EMAIL_FIELD,
        blank=True,
        unique=True,
        verbose_name='Электронная почта',
        help_text='Введите свой email'
    )
    bio = models.TextField(
        blank=True,
        null=True,
        verbose_name='Биография',
        help_text='Заполните информацию о себе'
    )
    role = models.CharField(
        max_length=max(len(role) for role, _ in ROLES),
        choices=ROLES,
        default=USER,
        verbose_name='Роль пользователя',
        help_text='Уровень доступа пользователя'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    def __str__(self):
        return self.username[:LENGTH_TEXT]
