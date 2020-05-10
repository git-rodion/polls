from django.contrib import admin
from django.contrib.admin import ModelAdmin, TabularInline
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from polls.models import Poll, Question, User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    pass


class QuestionInline(TabularInline):
    model = Question


@admin.register(Poll)
class PollAdmin(ModelAdmin):
    inlines = [QuestionInline]
