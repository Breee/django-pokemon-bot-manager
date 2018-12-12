from datetime import timedelta

from channels.generic.websocket import AsyncWebsocketConsumer
import json

from django.utils import timezone


class PokemonConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.scope["session"]["last_updated"] = {}
        self.scope["session"]['last_updated_default'] = timezone.now() - timedelta(minutes=20)
        await self.accept()

        # is this needed?
        await self.send(text_data=json.dumps({
            'message': 'message'
        }))

    async def disconnect(self, close_code):
        pass

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
        instance = event['instance']

        message = {"type": "change",
                   "model": model_str,
                   "instance": instance}

        # only update if not updated in last 5s to spare traffic
        can_be_updated = await self.is_updated(event['updated'], model_str, 5)
        # if can_be_updated:
        self.scope["session"]["last_updated"][model_str] = timezone.now()
        await self.send(text_data=json.dumps(message))

    async def receive(self, text_data):
        '''
        Get Information from the Frontend to the Backend
        :param data:
        :return:
        '''
        data = json.loads(text_data)
        print("received: " + text_data)
        # send a OK for received
        await self.send(text_data=json.dumps({"type": "OK"}))
