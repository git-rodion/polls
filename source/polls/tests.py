from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils.datetime_safe import date
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_400_BAD_REQUEST)
from rest_framework.test import APITestCase

from polls.models import AnswerOption, Poll, Question, User


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


class ActivePollsTestCase(APITestCase):
    def setUp(self) -> None:
        User.objects.create_user('test')

        poll = Poll.objects.create(name='Проверочный опрос',
                                   start_date=date.today(),
                                   end_date=date.today(),
                                   description='Описание для опроса')
        yesterday = date.today() - timedelta(days=1)
        Poll.objects.create(name='Неактивный опрос', start_date=yesterday,
                            end_date=yesterday,
                            description='Описание для опроса')

        self.text_answer_question = Question.objects.create(
            text='Как работают Middleware?',
            type=Question.TypeChoices.TEXT_ANSWER, poll=poll)

        self.single_answer_question = Question.objects.create(
            text='Django или Flask?', type=Question.TypeChoices.SINGLE_ANSWER,
            poll=poll)
        AnswerOption.objects.create(question=self.single_answer_question,
                                    content='Django')
        AnswerOption.objects.create(question=self.single_answer_question,
                                    content='Flask')

        self.several_options_answer_question = Question.objects.create(
            text='Какие возможности в Django?',
            type=Question.TypeChoices.SEVERAL_OPTIONS_ANSWER,
        poll=poll)
        AnswerOption.objects.create(
            question=self.several_options_answer_question, content='ASGI')
        AnswerOption.objects.create(
            question=self.several_options_answer_question, content='WSGI')
        AnswerOption.objects.create(
            question=self.several_options_answer_question, content='ML')

    def test_polls_are_active(self):
        url = reverse('active_polls')
        response = self.client.get(url)
        expected_response = [
            {'id': 3, 'question_set': [
                {'id': 4, 'text': 'Как работают Middleware?',
                 'type': 'TEXT_ANSWER'},
                {'id': 5, 'text': 'Django или Flask?',
                 'type': 'SINGLE_ANSWER'},
                {'id': 6, 'text': 'Какие возможности в Django?',
                 'type': 'SEVERAL_OPTIONS_ANSWER'}],
             'name': 'Проверочный опрос', 'start_date': str(date.today()),
             'end_date': str(date.today()),
             'description': 'Описание для опроса'}]

        self.assertListEqual(response.json(), expected_response)
        self.assertEqual(response.status_code, HTTP_200_OK)


    def test_answer_by_question_type(self):
        url = reverse('create_answer')

        response = self.client.post(
            url, data={'user': 1, 'question': self.text_answer_question.id})
        expected_response = {
            'non_field_errors': ['Недопустимое количество ответов на '
                                 'вопрос.']}
        self.assertDictEqual(response.json(), expected_response)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

        response = self.client.post(
            url, data={'user': 1, 'question': self.text_answer_question.id,
                       'text': 'Какой-то текст', 'choices': [1, 2]})
        self.assertDictEqual(response.json(), expected_response)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

        response = self.client.post(url,
            data={'user': 1, 'question': self.text_answer_question.id,
                  'text': '', 'choices': [1, 2]})
        expected_response = {
            'non_field_errors': ['Для указанного вопроса отсутствует '
                                 'ответ в виде текста.']}
        self.assertDictEqual(response.json(), expected_response)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

        response = self.client.post(
            url, data={'user': 1, 'question': self.single_answer_question.id,
                       'text': '', 'choices': [1, 2]})
        expected_response = {
            'non_field_errors': ['Для указанного вопроса слишком много '
                                 'выбранных вариантов ответа.']}
        self.assertDictEqual(response.json(), expected_response)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

        response = self.client.post(url,
            data={'user': 1,
                  'question': self.several_options_answer_question.id,
                  'text': 'Какой-то текст.', 'choices': []})
        expected_response = {
            'non_field_errors': ['Для указанного вопроса не указан ни '
                                 'один вариант ответа.']}
        self.assertDictEqual(response.json(), expected_response)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

        response = self.client.post(
            url, data={'user': 1,
                       'question': self.several_options_answer_question.id,
                       'text': '', 'choices': [2, 3, 4]})
        expected_response = {
            'non_field_errors': ['Указанный вариант ответа недоступен '
                                 'для этого вопроса.']}
        self.assertDictEqual(response.json(), expected_response)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

        good_response = self.client.post(
            url, data={'user': 1, 'question': self.single_answer_question.id,
                       'choices': [1]})
        expected_response = {'id': 1, 'text': '', 'user': 1, 'question': 2,
                             'choices': [1]}
        self.assertDictEqual(good_response.json(), expected_response)
        self.assertEqual(good_response.status_code, HTTP_201_CREATED)
