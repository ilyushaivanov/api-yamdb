import csv
import os
from django.core.management.base import BaseCommand
from reviews.models import User, Category, Genre, Title, Review, Comment


class Command(BaseCommand):
    help = 'Базовый импорт CSV'

    def handle(self, *args, **options):
        data_path = 'static/data'
        files = [
            ('users.csv', User),
            ('category.csv', Category),
            ('genre.csv', Genre),
            ('titles.csv', Title),
            ('review.csv', Review),
            ('comments.csv', Comment),
        ]

        for filename, model in files:
            self.import_model(data_path, filename, model)

        self.import_relations(data_path)

    def import_model(self, path, filename, model):
        filepath = os.path.join(path, filename)

        if not os.path.exists(filepath):
            print(f'{filename} не найден')
            return

        count = 0
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    model.objects.create(**row)
                    count += 1
                except Exception:
                    continue

        print(f'{model.__name__}: {count} записей')

    def import_relations(self, path):
        filepath = os.path.join(path, 'genre_title.csv')

        if not os.path.exists(filepath):
            print('genre_title.csv не найден')
            return

        count = 0
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    title = Title.objects.get(id=int(row['title_id']))
                    genre = Genre.objects.get(id=int(row['genre_id']))
                    title.genre.add(genre)
                    count += 1
                except Exception:
                    continue

        print(f'Genre-Title связей: {count}')
