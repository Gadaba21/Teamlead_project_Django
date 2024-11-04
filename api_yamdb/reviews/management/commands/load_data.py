import csv

from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from api_yamdb.settings import BASE_DIR

from reviews.models import (Category, Comment, Genre, TitleGenre, Review,
                            Title, User)
from reviews.models import User


MODELS_FILENAME = {
    User: 'users.csv',
    Category: 'category.csv',
    Genre: 'genre.csv',
    Title: 'titles.csv',
    TitleGenre: 'genre_title.csv',
    Review: 'review.csv',
    Comment: 'comments.csv',
}


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        for model, file_name in MODELS_FILENAME.items():
            file_path = f'{BASE_DIR}/static/data/{file_name}'
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    reader = csv.DictReader(file)
                    model.objects.bulk_create(
                        model(**data) for data in reader
                    )
                    self.stdout.write(self.style.SUCCESS(
                        f'Файл: {file_name} загружен успешно')
                    )
            except IntegrityError:
                pass
            except FileNotFoundError:
                self.stderr.write(self.style.ERROR(
                    f'файл: {file_name} не найден')
                )
