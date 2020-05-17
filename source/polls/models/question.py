"""Набор моделей для вопроса."""
from django.db.models import (CASCADE, CharField, ForeignKey, Model,
                              TextChoices, TextField)


class Question(Model):
    """Вопрос."""

    class TypeChoices(TextChoices):
        """Набор типов вопроса."""

        TEXT_ANSWER = ('TEXT_ANSWER', 'Ответ с текстом')
        SINGLE_ANSWER = ('SINGLE_ANSWER', 'Ответ с выбором одного варианта')
        SEVERAL_OPTIONS_ANSWER = ('SEVERAL_OPTIONS_ANSWER',
                                  'Ответ с выбором нескольких вариантов')

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    text = CharField(max_length=254, verbose_name='Текст')
    type = CharField(max_length=22, choices=TypeChoices.choices,
                     verbose_name='Тип')
    poll = ForeignKey('Poll', CASCADE, verbose_name='Опрос')

    def __str__(self) -> str:
        """Строковое представление вопроса."""
        return f'{self.type}: {self.text}'


class AnswerOption(Model):
    """Вариант ответа к вопросу."""

    class Meta:
        verbose_name = 'Вариант ответа'
        verbose_name_plural = 'Варианты ответа'

    question = ForeignKey('Question', CASCADE, verbose_name='Тип вопроса')
    content = TextField(verbose_name='Вариант ответа')

    def __str__(self) -> str:
        """Строковое представление варианта ответа."""
        return self.content
