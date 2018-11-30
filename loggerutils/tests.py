import unittest
import logging

from unittest import mock
from freezegun import freeze_time
from loggerutils import Formatter


class TestCase(unittest.TestCase):

    def setUp(self):
        with freeze_time('2018-11-29T10:00:00+00:00'):
            self.record = logging.LogRecord(
                name='root',
                level=logging.INFO,
                pathname='',
                lineno=2,
                msg='a log message',
                args=(),
                exc_info=None,)


class PercentStyleTestCase(TestCase):

    def setUp(self):
        super().setUp()
        self.format = '%(asctime)s [%(task_id)s:%(task_name)s] - %(name)s - %(levelname)s - %(message)s'

    def test_without_celery(self):
        formatter = Formatter(self.format, style='%')
        log_message = formatter.format(self.record)
        self.assertEqual(log_message, '2018-11-29 10:00:00,000 [:] - root - INFO - a log message')

    def test_with_celery(self):
        mocked_task = mock.Mock(request=mock.Mock(id='some-id'))
        mocked_task.name = 'task.name'
        formatter = Formatter(self.format, style='%')
        formatter.get_celery_task = lambda: mocked_task
        log_message = formatter.format(self.record)
        self.assertEqual(log_message, '2018-11-29 10:00:00,000 [some-id:task.name] - root - INFO - a log message')


class StrStyleTestCase(TestCase):

    def setUp(self):
        super().setUp()
        self.format = '{asctime} [{task_id}:{task_name}] - {name} - {levelname} - {message}'

    def test_without_celery(self):
        formatter = Formatter(self.format, style='{')
        log_message = formatter.format(self.record)
        self.assertEqual(log_message, '2018-11-29 10:00:00,000 [:] - root - INFO - a log message')

    def test_with_celery(self):
        mocked_task = mock.Mock(request=mock.Mock(id='some-id'))
        mocked_task.name = 'task.name'
        formatter = Formatter(self.format, style='{')
        formatter.get_celery_task = lambda: mocked_task
        log_message = formatter.format(self.record)
        self.assertEqual(log_message, '2018-11-29 10:00:00,000 [some-id:task.name] - root - INFO - a log message')


class StringTemplateStyleTestCase(TestCase):

    def setUp(self):
        super().setUp()
        self.format = '${asctime} [${task_id}:${task_name}] - ${name} - ${levelname} - ${message}'

    def test_without_celery(self):
        formatter = Formatter(self.format, style='$')
        log_message = formatter.format(self.record)
        self.assertEqual(log_message, '2018-11-29 10:00:00,000 [:] - root - INFO - a log message')

    def test_with_celery(self):
        mocked_task = mock.Mock(request=mock.Mock(id='some-id'))
        mocked_task.name = 'task.name'
        formatter = Formatter(self.format, style='$')
        formatter.get_celery_task = lambda: mocked_task
        log_message = formatter.format(self.record)
        self.assertEqual(log_message, '2018-11-29 10:00:00,000 [some-id:task.name] - root - INFO - a log message')


class Jinja2TestCase(TestCase):

    def setUp(self):
        super().setUp()
        self.format = '{{asctime}}{% if task_id %} [{{task_id}}:{{task_name}}]{% endif %} - {{name}} - {{levelname}} - {{message}}'

    def test_without_celery(self):
        formatter = Formatter(self.format, style='{{')
        log_message = formatter.format(self.record)
        self.assertEqual(log_message, '2018-11-29 10:00:00,000 - root - INFO - a log message')

    def test_with_celery(self):
        mocked_task = mock.Mock(request=mock.Mock(id='some-id'))
        mocked_task.name = 'task.name'
        formatter = Formatter(self.format, style='{{')
        formatter.get_celery_task = lambda: mocked_task
        log_message = formatter.format(self.record)
        self.assertEqual(log_message, '2018-11-29 10:00:00,000 [some-id:task.name] - root - INFO - a log message')

