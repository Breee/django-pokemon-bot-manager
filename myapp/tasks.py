# Create your tasks here
from __future__ import absolute_import, unicode_literals

from time import sleep

from celery import shared_task


# Add a celery Task here with the '@shared_task' decorator
# Like this:
@shared_task
def example_add(x, y):
    sleep(5)
    return x + y
