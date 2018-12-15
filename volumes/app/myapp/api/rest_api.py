from datetime import timedelta

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
            if 'uuid' in data:
                self.update_mapper_info(data)
            if 'protos' in data:
                protos = Pogoprotos()
                if len(data['protos']) > 0:
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
                if key == 'validation1':
                    pass
                elif key == 'protos':
                    pass
                elif key == 'submit_version':
                    pass
                elif key == 'longitude':
                    pass
                elif key == 'latitude':
                    pass
                elif key == 'uuid':
                    pass
                elif key == 'trainerlvl':
                    pass
                elif key == 'timestamp':
                    pass
                else:
                    raise NotImplementedError('not in parse list: ' + key)
            if 'pokemon' in data:
                print(data['pokemon'])

        return Response(context, status=status.HTTP_201_CREATED)

    @staticmethod
    def update_mapper_info(data):
        if not Mapper.objects.filter(uuid=data['uuid']).exists():
            Mapper.objects.create(uuid=data['uuid'],
                                  longitude=data['longitude'],
                                  latitude=data['latitude'],
                                  trainerlevel=data['trainerlvl'])
        else:
            mapper = Mapper.objects.get(uuid=data['uuid'])
            mapper.longitude = data['longitude']
            mapper.latitude = data['latitude']
            mapper.trainerlevel= data['trainerlvl']
            mapper.save()


class QuestSet(APIView):
    """
    Quests
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PointOfInterestSerializer

    def get(self, request, format=None):
        queryset = Quest.objects.filter(created__gte=timezone.datetime.combine(
            timezone.localtime().date(),
            timezone.localtime().time().replace(hour=00, minute=00, second=00)
        ))

        # parse query string stuff
        if 'pokestop' in request.GET:
            queryset = queryset.filter(pokestop_id=request.GET['pokestop'])
        serializer = QuestSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        context = []
        for item in request.data:
            serializer = QuestSerializer(data=item)
            if serializer.is_valid():
                serializer.save()
                context.append(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(context, status=status.HTTP_201_CREATED)


class MapperSet(APIView):
    """
    Quests
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = MapperSerializer

    def get(self, request, format=None):
        queryset = Mapper.objects.filter(updated__gte=timezone.localtime() - timedelta(minutes=5))
        # parse query string stuff
        serializer = MapperSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        context = []
        for item in request.data:
            serializer = MapperSerializer(data=item)
            if serializer.is_valid():
                serializer.save()
                context.append(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(context, status=status.HTTP_201_CREATED)

class RaidSet(APIView):
    """
    Raids
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = RaidSerializer

    def get(self, request, format=None):
        queryset = Raid.objects.filter(time_start__lte=timezone.localtime(),
                                       time_end__gte=timezone.localtime())
        # parse query string stuff
        serializer = RaidSerializer(queryset, many=True)
        return Response(serializer.data)
