import logging
from jinja2 import Template

__all__ = ['Formatter']


class Jinja2Style(logging.StrFormatStyle):

    def format(self, record):
        template = Template(self._fmt)
        return template.render(**record.__dict__)



class Formatter(logging.Formatter):

    def __init__(self, *args, **kwargs):
        logging._STYLES = dict(list(logging._STYLES.items()) + [('{{', (Jinja2Style, '{levelname}:{name}:{message}'))]) # monkeypatch logging._STYLES
        super().__init__(*args, **kwargs)
        try:
            from celery._state import get_current_task
            self.get_celery_task = get_current_task
        except ImportError:
            self.get_celery_task = lambda: None

    def format(self, record):
        task = self.get_celery_task()
        if task and task.request:
            record.__dict__.update(task_id=task.request.id,
                                   task_name=task.name)
        else:
            record.__dict__.setdefault('task_name', '')
            record.__dict__.setdefault('task_id', '')
        return super().format(record)
