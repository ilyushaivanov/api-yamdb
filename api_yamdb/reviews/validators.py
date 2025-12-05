from django.core.exceptions import ValidationError
from django.utils import timezone

FORBIDDEN_USERNAME = ('me',)


def validate_username(value):
    """
    Валидатор проверят имя пользователя:
        Не являет ли имя пользователя - me
        и проверяет на неподходящие символы
    """
    if value.lower() in FORBIDDEN_USERNAME:
        raise ValidationError("Неподходящее имя пользователя")


def validate_year(value):
    now = timezone.now().year
    if value > now:
        raise ValidationError(
            f'{value} не может быть больше {now}'
        )
