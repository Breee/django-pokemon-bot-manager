from django.urls import path

from myapp import views


urlpatterns = [
    path('', views.redirect_to_map),
    path('denied/', views.denied),
    path('map/', views.Pokemap.as_view(), name='map'),
]