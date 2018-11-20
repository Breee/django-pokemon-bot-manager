from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from django.views.generic import TemplateView

from BotManager.BotManager import BotManager
import json

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


@user_passes_test(lambda u: u.is_superuser, login_url='/admin')
def up(request):
    global bot_manager
    if 'bot' not in request.GET:
        return HttpResponse('Please send bot number')
    index = int(request.GET['bot'])

    if bot_manager.run_bot(index):
        return HttpResponse('Bot ' + str(index) + ' started successfully')
    else:
        return HttpResponse('Bot ' + str(index) + ' failed to start')


@user_passes_test(lambda u: u.is_superuser, login_url='/admin')
def down(request):
    global bot_manager
    if 'bot' not in request.GET:
        return HttpResponse('Please send bot number')
    index = int(request.GET['bot'])

    if bot_manager.close_bot(index):
        return HttpResponse('Bot ' + str(index) + ' closed successfully')
    else:
        return HttpResponse('Bot ' + str(index) + ' failed to close')


# we allow this without login to check the bot status from everywhere
def status(request):
    global bot_manager
    if 'bot' not in request.GET:
        bot_manager.get_all_status()
        return HttpResponse(json.dumps(bot_manager.get_all_status()))
    index = int(request.GET['bot'])

    if bot_manager.get_bot_status(index):
        return HttpResponse('Bot ' + str(index) + ' is running', status=200)
    else:
        return HttpResponse('Bot ' + str(index) + ' is down', status=204)


# we allow this without login to pull the output from everywhere
def pull_output(request):
    global bot_manager
    if 'bot' not in request.GET:
        return HttpResponse('Please send bot number')
    index = int(request.GET['bot'])

    bot_manager.get_bot_output(index)
    return HttpResponse('Bot ' + str(index) + 's output is pulled', status=200)


@user_passes_test(lambda u: u.is_superuser, login_url='/admin')
def loader_output(request):
    global bot_manager

    bot_output = bot_manager.get_log_loader_output()
    if isinstance(bot_output, str):
        context = {
            'command': 'Output',
            'bot': 'log loader',
            'lines': bot_output.splitlines()
        }
        return render(request, 'bot/output.html', context)
    else:
        return HttpResponse('something is wrong')


@user_passes_test(lambda u: u.is_superuser, login_url='/admin')
def output(request):
    global bot_manager
    if 'bot' not in request.GET:
        return HttpResponse('Please send bot number')
    index = int(request.GET['bot'])

    bot_output = bot_manager.get_bot_output(index)
    if isinstance(bot_output, str):
        context = {
            'command': 'Output',
            'bot': bot_manager.get_bot_list()[index].name,
            'lines': bot_output.splitlines()
        }
        return render(request, 'bot/output.html', context)
    else:
        return HttpResponse('something is wrong')


@user_passes_test(lambda u: u.is_superuser, login_url='/admin')
def git_pull_bot(request):
    global bot_manager
    if 'bot' not in request.GET:
        return HttpResponse('Please send bot number')
    index = int(request.GET['bot'])

    bot_output = bot_manager.git_pull_bot(index).decode('utf_8')
    context = {
        'command': 'GitPull',
        'bot': bot_manager.get_bot_list()[index].name,
        'lines': bot_output.splitlines()
    }
    return render(request, 'bot/output.html', context)


@user_passes_test(lambda u: u.is_superuser, login_url='/admin')
def clear_output(request):
    global bot_manager
    if 'bot' not in request.GET:
        return HttpResponse('Please send bot number')
    index = int(request.GET['bot'])

    if bot_manager.clear_bot_output(index):
        return HttpResponse('Bot ' + str(index) + ' output cleared')
    else:
        return HttpResponse('could not be cleared, does bot exist?')


@user_passes_test(lambda u: u.is_superuser, login_url='/admin')
def bot(request):
    context = _get_bot_context()
    return render(request, 'bot/index.html', context)


def _get_bot_context():
    global bot_manager
    bot_list = bot_manager.get_bot_list()
    status_list = bot_manager.get_all_status()
    context_list = []
    for key in range(len(bot_list)):
        context_bot = {
            'bot': bot_list[key],
            'status': status_list[key]
        }
        context_list.append(context_bot)
    context = {
        'bot_list': context_list,
    }
    return context