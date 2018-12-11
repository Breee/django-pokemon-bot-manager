import channels.layers
from asgiref.sync import async_to_sync
from django.db.models.signals import post_save

from myapp.models import PokemonSpawn, PointOfInterest


def send_pokemon_update_to_websocket(*args, **kwargs):
    channel_layer = channels.layers.get_channel_layer()
    async_to_sync(channel_layer.group_send)("update", {
        'type': 'pokemon.message',
        'message': '{"type": "change", "model": "PokemonSpawn"}'
    })

def send_poi_update_to_websocket(*args, **kwargs):
    channel_layer = channels.layers.get_channel_layer()
    async_to_sync(channel_layer.group_send)("update", {
        'type': 'pokemon.message',
        'message': '{"type": "change", "model": "PointOfInterest"}'
    })


post_save.connect(send_pokemon_update_to_websocket, sender=PokemonSpawn)
post_save.connect(send_poi_update_to_websocket, sender=PointOfInterest)

