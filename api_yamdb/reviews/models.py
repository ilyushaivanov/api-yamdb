from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import validate_username, validate_year
from .constants import (
    MAX_LENGTH_USERNAME,
    MAX_LENGTH_ROLE, MAX_LENGTH_FIRST_NAME,
    MAX_LENGTH_LAST_NAME,
    MAX_LENGTH_NAME_CATEGORY, MAX_LENGTH_NAME_GENRE,
    MAX_LENGTH_NAME_TITLE,
    MIN_SCORE, MAX_SCORE
)


class UserRole(models.TextChoices):
    USER = 'user', 'Пользователь'
    ADMIN = 'admin', 'Администратор'
    MODERATOR = 'moderator', 'Модератор'
    SUPERUSER = 'superuser', 'Суперюзер'


class User(AbstractUser):
    username = models.CharField(
        validators=(
            validate_username,
            UnicodeUsernameValidator(),
        ),
        max_length=MAX_LENGTH_USERNAME,
        unique=True,
    )
    email = models.EmailField(
        unique=True,
    )
    role = models.CharField(
        'роль',
        max_length=MAX_LENGTH_ROLE,
        choices=UserRole.choices,
        default=UserRole.USER,
        blank=True
    )
    bio = models.TextField(
        'биография',
        blank=True,
    )
    first_name = models.CharField(
        'имя',
        max_length=MAX_LENGTH_FIRST_NAME,
        blank=True
    )
    last_name = models.CharField(
        'фамилия',
        max_length=MAX_LENGTH_LAST_NAME,
        blank=True
    )

    @property
    def is_admin(self):
        return self.role == UserRole.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == UserRole.MODERATOR

    class Meta:
        ordering = ('username', 'email', 'first_name', 'last_name')
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(
        'имя категории',
        max_length=MAX_LENGTH_NAME_CATEGORY
    )
    slug = models.SlugField(
        'слаг категории',
        unique=True,
        db_index=True
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        'имя жанра',
        max_length=MAX_LENGTH_NAME_GENRE
    )
    slug = models.SlugField(
        'слаг жанра',
        unique=True,
        db_index=True
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        'название',
        max_length=MAX_LENGTH_NAME_TITLE,
        db_index=True
    )
    year = models.IntegerField(
        'год',
        validators=(validate_year,)
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='категория',
        null=True,
        blank=True
    )
    description = models.TextField(
        'описание',
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='жанр'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='произведение'
    )
    text = models.CharField(
        'текст отзыва',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='автор'
    )
    score = models.IntegerField(
        'оценка',
        validators=[
            MinValueValidator(
                MIN_SCORE,
                message=f'Оценка не может быть меньше {MIN_SCORE}'
            ),
            MaxValueValidator(
                MAX_SCORE,
                message=f'Оценка не может быть больше {MAX_SCORE}'
            )
        ]
    )
    pub_date = models.DateTimeField(
        'дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author'),
                name='unique_review'
            )
        ]
        ordering = ('pub_date',)

    def __str__(self):
        return (
            f'Отзыв {self.id}'
            f'от {self.author.username} на {self.title.name}'
        )


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='отзыв'
    )
    text = models.CharField(
        'текст комментария',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='автор'
    )
    pub_date = models.DateTimeField(
        'дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ('pub_date',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'Комментарий {self.id} от {self.author.username}'
