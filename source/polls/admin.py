"""Представление моделей в панели администратора."""
from typing import List

from django.contrib import admin
from django.contrib.admin import ModelAdmin, StackedInline
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.http import HttpRequest

from polls.models import AnswerOption, Poll, Question, User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Панель управления пользователями."""


class AnswerOptionInline(StackedInline):
    """Строчное представление вариантов ответа."""

    model = AnswerOption


@admin.register(Question)
class QuestionAdmin(ModelAdmin):
    """Панель управления вопросами."""

    inlines = [AnswerOptionInline]


@admin.register(Poll)
class PollAdmin(ModelAdmin):
    """Панель управления опросами."""

    def get_readonly_fields(self, request: HttpRequest,
                            obj: Poll = None) -> List[str]:
        """
        Определение полей "только для чтения".

        :param request: HTTP запрос.
        :param obj: Объект опроса.
        :return: Набор полей "только для чтения".
        """
        if 'add' in request.path:
            return []
        return ['start_date']
