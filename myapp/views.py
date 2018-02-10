from django.http import HttpResponse
from django.shortcuts import render
from .tasks import example_add
from celery.result import AsyncResult


# Create your views here.
def test(request):
    # This is how you request to celery and then get the result
    cetest = example_add.delay(2, 3)
    print(cetest)
    # Get the Result from Async request.
    res = AsyncResult(cetest.id, app=cetest)
    print(res.get())
    return HttpResponse()
