# from datetime import date

from django.conf import settings
from django.contrib.auth.validators import UnicodeUsernameValidator
# from django.core.exceptions import ValidationError


class UsernameValidatorRegex(UnicodeUsernameValidator):
    """Валидация имени пользователя и его соответсвие."""

    regex = r"^[\w.@+-]+\Z"
    flag = 0
    max_length = settings.LENG_LOGIN_USER
    message = (
        f"Введите правильное имя пользователя."
        f" Должно содержать буквы, цифры и знаки @/./+/-/_."
        f" Длина не более {settings.LENG_LOGIN_USER} символов"
    )
    error_message = {
        "invalid": f"Набор символов не более {settings.LENG_LOGIN_USER}. "
        "Только буквы, цифры и @/./+/-/_",
        "required": "Поле не может быть пустым и обязательно!",
    }
