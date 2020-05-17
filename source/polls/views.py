from django.utils.datetime_safe import datetime
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView

from polls.models import Poll, User
from polls.serializers import AnswerSerializer, PollSerializer, UserSerializer


class ActivePolls(ListAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(start_date__gte=datetime.now().date(),
                               end_date__gte=datetime.now().date())


class UserAnswersDetail(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CreateAnswer(CreateAPIView):
    serializer_class = AnswerSerializer
