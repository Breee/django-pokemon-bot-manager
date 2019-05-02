from django.conf.urls import url

from core_app.websockets import consumers

websocket_urlpatterns = [
    url(r'^ws/update/map$', consumers.MapConsumer),
]
