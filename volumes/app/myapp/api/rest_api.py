from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import generics, serializers, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import permissions

from myapp.models import PokePosition, Pokemon

permission_classes = (permissions.IsAuthenticated,)

def set_token(request):
    token = Token.objects.filter(user=request.user)

    if token.count() == 1:
        token.delete()
    elif token.count() > 1:
        return Exception("token > 1")

    Token.objects.create(user=request.user)
    user_id = request.user.id
    return redirect(reverse('account_overview', args=[user_id]))


@api_view(['GET'])
def get_pokemon(request):
    queryset = Pokemon.objects.all()
    if 'nr' in request.GET:
        queryset = Pokemon.objects.filter(poke_nr=request.GET['nr'])
    if 'name_eng' in request.GET:
        queryset = Pokemon.objects.filter(poke_name_ger=request.GET['name_eng'])
    if 'name_ger' in request.GET:
        queryset = Pokemon.objects.filter(poke_name_ger=request.GET['name_ger'])
    serializer = PokemonSerializer(queryset, context={'request': request}, many=True)
    return Response(serializer.data)


class PokemonPositionSerializer(serializers.ModelSerializer):

    class Meta:
        model = PokePosition
        fields = ('poke_lvl', 'poke_iv', 'poke_lat', 'poke_lon', 'poke_nr', 'poke_despawn_time')


class PokemonPositionSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = PokePosition.objects.all()
    serializer_class = PokemonPositionSerializer


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
