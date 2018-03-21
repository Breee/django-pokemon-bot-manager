from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework import generics, serializers, status, viewsets, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime
from myapp.models import PokePosition, Pokemon
import csv


class PokedexSet(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @api_view(['GET'])
    def get_pokemon(request):
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

    @api_view(['GET'])
    def init_pokemon(request):
        """
        Load Pokedex if Database is empty
        TODO: Find a better way to init!
        """
        Pokemon.objects.all().delete()
        if Pokemon.objects.count() == 0:
            with open('pokedex.csv') as pokedex_ger:
                reader = csv.DictReader(pokedex_ger)
                for poke in reader:
                    pid = poke['Ndex']
                    newpoke = Pokemon(poke_nr=int(pid),
                                      poke_name_eng=poke['English'],
                                      poke_name_ger=poke['German'])
                    newpoke.save()
                pokedex_ger.close()
                print('pokedex_ger written')
        return HttpResponse('[]')


class PokemonPositionSerializer(serializers.ModelSerializer):

    class Meta:
        model = PokePosition
        fields = ('poke_lvl', 'poke_iv', 'poke_lat', 'poke_lon', 'poke_nr', 'poke_despawn_time')


class PokemonPositionSet(APIView):
    """
    List pokepositions which aren't despawned, or create a new pokeposition.
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        queryset = PokePosition.objects.all()
        queryset = queryset.filter(poke_despawn_time__gt=datetime.utcnow())
        serializer = PokemonPositionSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PokemonPositionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PokemonSerializer(serializers.ModelSerializer):
    model = Pokemon

    class Meta:
        model = Pokemon
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username')


class UserList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
