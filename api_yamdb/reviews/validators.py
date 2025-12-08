from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_username(value):
    """
    Валидатор проверят имя пользователя:
        Не являет ли имя пользователя - me
        и проверяет на неподходящие символы
    """
    if value.lower() in settings.FORBIDDEN_USERNAMES:
        raise ValidationError(
            f'Имя пользователя "{value}" запрещено. Выберите другое имя.'
        )


def validate_year(value):
    """
    Валидатор для проверки года выпуска произведения.
    Проверяет, что год не превышает текущий год.
    """
    now = timezone.now().year
    if value > now:
        raise ValidationError(
            f'{value} не может быть больше {now}'
        )
