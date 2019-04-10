from rest_framework import serializers
from myapp.models import *
import datetime

#class PokemonSerializer(serializers.ModelSerializer):
#
#    class Meta:
#        model = Pokemon
#        fields = '__all__'
#
#
#class PokemonMoveSerializer(serializers.ModelSerializer):
#
#    class Meta:
#        model = PokemonMove
#        fields = '__all__'
#
#
#class PokemonTypeSerializer(serializers.ModelSerializer):
#
#    class Meta:
#        model = PokemonType
#        fields = '__all__'
#
#
#class PokemonSpawnSerializer(serializers.ModelSerializer):
#
#    class Meta:
#        model = PokemonSpawn
#        fields = '__all__'
#
#
#class RaidSerializer(serializers.ModelSerializer):
#    def __init__(self, *args, **kwargs):
#        many = kwargs.pop('many', True)
#        super(RaidSerializer, self).__init__(many=many, *args, **kwargs)
#
#    time_start = serializers.DateTimeField(format="%H:%M:%S")
#    time_battle = serializers.DateTimeField(format="%H:%M:%S")
#    time_end = serializers.DateTimeField(format="%H:%M:%S")
#
#    class Meta:
#        model = Raid
#        fields = '__all__'
#
#
#class PointOfInterestSerializer(serializers.ModelSerializer):
#
#    def __init__(self, *args, **kwargs):
#        many = kwargs.pop('many', True)
#        super(PointOfInterestSerializer, self).__init__(many=many, *args, **kwargs)
#
#    # custom field to fetch raids for our points of interest.
#    raid = serializers.SerializerMethodField()
#
#    def get_raid(self, poi : PointOfInterest):
#        # Queries are expensive.
#        # We only want to check point of interests for raids, which are gyms and have been updated in the past 2 hours.
#        time_threshold = datetime.datetime.now(poi.last_updated.tzinfo) - datetime.timedelta(hours=2)
#        if poi.type == 'gym' and poi.last_updated > time_threshold:
#            raid = Raid.objects.filter(gym__poi_id=poi.poi_id).first()
#            # Serializing is expensive, only do it if there is a raid.
#            if raid:
#                return RaidSerializer(raid).data
#        return None
#
#    class Meta:
#        model = PointOfInterest
#        fields = '__all__'
#
#
#class QuestSerializer(serializers.ModelSerializer):
#
#    def __init__(self, *args, **kwargs):
#        many = kwargs.pop('many', True)
#        super(QuestSerializer, self).__init__(many=many, *args, **kwargs)
#
#    class Meta:
#        model = Quest
#        fields = '__all__'
#
#
#class MapperSerializer(serializers.ModelSerializer):
#
#    def __init__(self, *args, **kwargs):
#        many = kwargs.pop('many', True)
#        super(MapperSerializer, self).__init__(many=many, *args, **kwargs)
#
#    class Meta:
#        model = Mapper
#        fields = '__all__'
#
#
#class PokeStopLureSerializer(serializers.ModelSerializer):
#
#    class Meta:
#        model = PokeStopLure
#        fields = '__all__'
#
#
#class GymPokemonSerializer(serializers.ModelSerializer):
#
#    class Meta:
#        model = GymPokemon
#        fields = '__all__'
#
#
#class GymStatusSerializer(serializers.ModelSerializer):
#
#    class Meta:
#        model = GymStatus
#        fields = '__all__'
#
#
#class RealDeviceMapBlackHoleSerializer(serializers.Serializer):
#    status = serializers.CharField
#
#    def save(self, **kwargs):
#        status = 'ok'
#