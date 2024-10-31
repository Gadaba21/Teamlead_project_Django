from django.core.exceptions import ValidationError
from django.utils import timezone
from django.core.validators import (MinValueValidator,
                                    MaxValueValidator,
                                    RegexValidator)
from api.constanst import MIN_YEAR, MIN_VALUE, MAX_VALUE


def validate_year(year):
    now = timezone.now().year
    if year > now or year <= MIN_YEAR:
        raise ValidationError(
            f'{year} не может быть больше {now} или меньше {MIN_YEAR}'
        )


def validate_slag():
    return RegexValidator(
        regex=r'^[-a-zA-Z0-9_]+$',
        message='Слаг содержит недопустимый символ'
    )


def validate_score():
    return (MinValueValidator(MIN_VALUE), MaxValueValidator(MAX_VALUE))
