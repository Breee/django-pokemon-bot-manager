"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from myapp import views


urlpatterns = [
    path('', views.redirect_to_map),
    path('denied/', views.denied),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('api/', include('myapp.api.rest_urls')),
    path('map/', views.pokemap, name='map'),
    path('bot/', views.bot, name='bot'),
    path('bot/up', views.up, name='up'),
    path('bot/down', views.down, name='down'),
    path('bot/status', views.status, name='status'),
    path('bot/output', views.output, name='output'),
    path('bot/output/clear', views.clear_output, name='output'),
]