import channels.layers
from asgiref.sync import async_to_sync
from django.db.models.signals import post_save
from django.utils import timezone

from myapp.api.serializers import PokemonSpawnSerializer, PointOfInterestSerializer, \
    MapperSerializer, QuestSerializer
from myapp.models import PokemonSpawn, PointOfInterest, Mapper, Quest

last_updated = timezone.now()


def send_pokemon_update_to_websocket(*args, **kwargs):
    serializer = PokemonSpawnSerializer
    send_update_message('PokemonSpawn', serializer=serializer, instance=kwargs.get('instance'))


def send_poi_update_to_websocket(*args, **kwargs):
    serializer = PointOfInterestSerializer
    send_update_message('PointOfInterest', serializer=serializer, instance=kwargs.get('instance'))


def send_mapper_update_to_websocket(*args, **kwargs):
    serializer = MapperSerializer
    send_update_message('Mapper', serializer=serializer, instance=kwargs.get('instance'))


def send_quest_update_to_websocket(*args, **kwargs):
    serializer = QuestSerializer
    send_update_message('Quest', serializer=serializer, instance=kwargs.get('instance'))


def send_update_message(model_str, serializer, instance):
    instance = serializer(instance).data

    channel_layer = channels.layers.get_channel_layer()
    async_to_sync(channel_layer.group_send)("update", {
        'type': 'update.message',
        'updated':  str(timezone.now()),
        'model_str': model_str,
        'instance': instance
    })


post_save.connect(send_pokemon_update_to_websocket, sender=PokemonSpawn)
post_save.connect(send_poi_update_to_websocket, sender=PointOfInterest)
post_save.connect(send_mapper_update_to_websocket, sender=Mapper)
post_save.connect(send_quest_update_to_websocket, sender=Quest)

