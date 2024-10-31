from django.db import models
from user.models import User
from api.constanst import (LENGTH_TEXT, MAX_LENGTH, MAX_SLAG)
from .validators import validate_year, validate_slag, validate_score


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
        validators=(validate_slag,)
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
        validators=(validate_slag,)
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
    year = models.IntegerField(
        validators=(validate_year, ),
        verbose_name='Год'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Review(models.Model):
    """Класс отзывов."""
    text = models.TextField(verbose_name='текст')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='review',
        verbose_name='Автор'
    )
    score = models.PositiveIntegerField(
        verbose_name='Оценка',
        validators=(validate_score,)
    )
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='review',
        verbose_name='Произведение'
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date',)
        constraints = [
            models.UniqueConstraint(fields=('author', 'title'),
                                    name='author_title')
        ]

    def __str__(self):
        return self.text[:LENGTH_TEXT]


class Comment(models.Model):
    """Класс комментариев."""
    text = models.TextField(verbose_name='текст')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='отзыв'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:LENGTH_TEXT]
