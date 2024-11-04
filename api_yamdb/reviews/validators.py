from django.core.exceptions import ValidationError
from django.utils import timezone
from api.constanst import MIN_YEAR, MIN_VALUE, MAX_VALUE
import re


def validate_year(year):
    now = timezone.now().year
    if year > now or year <= MIN_YEAR:
        raise ValidationError(
            f'{year} не может быть больше {now} или меньше {MIN_YEAR}'
        )


def validate_slug(value):
    slug_regex = r'^[-a-zA-Z0-9_]+$'
    if not re.match(slug_regex, value):
        raise ValidationError('Слаг содержит недопустимый символ.')


def validate_score(value):
    if not (MIN_VALUE <= value <= MAX_VALUE):
        raise ValidationError(f'Оценка должна быть в диапазоне от {MIN_VALUE} до {MAX_VALUE}.')
