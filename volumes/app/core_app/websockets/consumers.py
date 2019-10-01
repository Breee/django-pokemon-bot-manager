import json

from datetime import timedelta
from typing import List
from django.utils import timezone
from channels.generic.websocket import AsyncWebsocketConsumer
from geofence.geofencehelper import GeofenceHelper
from channels.db import database_sync_to_async
from scannerdb.rocketdb import Gym, Pokestop
from core_app.api.serializers import PokestopSerializer, GymSerializer


with open("jsonData/pokemon.json", 'r') as pokemon_file:
    POKEDEX = {x['number']:x for x in json.load(pokemon_file)}


class UpdateConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.scope["session"]["last_updated"] = {}
        self.scope["session"]['last_updated_default'] = timezone.now() - timedelta(minutes=20)
        await self.channel_layer.group_add(
            "update",
            self.channel_name
        )
        await self.accept()
        await self.send(text_data=json.dumps({"type": "viewport_information_request"}))

    async def disconnect(self, close_code):
        pass

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
        print(event)
        model_str = event['model_str']
        instance = event['instance']

        message = {"type": "change",
                   "model": model_str,
                   "instance": [instance]}

        # only update if not updated in last 5s to spare traffic
        can_be_updated = await self.is_updated(event['updated'], model_str, 5)
        if can_be_updated:
            print("can_be_updated")
            self.scope["session"]["last_updated"][model_str] = timezone.now()
            await self.send(text_data=json.dumps(message))


class MapConsumer(UpdateConsumer):

    async def receive(self, text_data):
        '''
        Get Information from the Frontend to the Backend
        :param data:
        :return:
        '''
        data = json.loads(text_data)
        if data['type'] == 'viewport_information_answer':
            # Do stuff
            geofence_dict = {'name':        'viewport_information',
                             'coordinates': [(float(data['corners']['top_left']['lat']), float(data['corners']['top_left']['lng'])),
                                             (float(data['corners']['top_right']['lat']), float(data['corners']['top_right']['lng'])),
                                             (float(data['corners']['bottom_right']['lat']), float(data['corners']['bottom_right']['lng'])),
                                             (float(data['corners']['bottom_left']['lat']), float(data['corners']['bottom_left']['lng']))]
                             }
            serialized_stops = await self.get_pokestops(geofence_dict)
            msg = {'type': 'pokestops', 'pokestops': serialized_stops.data}
            await self.send(text_data=json.dumps(msg))
            serialized_gyms = await self.get_gyms(geofence_dict)
            msg = {'type': 'gyms', 'gyms': serialized_gyms.data}
            await self.send(text_data=json.dumps(msg))

        # send a OK for received
        await self.send(text_data=json.dumps({"type": "OK"}))

    @database_sync_to_async
    def get_pokestops(self, geofence_dict):
        geofence_helper = GeofenceHelper(geofence_dict=geofence_dict)
        pokestops: List[Pokestop] = Pokestop.objects.all()
        geofenced_stops = []
        for stop in pokestops:
            if geofence_helper.is_in_any_geofence(latitude=stop.latitude, longitude=stop.longitude):
                geofenced_stops.append(stop)
        serialized_stops = PokestopSerializer(geofenced_stops, many=True, fields=('pokestop_id', 'latitude', 'longitude', 'image', 'name', 'quest'))
        return serialized_stops

    @database_sync_to_async
    def get_gyms(self, geofence_dict):
        geofence_helper = GeofenceHelper(geofence_dict=geofence_dict)
        gyms: List[Gym] = Gym.objects.all()
        geofenced_stops = []
        for gym in gyms:
            if geofence_helper.is_in_any_geofence(latitude=gym.latitude, longitude=gym.longitude):
                geofenced_stops.append(gym)
        serialized_stops = GymSerializer(geofenced_stops, many=True, fields=('gym_id', 'latitude', 'longitude', 'raid', 'team_id', 'slots_available', 'info'))
        return serialized_stops
