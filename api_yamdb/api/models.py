from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Title(models.Model):
    """Модель произведения (фильм, книга, музыка)."""
    name = models.CharField(max_length=200)
    year = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(
        'Category', on_delete=models.SET_NULL, null=True, blank=True
    )
    genre = models.ManyToManyField('Genre', blank=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    """Отзыв на произведение."""
    title = models.ForeignKey(Title, on_delete=models.CASCADE,
                              related_name='reviews')
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='reviews')
    score = models.IntegerField()  # Рейтинг от 1 до 10
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Один пользователь — один отзыв на произведение
        unique_together = ('title', 'author')

    def __str__(self):
        return f'Review by {self.author} on {self.title}'


class Comment(models.Model):
    """Комментарий к отзыву."""
    review = models.ForeignKey(Review, on_delete=models.CASCADE,
                               related_name='comments')
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='comments')
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author} on review {self.review.id}'
