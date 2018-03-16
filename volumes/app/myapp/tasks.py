# Create your tasks here
from celery.contrib.abortable import AbortableTask
from mysite.celery import capp


@capp.task(bind=True, base=AbortableTask)
def cel_bot_start(self):
    pass
