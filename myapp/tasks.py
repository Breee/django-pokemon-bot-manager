# Create your tasks here
from __future__ import absolute_import, unicode_literals
from .interface import PollBot  # for dem bots
from celery.result import AsyncResult
from celery import shared_task
import celery

# Add a celery Task here with the '@shared_task' decorator
# Like this:

bot = PollBot()


@shared_task(bind=True)
def cel_bot_up(capp):
    global bot
    token = 'NDExNTM5NTY4Mjg2NzYwOTcw.DV9MNA.iKa3qlTDObDYo5EG_F0kDaLCVvU'
    bot.myinit(prefix="!raid-", token=token, description="")
    bot.run()


@shared_task(bind=True)
def cel_bot_down(capp):
    global bot
    bot.close()


@shared_task(bind=True)
def cel_bot_status(capp):
    global bot
    return bot.get_dict()
