from django.urls import path

from myapp import views

urlpatterns = [
    path('', views.redirect_to_map),
    path('denied/', views.denied),
    path('map/', views.Pokemap.as_view(), name='map'),
    path('bot/', views.bot, name='bot'),
    path('bot/up', views.up, name='up'),
    path('bot/down', views.down, name='down'),
    path('bot/status', views.status, name='status'),
    path('bot/git_pull', views.git_pull_bot, name='git_pull'),
    path('bot/output', views.output, name='output'),
    path('bot/output/pull', views.pull_output, name='output'),
    path('bot/output/clear', views.clear_output, name='output'),
    path('bot/output/loader', views.loader_output, name='output'),
]


def one_time_startup():
    views._up_hack(0)
    views._up_hack(2)


one_time_startup()
