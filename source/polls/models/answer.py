"""Модуль с моделью ответа на вопрос."""
from django.db.models import (CASCADE, ForeignKey, ManyToManyField, Model,
                              TextField)


class Answer(Model):
    """Ответ на вопрос."""
    class Meta:
        verbose_name = 'Ответ на вопрос'
        verbose_name_plural = 'Ответы на вопрос'

    user = ForeignKey('User', CASCADE, verbose_name='Участник опроса')
    question = ForeignKey('Question', CASCADE, verbose_name='Вопрос')
    choices = ManyToManyField('AnswerOption', blank=True,
                              verbose_name='Выбранные ответы')
    text = TextField(blank=True, default='', verbose_name='Текст ответа')
