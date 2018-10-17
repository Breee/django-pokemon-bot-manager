from rest_framework import serializers
from myapp.models import *


class PokemonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pokemon
        fields = '__all__'


class PokemonMoveSerializer(serializers.ModelSerializer):

    class Meta:
        model = PokemonMove
        fields = '__all__'


class PokemonTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = PokemonType
        fields = '__all__'


class PokemonSpawnSerializer(serializers.ModelSerializer):

    class Meta:
        model = PokemonSpawn
        fields = '__all__'


class PointOfInterestSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        many = kwargs.pop('many', True)
        super(PointOfInterestSerializer, self).__init__(many=many, *args, **kwargs)

    class Meta:
        model = PointOfInterest
        fields = '__all__'


class PokeStopLureSerializer(serializers.ModelSerializer):

    class Meta:
        model = PokeStopLure
        fields = '__meta__'


class RaidSerializer(serializers.ModelSerializer):

    class Meta:
        model = Raid
        fields = '__meta__'


class GymPokemonSerializer(serializers.ModelSerializer):

    class Meta:
        model = GymPokemon
        fields = '__meta__'


class GymStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = GymStatus
        fields = '__all__'
