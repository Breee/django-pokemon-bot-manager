import channels.layers
from asgiref.sync import async_to_sync
from django.db.models.signals import post_save

from myapp.models import PokemonSpawn


def send_message_to_websocket(*args, **kwargs):
    channel_layer = channels.layers.get_channel_layer()
    async_to_sync(channel_layer.group_send)("update", {
        'type': 'pokemon.message',
        'message': '{"type": "change"}'
    })


post_save.connect(send_message_to_websocket, sender=PokemonSpawn)

