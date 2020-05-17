"""Модуль с моделью опроса."""

from django.db.models import CharField, DateField, Model, TextField


class Poll(Model):
    """Опрос с набором вопросов."""

    class Meta:
        verbose_name = 'Опрос'
        verbose_name_plural = 'Опросы'

    name = CharField(max_length=254, verbose_name='Название')
    start_date = DateField(verbose_name='Дата начала')
    end_date = DateField(null=True, blank=True, verbose_name='Дата окончания')
    description = TextField(blank=True, default='', verbose_name='Описание')

    def __str__(self) -> str:
        """Строковое представление опроса."""
        return f'{self.name} ({self.start_date} - {self.end_date})'
