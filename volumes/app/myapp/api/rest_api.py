from datetime import datetime
from django.contrib.auth.models import User
from rest_framework import generics, serializers, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import permissions

from myapp.models import PokePosition, Pokemon

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


class PokemonPositionSerializer(serializers.ModelSerializer):

    class Meta:
        model = PokePosition
        fields = ('poke_lvl', 'poke_iv', 'poke_lat', 'poke_lon', 'poke_nr', 'poke_despawn_time')


class PokemonPositionSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = PokePosition.objects.all()
    serializer_class = PokemonPositionSerializer

    # return only pokemon which are not despawned yet
    queryset = queryset.filter(poke_despawn_time__gt=datetime.now())


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
