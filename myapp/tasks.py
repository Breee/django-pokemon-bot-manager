# Create your tasks here
from __future__ import absolute_import, unicode_literals
from .interface import BotInterface
from time import sleep

from celery import shared_task


# Add a celery Task here with the '@shared_task' decorator
# Like this:
@shared_task
def cel_bot_up():
    newbot = BotInterface()
    return newbot.start_bot


@shared_task
def cel_bot_down():
    newbot = BotInterface()
    return newbot.stop_bot
