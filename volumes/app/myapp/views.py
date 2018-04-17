from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from BotManager.BotManager import BotManager

bot_manager = BotManager()


@csrf_protect
@login_required()
@user_passes_test(lambda u: u.groups.count() > 0, login_url='/denied')
def pokemap(request):
    context = {
    }
    return render(request, 'map/index.html', context)


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
        return HttpResponse('Please send bot number')
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
            'bot': bot_manager.get_bot_list()[index].name,
            'lines': bot_output.splitlines()
        }
        return render(request, 'bot/output.html', context)
    else:
        return HttpResponse('something is wrong')


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
    global bot_manager
    bot_list = bot_manager.get_bot_list()
    stat = bot_manager.get_all_status()
    context = {
        'bot_list': bot_list,
        'bot_status': stat
    }
    return render(request, 'bot/index.html', context)
