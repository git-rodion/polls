from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from polls.models import Answer, AnswerOption, Poll, Question, User


class _QuestionSerializer(ModelSerializer):
    """Сериализатор вопроса с ограниченным набором полей."""

    class Meta:
        model = Question
        exclude = ['poll']


class _QuestionWithoutIDSerializer(_QuestionSerializer):
    """Сериализатор вопроса без его идентификатора."""

    class Meta(_QuestionSerializer.Meta):
        exclude = _QuestionSerializer.Meta.exclude + ['id']


class PollSerializer(ModelSerializer):
    """Сериализатор опроса."""

    question_set = _QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Poll
        fields = '__all__'


class _ChoicesSerializer(ModelSerializer):
    """Сериализатор вариантов ответа на вопрос."""

    class Meta:
        model = AnswerOption
        exclude = ['question']


class _AnswerDetailSerializer(ModelSerializer):
    """Сериализатор ответа на вопрос (в деталях)."""

    question = _QuestionWithoutIDSerializer(read_only=True)
    choices = _ChoicesSerializer(many=True, read_only=True)

    class Meta:
        model = Answer
        exclude = ['user', 'id']


class UserSerializer(ModelSerializer):
    """Сериализатор пользователя."""

    answer_set = _AnswerDetailSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['answer_set']


class AnswerSerializer(ModelSerializer):
    """Сериализатор ответа на вопрос."""

    class Meta:
        model = Answer
        fields = '__all__'

    def validate(self, attrs: dict) -> dict:
        """
        Валидация отправленных данных в целостности.

        Проверка бизнес-правил:
        - Ответ должен быть только в одном из полей.
        - В зависимости от типа вопроса, существуют разные наборы
        проверок:
            - Для TEXT_ANSWER ожидаются данные в поле text.
            - Для SINGLE_ANSWER ожидаются данные в поле choices с
                проверкой на количество (равно 1).
            - Для SEVERAL_OPTIONS_ANSWER ожидаются данные в поле choices
                (не менее 0).
        - Выбранные варианты ответа проверяются на соответствие типу
            вопроса и его доступным вариантам.

        :param attrs: Набор данных (поле: значение) в целостности.
        :return: Проверенный набор данных.
        """
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
