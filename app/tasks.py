# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task


# Add a celery Task here with the '@shared_task' decorator
# Like this:
def example_add(x, y):
    return x + y
