from django.test import TestCase
from django.utils.datetime_safe import date

from polls.models import Poll


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
