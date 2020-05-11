from rest_framework.serializers import ModelSerializer

from polls.models import ExpectedAnswer, Poll, Question


class ExpectedAnswerSerializer(ModelSerializer):
    class Meta:
        model = ExpectedAnswer
        fields = ['content']


class QuestionSerializer(ModelSerializer):
    expectedanswer_set = ExpectedAnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = '__all__'


class PollSerializer(ModelSerializer):
    question_set = QuestionSerializer(many=True)

    class Meta:
        model = Poll
        fields = '__all__'
