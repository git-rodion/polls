from django.http import HttpRequest
from django.utils.datetime_safe import datetime
from rest_framework.generics import ListAPIView

from polls.models import Poll
from polls.serializers import PollsSerializer


class ActivePolls(ListAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollsSerializer

    def get(self, request: HttpRequest, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(start_date__gte=datetime.now().date(),
                               end_date__gte=datetime.now().date())
