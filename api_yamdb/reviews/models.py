from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import validate_username, validate_year
from .constants import (
    max_length_username,
    max_length_role, max_length_first_name,
    max_length_last_name, max_length_confirmation_code,
    max_length_name_Category, max_length_name_Genre,
    max_length_name_Title, max_length_description_Title,
    max_length_text_Review, max_length_text_Comment,
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
        max_length=max_length_username,
        unique=True,
    )
    email = models.EmailField(
        unique=True,
    )
    role = models.CharField(
        'роль',
        max_length=max_length_role,
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
        max_length=max_length_first_name,
        blank=True
    )
    last_name = models.CharField(
        'фамилия',
        max_length=max_length_last_name,
        blank=True
    )

    @property
    def is_user(self):
        return self.role == UserRole.USER

    @property
    def is_admin(self):
        return self.role == UserRole.ADMIN

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
        max_length=max_length_name_Category
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
        max_length=max_length_name_Genre
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
        max_length=max_length_name_Title,
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
        max_length=max_length_description_Title,
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
        max_length=max_length_text_Review
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='автор'
    )
    score = models.IntegerField(
        'оценка',
        validators=(
            MinValueValidator(1),
            MaxValueValidator(10)
        ),
        error_messages={'validators': 'Оценка от 1 до 10!'}
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
        return f'Отзыв {self.id} от {self.author.username} на {
            self.title.name}'


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='отзыв'
    )
    text = models.CharField(
        'текст комментария',
        max_length=max_length_text_Comment
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
