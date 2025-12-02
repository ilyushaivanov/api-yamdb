from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

regex_validator = RegexValidator(
    regex=r'^[\w.@+-]+\Z',
    message='Username может содержать только буквы, цифры и символы @/./+/-/_'
)


def username_validator(value):
    """
    Валидатор проверят имя пользователя:
        Не являет ли имя пользователя - me
        и проверяет на неподходящие символы
    """
    if value.lower() == 'me':
        raise ValidationError("Неподходящее имя пользователя")
    regex_validator(value)