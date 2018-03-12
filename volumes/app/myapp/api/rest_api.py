from rest_framework import serializers, viewsets
from myapp.models import PokePosition, Pokemon


class PokemonPositionSerializer(serializers.ModelSerializer):

    class Meta:
        model = PokePosition
        fields = '__all__'


class PokemonPositionSet(viewsets.ModelViewSet):
    queryset = PokePosition.objects.all()
    serializer_class = PokemonPositionSerializer


class PokemonSerializer(serializers.ModelSerializer):
    model = Pokemon

    class Meta:
        model = Pokemon
        fields = "__all__"


class PokemonSet(viewsets.ModelViewSet):
    queryset = Pokemon.objects.all()
    serializer_class = PokemonSerializer