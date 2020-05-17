from django.test import TestCase
from django.utils.datetime_safe import date

from polls.models import AnswerOption, Poll, Question


class PollTestCase(TestCase):
    def setUp(self) -> None:
        self.today = date.today()
        Poll.objects.create(name='Проверочный опрос', start_date=self.today,
                            end_date=self.today,
                            description='Описание для опроса')

    def test_poll_has_correct_str_view(self):
        poll = Poll.objects.get(name='Проверочный опрос')
        expected_result = f'Проверочный опрос ({self.today} - {self.today})'
        self.assertEqual(str(poll), expected_result)


class QuestionTestCase(TestCase):
    def setUp(self) -> None:
        poll = Poll.objects.create(
            name='Проверочный опрос', start_date=date.today(),
            end_date=date.today(), description='Описание для опроса')
        Question.objects.create(text='Что должно здесь быть?',
                                type=Question.TypeChoices.TEXT_ANSWER,
                                poll=poll)

    def test_question_has_correct_str_view(self):
        text = 'Что должно здесь быть?'
        question = Question.objects.get(text=text)
        self.assertEqual(str(question), f'TEXT_ANSWER: {text}')


class AnswerOptionTestCase(TestCase):
    def setUp(self) -> None:
        poll = Poll.objects.create(name='Проверочный опрос',
                                   start_date=date.today(),
                                   end_date=date.today(),
                                   description='Описание для опроса')
        question = Question.objects.create(
            text='Что должно здесь быть?',
            type=Question.TypeChoices.TEXT_ANSWER, poll=poll)
        AnswerOption.objects.create(question=question, content='Django')

    def test_answer_option_has_correct_view(self):
        content = 'Django'
        answer_option = AnswerOption.objects.get(content=content)
        self.assertEqual(str(answer_option), content)
