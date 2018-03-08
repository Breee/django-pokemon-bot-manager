from rest_framework import serializers
from .models import Pokemon, PokePosition


class PokemonPositionSerializer(serializers.ModelSerializer):

    class Meta:
        model = PokePosition
        fields = '__all__'


class PokemonSerializer(serializers.ModelSerializer):
    model = Pokemon

    class Meta:
        model = Pokemon
        fields = "__all__"
