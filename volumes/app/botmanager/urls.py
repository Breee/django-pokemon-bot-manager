from django.urls import path

from botmanager import views as botmanager_views

urlpatterns = [
    path('',                botmanager_views.bot, name='bot'),
    path('up',              botmanager_views.up, name='up'),
    path('down',            botmanager_views.down, name='down'),
    path('status',          botmanager_views.status, name='status'),
    path('git_pull',        botmanager_views.git_pull_bot, name='git_pull'),
    path('output',          botmanager_views.output, name='output'),
    path('output/pull',     botmanager_views.pull_output, name='output'),
    path('output/clear',    botmanager_views.clear_output, name='output'),
    path('output/loader',   botmanager_views.loader_output, name='output'),
]