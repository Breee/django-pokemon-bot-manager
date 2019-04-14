import allauth.account.signals
import requests
from allauth.socialaccount.models import SocialToken, SocialAccount
import channels.layers
from asgiref.sync import async_to_sync
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.utils import timezone
import logging

from myapp.api.serializers import PokestopSerializer
from myapp.models import Pokestops, AllowedDiscordServer, TrsQuest

last_updated = timezone.now()

logger = logging.getLogger('default')
from django.dispatch import receiver

@receiver(post_save, sender=Pokestops)
def send_pokestop_update_to_websocket(*args, **kwargs):
    serializer = PokestopSerializer
    send_update_message('pokestop', serializer=serializer, instance=kwargs.get('instance'), fields=('external_id', 'lat', 'lon', 'url', 'name', 'quest'))

@receiver(post_save, sender=TrsQuest)
def send_quest_update_to_websocket(*args, **kwargs):
    print("update")
    serializer = PokestopSerializer
    quest = kwargs.get('instance')
    pokestop = Pokestops.objects.all().filter(external_id=quest.guid).first()
    send_update_message('pokestop', serializer=serializer, instance=pokestop, fields=('external_id', 'lat', 'lon', 'url', 'name', 'quest'))


#def send_poi_update_to_websocket(*args, **kwargs):
#    serializer = PointOfInterestSerializer
#    send_update_message('PointOfInterest', serializer=serializer, instance=kwargs.get('instance'))
#
#
#def send_mapper_update_to_websocket(*args, **kwargs):
#    serializer = MapperSerializer
#    send_update_message('Mapper', serializer=serializer, instance=kwargs.get('instance'))
#
#
#def send_quest_update_to_websocket(*args, **kwargs):
#    serializer = QuestSerializer
#    send_update_message('Quest', serializer=serializer, instance=kwargs.get('instance'))
#

def send_update_message(model_str, serializer, instance, fields=None):
    if fields:
        instance = serializer(instance, fields=fields).data
    else:
        instance = serializer(instance).data
    channel_layer = channels.layers.get_channel_layer()
    async_to_sync(channel_layer.group_send)("update", {
        'type': 'update_message',
        'updated':  str(timezone.now()),
        'model_str': model_str,
        'instance': instance
    })


def get_discord_guild_information(request, user, *args, **kwargs):
    if '/accounts/discord/' in request.path:
        user = User.objects.get(username=user)
        social_account = SocialAccount.objects.get(user=user)
        social_token = SocialToken.objects.get(account=social_account)

        discord_group = Group.objects.filter(name='map')
        if not discord_group.exists():
            logger.warning('the default group "map" does not exist, please add this group')
        discord_group = discord_group.first()

        headers = {
            'Authorization': 'Bearer {0}'.format(social_token.token),
            'Content-Type': 'application/json',
        }

        extra_data = requests.get('https://discordapp.com/api/users/@me/guilds', headers=headers)
        for server in extra_data.json():
            for allowed_server in AllowedDiscordServer.objects.all():
                if allowed_server.server_id == server['id']:
                    discord_group.user_set.add(user)
                    return
        discord_group.user_set.remove(user)


#post_save.connect(send_pokestop_update_to_websocket(), sender=Pokestops)
#post_save.connect(send_poi_update_to_websocket, sender=PointOfInterest)
#post_save.connect(send_mapper_update_to_websocket, sender=Mapper)
#post_save.connect(send_quest_update_to_websocket, sender=Quest)
allauth.account.signals.user_logged_in.connect(get_discord_guild_information)
