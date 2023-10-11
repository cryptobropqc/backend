from re import search
from django.conf import settings
from django.core.exceptions import ValidationError


def username_validator(username):
    """Валидация для поля 'Логин пользователя' модели User."""
    if username == 'me':
        raise ValidationError(f"You can't use the username me!")

    if not search(r'^[a-zA-Z][a-zA-Z0-9-_\.]{1,150}$', username):
        raise ValidationError(
            f"Invalid characters are used in the User login!")


def first_name_validator(first_name):
    """Валидация для поля 'Имя пользователя' модели User."""
    if not search(r'^[A-Za-zА-Яа-я0-9]{1,150}$', first_name):
        raise ValidationError(
            f"Invalid characters are used in the username!")


def last_name_validator(last_name):
    """Валидация для поля 'Фамилия пользователя' модели User."""
    if not search(r'^[A-Za-zА-Яа-я0-9]{1,150}$', last_name):
        raise ValidationError(
            f"Invalid characters are used in the user's last name")



# class UsernameValidatorRegex(UnicodeUsernameValidator):
#     """Валидация имени пользователя и его соответсвие."""

#     regex = r"^[\w.@+-]+\Z"
#     flag = 0
#     max_length = settings.LENG_LOGIN_USER
#     message = (
#         f"Введите правильное имя пользователя."
#         f" Должно содержать буквы, цифры и знаки @/./+/-/_."
#         f" Длина не более {settings.LENG_LOGIN_USER} символов"
#     )
#     error_message = {
#         "invalid": f"Набор символов не более {settings.LENG_LOGIN_USER}. "
#         "Только буквы, цифры и @/./+/-/_",
#         "required": "Поле не может быть пустым и обязательно!",
#     }