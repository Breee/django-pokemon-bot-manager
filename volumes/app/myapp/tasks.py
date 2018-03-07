# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery.contrib.abortable import AbortableTask

bot_processes = []


@shared_task(bind=True, base=AbortableTask)
def cel_bot_start(self):
    while not self.is_aborted():
        print('I am running')
    print('I was aborted!')
