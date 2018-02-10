from django.http import HttpResponse
from django.shortcuts import render
from .tasks import *
from celery.result import AsyncResult

from discord.ext import commands


# Create your views here.
def up(request):
    # This is how you request to celery and then get the result
    cbotup = cel_bot_up.delay()
    # Get the Result from Async request.
    #
    # res = AsyncResult(cetest.id, app=cetest)
    # print(res.get())

    # NOT WORKING RIGHT NOW
    print(AsyncResult(cbotup.id, app=cbotup))
    return HttpResponse('should be up now?!')


def down(request):
    cel_bot_down.delay()
    return HttpResponse('am i down, nao?')
