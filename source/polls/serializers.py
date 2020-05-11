from rest_framework.serializers import ModelSerializer

from polls.models import Poll, Question


class QuestionSerializer(ModelSerializer):
    class Meta:
        model = Question
        exclude = ['poll']


class PollsSerializer(ModelSerializer):
    question_set = QuestionSerializer(many=True)

    class Meta:
        model = Poll
        fields = '__all__'
