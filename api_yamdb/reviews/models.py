from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from user.models import User
from api.constants import (LENGTH_TEXT, MAX_LENGTH, MAX_SLAG,
                           MIN_VALUE, MAX_VALUE)
from .validators import validate_year, validate_slug


class Category(models.Model):
    '''Класс категорий.'''
    name = models.CharField(
        verbose_name='Категория',
        max_length=MAX_LENGTH
    )
    slug = models.SlugField(
        verbose_name='Слаг категории',
        max_length=MAX_SLAG,
        unique=True,
        validators=(validate_slug,)
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Genre(models.Model):
    '''Класс жанров.'''
    name = models.CharField(
        verbose_name='Жанр',
        max_length=MAX_LENGTH
    )
    slug = models.SlugField(
        verbose_name='Слаг жанра',
        max_length=MAX_SLAG,
        unique=True,
        validators=(validate_slug,)
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Title(models.Model):
    '''Класс произведений.'''
    name = models.TextField(
        verbose_name='Название',
        max_length=MAX_LENGTH
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория',
        blank=True, null=True,
    )
    description = models.TextField(verbose_name='Описание')
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанр',
    )
    year = models.SmallIntegerField(
        validators=(validate_year, ),
        verbose_name='Год'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('name',)

    def __str__(self):
        return self.name


class TitleGenre(models.Model):
    '''Класс произведений-жанров.'''
    title = models.ForeignKey(Title, on_delete=models.CASCADE,)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE,)

    def __str__(self) -> str:
        return f'{self.title},{self.genre}'


class BaseModel(models.Model):
    """Базовая абстрактная модель для контента"""

    text = models.TextField(verbose_name='текст')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='%(app_label)s_%(class)s',
    )
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

    class Meta:
        abstract = True
        ordering = ('-pub_date',)


class Review(BaseModel):
    """Класс отзывов."""
    score = models.SmallIntegerField(
        verbose_name='Оценка',
        validators=[MinValueValidator(MIN_VALUE), MaxValueValidator(MAX_VALUE)]
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='review',
        verbose_name='Произведение'
    )

    class Meta(BaseModel.Meta):
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(fields=('author', 'title'),
                                    name='author_title')
        ]

    def __str__(self):
        return self.text[:LENGTH_TEXT]


class Comment(BaseModel):
    """Класс комментариев."""
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='отзыв'
    )

    class Meta(BaseModel.Meta):
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:LENGTH_TEXT]
