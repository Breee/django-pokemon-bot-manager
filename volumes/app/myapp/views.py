from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test
from BotManager.BotManager import BotManager

bot_manager = BotManager()


@login_required
def pokemap(request):
    context = {
    }
    return render(request, 'map/index.html', context)


@user_passes_test(lambda u: u.is_superuser)
def up(request):
    global bot_manager
    if 'bot' not in request.GET:
        return HttpResponse('Please send bot number')
    index = int(request.GET['bot'])

    if bot_manager.run_bot(index):
        return HttpResponse('Bot ' + str(index) + ' started successfully')
    else:
        return HttpResponse('Bot ' + str(index) + ' failed to start')


@user_passes_test(lambda u: u.is_superuser)
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
        return HttpResponse('Bot ' + str(index) + ' is running')
    else:
        return HttpResponse('Bot ' + str(index) + ' is down')


@user_passes_test(lambda u: u.is_superuser)
def output(request):
    global bot_manager
    if 'bot' not in request.GET:
        return HttpResponse('Please send bot number')
    index = int(request.GET['bot'])

    bot_output = bot_manager.get_bot_output(index)
    if isinstance(bot_output, str):
        context = {
            'bot': bot_manager.get_bot_list()[index],
            'lines': bot_output.splitlines()
        }
        return render(request, 'bot/output.html', context)
    else:
        return HttpResponse('something is wrong')


@user_passes_test(lambda u: u.is_superuser)
def bot(request):
    global bot_manager
    bot_list = bot_manager.get_bot_list()
    context = {
        'bot_list': bot_list
    }
    return render(request, 'bot/index.html', context)
