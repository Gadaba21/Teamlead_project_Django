from django.core.exceptions import ValidationError
from django.utils import timezone

from api.constanst import MIN_YEAR


def validate_year(year):
    now = timezone.now().year
    if year > now or year <= MIN_YEAR:
        raise ValidationError(
            f'{year} не может быть больше {now} или меньше {MIN_YEAR}'
        )
    