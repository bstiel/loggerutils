loggerutils
------------

loggerutils is a Python package that provides a drop-in replacement for the `logging.Formatter` class. loggerutils enriches the log message with extra information when running inside a Celery task.

Configure your logger using the `loggerutils.Formatter` class:

```python
import logging
import loggerutils

logger = logging.getLogger()
sh = logging.StreamHandler()
sh.setFormatter(loggerutils.Formatter('%(asctime)s - %(task_id)s - %(task_name)s - %(name)s - %(levelname)s - %(message)s'))
logger.setLevel(logging.INFO)
logger.addHandler(sh)
```

And you automatically get `task_id` and `task_name` when logging within a Celery task execution context.

```python
# funcs.py
import logging

logger = logging.getLogger(__name__)

def do_something():
    logger.info('Do something')
    return True
```

When calling from within a Celery task

```python
# tasks.py
import logging
import funcs
from worker import app

logger = logging.getLogger(__name__)

@app.task(bind=True)
def task(self):
    return funcs.do_something()
```

Logs

```
2018-11-06 07:33:16,140 - 7d2ec1a7-0af2-4e8c-8354-02cd0975c906 - tasks.task - tasks - INFO - Do something
```

When calling `do_something` from somewhere outside Celery, you get:

```
2018-11-06 07:33:16,140 -  -  - tasks - INFO - Do something
```

loggerutils extends the built-in Formatter styles (PercentStyle (`%`), StrFormatStyle (`{`) and StringTemplateStyle (`$`)) with Jinja2Style (`{{`). Jinja2Style leverages [Jinja2 templates](http://jinja.pocoo.org/docs/2.10/) and allows you to use conditions to prettify your log messages:

```python
...
sh.setFormatter(loggerutils.Formatter('{{asctime}}{% if task_id %} - {{task_id}} - {{task_name}}{% endif %} - {{name}} - {{levelname}} - {{message}}', style='{{'))
...
```



Motivation
----------

Celery provides a special task logger in `celery.utils.log.get_task_logger`.

This task logger enriches the log message with the Celery task's id and name.


```python
# tasks.py
import os
from celery.utils.log import get_task_logger
from worker import app

logger = get_task_logger(__name__)

@app.task()
def add(x, y):
    result = x + y
    logger.info(f'Add: {x} + {y} = {result}')
    return result
```

Produces this log output:

```
[2018-11-06 07:30:13,545: INFO/MainProcess] Received task: tasks.get_request[9c332222-d2fc-47d9-adc3-04cebbe145cb]
[2018-11-06 07:30:13,546: INFO/MainProcess] tasks.get_request[9c332222-d2fc-47d9-adc3-04cebbe145cb]: Add: 3 + 5 = 8
[2018-11-06 07:30:13,598: INFO/MainProcess] Task tasks.get_request[9c332222-d2fc-47d9-adc3-04cebbe145cb] succeeded in 0.052071799989789724s: None
```

But what to do with lower level code?


```python
# models.py
import logging

from passlib.hash import sha256_crypt
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import validates
from sqlalchemy import text
from . import db

logger = logging.getLogger(__name__)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    name = db.Column(db.String(64), unique=False, nullable=True)
    email = db.Column(db.String(256), unique=True, nullable=False)

    @validates('email')
    def validate_email(self, key, value):
        logger.info(f'Validate email address: {value}')
        if value is not None:
            assert '@' in value
            return value.lower()
```

The method `validate_email` could be called inside a Celery task. Or inside a Django or Flask request. Your model code should not know about the runtime context it is executed in.

For debugging, it is helpful to get a task id and task name if the model code runs inside a Celery task. Especially if you process a high volume of Celery tasks.



Requirements
------------

loggerutils currently works with:

* Python 3.6+



Installation
------------

To install Requests, simply use [pip](https://packaging.python.org/tutorials/installing-packages/) (or [pipenv](http://pipenv.org/):

``` {.sourceCode .bash}
$ pip install loggerutils
✨🍰✨
```



Links
-----

* [Celery Logging](http://docs.celeryproject.org/en/latest/userguide/tasks.html#logging)

* [https://www.distributedpython.com/2018/11/06/celery-task-logger-format/](https://www.distributedpython.com/2018/11/06/celery-task-logger-format/).



Contributions
-------------

Pull Requests welcome! Please open an issue to report bugs or suggest improvements.




