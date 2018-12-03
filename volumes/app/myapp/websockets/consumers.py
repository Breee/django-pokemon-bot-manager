from channels.generic.websocket import AsyncWebsocketConsumer
import json


class PokemonConsumer(AsyncWebsocketConsumer):
    async def connect(self):
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
