import csv
import os

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.dateparse import parse_datetime

from reviews.models import User, Category, Genre, Title, Review, Comment


class Command(BaseCommand):
    help = 'Импорт данных из CSV файлов'

    def add_arguments(self, parser):
        parser.add_argument(
            '--data-path',
            default='static/data',
            help='Путь к папке с CSV файлами'
        )
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Подробный вывод'
        )

    @transaction.atomic
    def handle(self, *args, **options):
        data_path = options['data_path']
        verbose = options['verbose']

        import_steps = [
            ('users.csv', self.import_users),
            ('category.csv', self.import_categories),
            ('genre.csv', self.import_genres),
            ('titles.csv', self.import_titles),
            ('genre_title.csv', self.import_genre_title_relations),
            ('review.csv', self.import_reviews),
            ('comments.csv', self.import_comments),
        ]

        for filename, import_func in import_steps:
            filepath = os.path.join(data_path, filename)

            if not os.path.exists(filepath):
                self.stdout.write(
                    self.style.WARNING(f'{filename} не найден, пропускаем'))
                continue

            self.stdout.write(f'Импорт {filename}...')
            try:
                import_func(filepath, verbose)
                self.stdout.write(self.style.SUCCESS(
                    f'{filename} успешно импортирован'))
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Ошибка импорта {filename}: {e}'))
                raise

    def import_users(self, filepath, verbose):
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    user_data = {
                        'id': int(row['id']),
                        'username': row['username'],
                        'email': row['email'],
                        'role': row.get('role', 'user'),
                        'bio': row.get('bio', ''),
                        'first_name': row.get('first_name', ''),
                        'last_name': row.get('last_name', ''),
                    }
                    User.objects.get_or_create(
                        id=user_data['id'], defaults=user_data)
                except Exception as e:
                    if verbose:
                        self.stdout.write(f'Ошибка в строке пользователя: {e}')

    def import_categories(self, filepath, verbose):
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    Category.objects.get_or_create(
                        id=int(row['id']),
                        defaults={
                            'name': row['name'],
                            'slug': row['slug']
                        }
                    )
                except Exception as e:
                    if verbose:
                        self.stdout.write(f'Ошибка в строке категории: {e}')

    def import_genres(self, filepath, verbose):
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    Genre.objects.get_or_create(
                        id=int(row['id']),
                        defaults={
                            'name': row['name'],
                            'slug': row['slug']
                        }
                    )
                except Exception as e:
                    if verbose:
                        self.stdout.write(f'Ошибка в строке жанра: {e}')

    def import_titles(self, filepath, verbose):
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    year = int(row['year']) if row['year'] else None

                    category_id = int(
                        row['category']) if row['category'] else None
                    category = Category.objects.get(
                        id=category_id) if category_id else None

                    Title.objects.get_or_create(
                        id=int(row['id']),
                        defaults={
                            'name': row['name'],
                            'year': year,
                            'description': row.get('description', ''),
                            'category': category
                        }
                    )
                except Exception as e:
                    if verbose:
                        self.stdout.write(f'Ошибка в строке произведения: {e}')

    def import_genre_title_relations(self, filepath, verbose):
        """Импорт связей ManyToMany между Title и Genre"""
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    title_id = int(row['title_id'])
                    genre_id = int(row['genre_id'])

                    title = Title.objects.get(id=title_id)
                    genre = Genre.objects.get(id=genre_id)

                    title.genre.add(genre)
                except Exception as e:
                    if verbose:
                        self.stdout.write(
                            f'Ошибка в строке связи жанр-произведение: {e}'
                        )

    def import_reviews(self, filepath, verbose):
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    title_id = int(row['title_id'])
                    author_id = int(row['author'])

                    title = Title.objects.get(id=title_id)
                    author = User.objects.get(id=author_id)

                    pub_date = parse_datetime(
                        row['pub_date']) if row.get('pub_date') else None

                    Review.objects.get_or_create(
                        id=int(row['id']),
                        defaults={
                            'title': title,
                            'text': row['text'],
                            'author': author,
                            'score': int(row['score']),
                            'pub_date': pub_date
                        }
                    )
                except Exception as e:
                    if verbose:
                        self.stdout.write(f'Ошибка в строке отзыва: {e}')

    def import_comments(self, filepath, verbose):
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    review_id = int(row['review_id'])
                    author_id = int(row['author'])

                    review = Review.objects.get(id=review_id)
                    author = User.objects.get(id=author_id)

                    pub_date = parse_datetime(
                        row['pub_date']) if row.get('pub_date') else None

                    Comment.objects.get_or_create(
                        id=int(row['id']),
                        defaults={
                            'review': review,
                            'text': row['text'],
                            'author': author,
                            'pub_date': pub_date
                        }
                    )
                except Exception as e:
                    if verbose:
                        self.stdout.write(
                            f'Ошибка в строке комментария: {e}'
                        )
