from django.contrib.auth.models import AbstractUser
from django.db.models import (CASCADE, CharField, DateField, ForeignKey, Model,
                              TextChoices, TextField)


class User(AbstractUser):
    """Пользователь системы."""


def _limit_end_date_choices() -> dict:
    return {'end_date__isnull': True}


def _limit_is_active_choices() -> dict:
    return {'is_active': True}


class Question(Model):
    class Type(TextChoices):
        TEXT_ANSWER = 'TA', 'Ответ с текстом'
        SINGLE_ANSWER = 'SA', 'Ответ с выбором одного варианта'
        MULTIPLE_CHOICE = 'MC', 'Ответ с выбором нескольких вариантов'

    text = CharField(max_length=254, verbose_name='Текст')
    type = CharField(max_length=2, choices=Type.choices, verbose_name='Тип')
    poll = ForeignKey('Poll', CASCADE,
                      limit_choices_to=_limit_end_date_choices,
                      verbose_name='Опрос')

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Answer(Model):
    user = ForeignKey(User, CASCADE, limit_choices_to=_limit_is_active_choices,
                      verbose_name='Пользователь')
    question = ForeignKey(Question, CASCADE, verbose_name='Вопрос')
    text = TextField(verbose_name='Текст отввета')

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'


class Poll(Model):
    name = CharField(max_length=254, verbose_name='Название')
    start_date = DateField(verbose_name='Дата начала')
    end_date = DateField(null=True, blank=True, verbose_name='Дата окончания')
    description = TextField(blank=True, default='', verbose_name='Описание')

    class Meta:
        verbose_name = 'Опрос'
        verbose_name_plural = 'Опросы'
