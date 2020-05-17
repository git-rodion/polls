"""Набор представлений для Polls приложения."""
from django.db.models import QuerySet
from django.utils.datetime_safe import datetime
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView

from polls.models import Poll, User
from polls.serializers import AnswerSerializer, PollSerializer, UserSerializer


class ActivePolls(ListAPIView):
    """Представление списка активных опросов."""

    queryset = Poll.objects.all()
    serializer_class = PollSerializer

    def get_queryset(self) -> QuerySet:
        """Извлечение только активных опросов по датам."""
        queryset = super().get_queryset()
        return queryset.filter(start_date__gte=datetime.now().date(),
                               end_date__gte=datetime.now().date())


class UserAnswersDetail(RetrieveAPIView):
    """Получение пройденных пользователем опросов с детализацией."""

    queryset = User.objects.all()
    serializer_class = UserSerializer


class CreateAnswer(CreateAPIView):
    """Ответы на вопросы."""

    serializer_class = AnswerSerializer
