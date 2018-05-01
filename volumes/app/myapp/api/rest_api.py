from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from myapp.api.serializers import *


class PokedexSet(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        queryset = Pokemon.objects.all()

        # parse query string stuff
        if 'nr' in request.GET:
            queryset = queryset.filter(poke_nr=request.GET['nr'])
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
