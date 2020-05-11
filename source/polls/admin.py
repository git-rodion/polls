from django.contrib import admin
from django.contrib.admin import ModelAdmin, StackedInline
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.http import HttpRequest

from polls.models import AnswerOption, Poll, Question, User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    pass


class AnswerOptionInline(StackedInline):
    model = AnswerOption


@admin.register(Question)
class QuestionAdmin(ModelAdmin):
    inlines = [AnswerOptionInline]


@admin.register(Poll)
class PollAdmin(ModelAdmin):
    def get_readonly_fields(self, request: HttpRequest, obj: Poll = None):
        if 'add' in request.path:
            return []
        return ['start_date']
