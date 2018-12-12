from django.conf.urls import url

from myapp.websockets import consumers

websocket_urlpatterns = [
    url(r'^ws/update/$', consumers.PokemonConsumer),
]
