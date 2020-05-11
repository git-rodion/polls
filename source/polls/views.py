from django.http import HttpRequest
from django.utils.datetime_safe import datetime
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin

from polls.models import Poll
from polls.serializers import PollSerializer


class ActivePolls(ListModelMixin, GenericAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

    def get(self, request: HttpRequest, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset.filter(start_date__gte=datetime.now().date(),
                        end_date__lte=datetime.now().date())
        return queryset
