"""Модуль аутентификации для набора моделей."""

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Главная модель пользователя проекта, доступная для расширения."""
