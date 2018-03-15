from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse
import datetime


@login_required
def pokemap(request):
    context = {
    }
    return render(request, 'map/index.html', context)


def up(request):
    pass


def down(request):
    pass
