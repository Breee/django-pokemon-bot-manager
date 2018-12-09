from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from myapp.api.serializers import *
from myapp.pogoprotos import ModelBridge
from myapp.pogoprotos.Pogoprotos import Pogoprotos
from pogoprotos.networking.responses.disk_encounter_response_pb2 import DiskEncounterResponse
from pogoprotos.networking.responses.encounter_response_pb2 import EncounterResponse
from pogoprotos.networking.responses.fort_details_response_pb2 import FortDetailsResponse
from pogoprotos.networking.responses.fort_search_response_pb2 import FortSearchResponse
from pogoprotos.networking.responses.get_map_objects_response_pb2 import GetMapObjectsResponse
from pogoprotos.networking.responses.gym_get_info_response_pb2 import GymGetInfoResponse


class PokedexSet(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        queryset = Pokemon.objects.all()

        # parse query string stuff
        if 'nr' in request.GET:
            queryset = queryset.filter(number=request.GET['nr'])
        if 'name_eng' in request.GET:
            queryset = queryset.filter(poke_name_ger=request.GET['name_eng'])
        if 'name_ger' in request.GET:
            queryset = queryset.filter(poke_name_ger=request.GET['name_ger'])
        serializer = PokemonSerializer(queryset, context={'request': request}, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        for key in request.data:
            data = request.data[key]
            if key == 'pokemon_move':
                return self.push_pokemon_move(data)
            if key == 'pokemon':
                return self.push_pokemon(data)
            if key == 'pokemon_type':
                queryset = PokemonType.objects.filter(name=data['name'])
                if queryset.count() <= 0:
                    return self.push_pokemon_type(data)
                else:
                    return self.update_pokemon_type(data, queryset)

    def push_pokemon(self, data):
        serializer = PokemonSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def push_pokemon_move(self, data):
        serializer = PokemonMoveSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def push_pokemon_type(self, data):
        serializer = PokemonTypeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update_pokemon_type(self, data, queryset):
        if queryset.count() > 1:
            raise serializers.ValidationError('too many possible matches for update')
        else:
            instance = queryset.first()
            for key in data:
                if hasattr(PokemonType, key):
                    setattr(instance, key, data[key])
            instance.full_clean()
            instance.save()
            serializer = PokemonTypeSerializer(instance=instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class PokemonSpawnSet(APIView):
    """
    List pokepositions which aren't despawned, or create a new pokeposition.
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        queryset = PokemonSpawn.objects.all()
        queryset = queryset.filter(disappear_time__gt=timezone.now())
        serializer = PokemonSpawnSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PokemonSpawnSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PointOfInterestSet(APIView):
    """
    Point of interests
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PointOfInterestSerializer


    def get(self, request, format=None):
        queryset = PointOfInterest.objects.all()
        serializer = PointOfInterestSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        context = []
        for item in request.data:
            serializer = PointOfInterestSerializer(data=item)
            if serializer.is_valid():
                serializer.save()
                context.append(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(context, status=status.HTTP_201_CREATED)


class RealDeviceMapBlackHole(APIView):
    """
    Push everything from RealDeviceMap here
    """
    serializer_class = RealDeviceMapBlackHoleSerializer

    def get(self, request, format=None):
        serializer = self.serializer_class()
        return Response(serializer.data)

    def post(self, request, format=None):
        data = request.data
        context = {}

        if isinstance(data, dict):
            if 'protos' in data:
                protos = Pogoprotos()
                if len(data) > 0:
                    protos.parse(data['protos'][0])
                for key in list(protos.messages):
                    message = protos.messages[key]
                    if isinstance(message, GetMapObjectsResponse):
                        for map_cell in message.map_cells:
                            ModelBridge.parse_map_cell(map_cell)
                    elif isinstance(message, EncounterResponse):
                        ModelBridge.parse_encounter_response(message)
                    elif isinstance(message, FortDetailsResponse):
                        ModelBridge.parse_fort_details_response(message)
                    elif isinstance(message, GymGetInfoResponse):
                        ModelBridge.parse_gym_get_info_response(message)
                    elif isinstance(message, DiskEncounterResponse):
                        ModelBridge.parse_disk_encounter_response(message)
                    elif isinstance(message, FortSearchResponse):
                        ModelBridge.parse_fort_search_response(message)
                    else:
                        NotImplementedError('proto_message: ' + str(key))

            for key, value in data.items():
                if key == 'quests':
                    pass
                elif key == 'pokestops':
                    if len(value) > 0:
                        for pokestop in value:
                            print(pokestop)
                            queryset = PointOfInterest.objects.filter(longitude=pokestop['longitude'],
                                                                      latitude=pokestop['latitude'])
                            if queryset.exists():
                                if queryset.count() > 1:
                                    print('pokestop is not unique!')
                                else:
                                    pokestop_object: PointOfInterest = queryset.first()
                                    pokestop_object.poi_id = pokestop['id']
                                    pokestop_object.enabled = pokestop['enabled']
                                    pokestop_object.save()
                                    print('pokestop updated')
                            else:
                                PointOfInterest.objects.create(poi_id=pokestop['id'],
                                                               longitude=pokestop['longitude'],
                                                               latitude=pokestop['latitude'],
                                                               type='pokestop')
                                print('pokestop created')
                elif key == 'spawnpoints':
                    pass
                elif key == 'pokemon':
                    if len(value) > 0:
                        for pokemon in value:
                            despawn_time = timezone.now() + timezone.timedelta(microseconds=pokemon['despawn_time'])  # one nanosecond is 1000 microseconds
                            poke_nr = Pokemon.objects.get(number=pokemon['pokemon_id'])
                            pokemon_spawn = PokemonSpawn.objects.create(poke_nr=poke_nr,
                                                                        latitude=pokemon['lat'],
                                                                        longitude=pokemon['lon'],
                                                                        disappear_time=despawn_time)
                            pokemon_spawn.save()
                elif key == 'nearby_pokemon':
                    pass
                elif key == 'validation1':
                    pass
                elif key == 'gyms':
                    pass
                else:
                    raise NotImplementedError('not in parse list: ' + key)
            if 'pokemon' in data:
                print(data['pokemon'])

        return Response(context, status=status.HTTP_201_CREATED)

