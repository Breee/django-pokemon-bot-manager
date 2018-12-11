from datetime import timedelta

from channels.generic.websocket import AsyncWebsocketConsumer
import json

from django.utils import timezone


class PokemonConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.scope["session"]["last_updated"] = {}
        self.scope["session"]['last_updated_default'] = timezone.now() - timedelta(minutes=20)
        await self.channel_layer.group_add(
            "update",
            self.channel_name
        )

        await self.accept()
        await self.send(text_data=json.dumps({
            'message': 'message'
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            "update",
            self.channel_name
        )

    async def pokemon_message(self, event):
        await self.send(text_data=event["message"])

    async def is_updated(self, time, model_str, seconds_to_wait):
        last_updated_dict = self.scope["session"]["last_updated"]
        iso_ts = time
        updated = timezone.datetime.strptime(''.join(iso_ts.rsplit(':', 1)),
                                             '%Y-%m-%d %H:%M:%S.%f%z')

        if model_str in last_updated_dict:
            last_updated = last_updated_dict[model_str]
        else:
            last_updated = self.scope["session"]['last_updated_default']
        return updated > last_updated + timedelta(seconds=seconds_to_wait)

    async def update_message(self, event):
        model_str = event['model_str']

        message = {"type": "change", "model": model_str}

        # only update if not updated in last 5s to spare traffic
        can_be_updated = await self.is_updated(event['updated'], model_str, 5)
        if can_be_updated:
            self.scope["session"]["last_updated"][model_str] = timezone.now()
            await self.send(text_data=json.dumps(message))

