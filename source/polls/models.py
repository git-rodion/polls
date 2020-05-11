from django.contrib.auth.models import AbstractUser
from django.db.models import (CASCADE, CharField, DateField, ForeignKey, Model,
                              TextChoices, TextField)


class User(AbstractUser):
    """Пользователь системы."""


class Poll(Model):
    name = CharField(max_length=254, verbose_name='Название')
    start_date = DateField(verbose_name='Дата начала')
    end_date = DateField(null=True, blank=True, verbose_name='Дата окончания')
    description = TextField(blank=True, default='', verbose_name='Описание')

    class Meta:
        verbose_name = 'Опрос'
        verbose_name_plural = 'Опросы'

    def __str__(self):
        return f'{self.name} ({self.start_date} - {self.end_date})'


class Question(Model):
    class TypeChoices(TextChoices):
        TEXT_ANSWER = ('TEXT_ANSWER', 'Ответ с текстом')
        SINGLE_ANSWER = ('SINGLE_ANSWER', 'Ответ с выбором одного варианта')
        MULTIPLE_CHOICE = ('MULTIPLE_CHOICE',
                           'Ответ с выбором нескольких вариантов')

    text = CharField(max_length=254, verbose_name='Текст')
    type = CharField(max_length=15, choices=TypeChoices.choices,
                     verbose_name='Тип')
    poll = ForeignKey(Poll, CASCADE, verbose_name='Опрос')

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self):
        return f'{self.type}: {self.text}'


class ExpectedAnswer(Model):
    question = ForeignKey(Question, CASCADE, verbose_name='Тип вопроса')
    content = TextField(verbose_name='Вариант ответа')

    class Meta:
        verbose_name = 'Ожидаемый вариант ответа'
        verbose_name_plural = 'Ожидаемые варианты ответа'


class AbstractChoiceOfAnswer(Model):
    choice = ForeignKey(ExpectedAnswer, CASCADE, verbose_name='Вариант ответа')

    class Meta:
        abstract = True


class SingleChoiceOfAnswer(AbstractChoiceOfAnswer):
    class Meta:
        verbose_name = 'Одиночный вариант ответа'
        verbose_name_plural = 'Одиночные варианты ответа'


class AbstractAnswer(Model):
    user = ForeignKey(User, CASCADE, verbose_name='Пользователь')
    question = ForeignKey(Question, CASCADE, verbose_name='Вопрос')

    class Meta:
        abstract = True


class TextAnswer(AbstractAnswer):
    text = TextField(verbose_name='Текст ответа')

    class Meta:
        verbose_name = 'Вариант ответа с текстом'
        verbose_name_plural = 'Вариант ответов с текстом'


class SingleChoiceAnswer(AbstractAnswer):
    choice = ForeignKey(SingleChoiceOfAnswer, CASCADE, verbose_name='Ответ')

    class Meta:
        verbose_name = 'Вариант ответа с выбором одного варианта'
        verbose_name_plural = 'Вариант ответов с выбором одного варианта'


class AnswerWithMiltipleChoices(AbstractAnswer):
    class Meta:
        verbose_name = 'Вариант ответа с выбором нескольких вариантов'
        verbose_name_plural = 'Вариант ответов с выбором нескольких вариантов'


class MiltipleChoiceOfAnswer(AbstractChoiceOfAnswer):
    answer = ForeignKey(AnswerWithMiltipleChoices, CASCADE,
                        verbose_name='Ответ')

    class Meta:
        verbose_name = 'Множественный вариант ответа'
        verbose_name_plural = 'Множественные варианты ответа'
