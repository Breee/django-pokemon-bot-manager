from datetime import timedelta

import channels.layers
from asgiref.sync import async_to_sync
from django.db.models import Model
from django.db.models.signals import post_save
from django.utils import timezone

from myapp.models import PokemonSpawn, PointOfInterest, Mapper

last_updated = timezone.now()


def send_pokemon_update_to_websocket(*args, **kwargs):
    send_message('PokemonSpawn')


def send_poi_update_to_websocket(*args, **kwargs):
    send_message('PointOfInterest')


def send_mapper_update_to_websocket(*args, **kwargs):
    send_message('Mapper')


def send_message(model_str):
    channel_layer = channels.layers.get_channel_layer()
    async_to_sync(channel_layer.group_send)("update", {
        'type': 'update.message',
        'updated':  str(timezone.now()),
        'model_str': model_str
    })


post_save.connect(send_pokemon_update_to_websocket, sender=PokemonSpawn)
post_save.connect(send_poi_update_to_websocket, sender=PointOfInterest)
post_save.connect(send_mapper_update_to_websocket, sender=Mapper)

