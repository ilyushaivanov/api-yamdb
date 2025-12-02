from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils import timezone

regex_validator = RegexValidator(
    regex=r'^[\w.@+-]+\Z',
    message='Username может содержать только буквы, цифры и символы @/./+/-/_'
)


def validate_username(value):
    """
    Валидатор проверят имя пользователя:
        Не являет ли имя пользователя - me
        и проверяет на неподходящие символы
    """
    if value.lower() == 'me':
        raise ValidationError("Неподходящее имя пользователя")
    regex_validator(value)


def validate_year(value):
    now = timezone.now().year
    if value > now:
        raise ValidationError(
            f'{value} не может быть больше {now}'
        )
