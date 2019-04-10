from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView

from botmanager.BotManager import BotManager
from botmanager.views import _get_bot_context

bot_manager = BotManager()


class Pokemap(TemplateView):
    template_name = 'map/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for key, value in _get_bot_context().items():
            context[key] = value
        return context

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user = User.objects.get(pk=request.user.id)
            if not user.is_superuser:
                if not user.groups.count() > 0:
                    return redirect('/denied')
            return super().dispatch(request, *args, **kwargs)
        return redirect('/accounts/login')


def redirect_to_map(request):
    return HttpResponseRedirect(reverse('map'))


def denied(request):
    username = None
    if request.user.is_authenticated:
        username = request.user.username
        map_membership = request.user.groups.filter(name='map').exists()
    else:
        map_membership = "not logged in"
    return HttpResponse('Access denied! You are: ' + username + '<br>' +
                        'map membership: ' + str(map_membership))

