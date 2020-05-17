from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from polls.models import Answer, Poll, Question


class QuestionSerializer(ModelSerializer):
    class Meta:
        model = Question
        exclude = ['poll']


class PollsSerializer(ModelSerializer):
    question_set = QuestionSerializer(many=True)

    class Meta:
        model = Poll
        fields = '__all__'


class CreateAnswerSerializer(ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'

    def validate(self, attrs: dict) -> dict:
        answers = (attrs['text'], attrs['choices'])
        if not any(answers) or all(answers):
            raise ValidationError(detail='Недопустимое количество '
                                         'ответов на вопрос.')

        type_choices = attrs['question'].TypeChoices
        if attrs['question'].type == type_choices.TEXT_ANSWER:
            if not attrs['text']:
                raise ValidationError(detail='Для указанного вопроса '
                                             'отсутствует ответ в виде '
                                             'текста.')
        elif attrs['question'].type == type_choices.SINGLE_ANSWER:
            if len(attrs['choices']) != 1:
                raise ValidationError(detail='Для указанного вопроса '
                                             'слишком много выбранных '
                                             'вариантов ответа.')
        elif attrs['question'].type == type_choices.SEVERAL_OPTIONS_ANSWER:
            if len(attrs['choices']) == 0:
                raise ValidationError(detail='Для указанного вопроса не'
                                             ' указан ни один вариант '
                                             'ответа.')
        for choice in attrs['choices']:
            if choice not in attrs['question'].answeroption_set.all():
                raise ValidationError(detail='Указанный вариант ответа '
                                             'недоступен для этого вопроса.')

        return attrs
