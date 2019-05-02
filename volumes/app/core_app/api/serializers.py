from rest_framework import serializers
from scannerdb.monocle import *
from core_app.models import Pokedex
import json


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class QuestSerializer(DynamicFieldsModelSerializer):
    quest_reward = serializers.SerializerMethodField()

    def get_quest_reward(self, quest: TrsQuest):
        quest_reward = quest.quest_reward
        quest_reward = quest_reward.replace('\'', '"').replace('False', 'false')
        quest_reward = json.loads(quest_reward)
        encounter = quest_reward[0]['pokemon_encounter']
        pokemon_id = encounter['pokemon_id']
        if pokemon_id != 0:
            pokemon = Pokedex.objects.get(pokemon_id=pokemon_id)
            quest_reward[0]['pokemon_encounter']['en'] = pokemon.name_en
            quest_reward[0]['pokemon_encounter']['ger'] = pokemon.name_ger
        return json.dumps(quest_reward)

    class Meta:
        model = TrsQuest
        fields = '__all__'

class PokestopSerializer(DynamicFieldsModelSerializer):

    #custom field to fetch quests
    quest = serializers.SerializerMethodField()

    def get_quest(self, poi : Pokestops):
        quest = TrsQuest.objects.filter(guid=poi.external_id).first()
        if quest:
            return QuestSerializer(quest, fields=('quest_reward', 'quest_task')).data
        return None

    class Meta:
        model = Pokestops
        fields = '__all__'


class RaidSerializer(DynamicFieldsModelSerializer):
    #time_spawn = serializers.DateTimeField(format="%H:%M:%S")
    #time_battle = serializers.DateTimeField(format="%H:%M:%S")
    #time_end = serializers.DateTimeField(format="%H:%M:%S")
    class Meta:
        model = Raids
        fields = '__all__'

class FortSightingSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = FortSightings
        fields = '__all__'


class GymSerializer(DynamicFieldsModelSerializer):

    # custom field to fetch raids for our points of interest.
    info = serializers.SerializerMethodField()
    raid = serializers.SerializerMethodField()

    def get_raid(self, poi : Forts):
        raid = Raids.objects.get(fort__external_id=poi.external_id)
        # Serializing is expensive, only do it if there is a raid.
        if raid:
            return RaidSerializer(raid).data
        return None

    def get_info(self, poi: Forts):
        fort_sighting = FortSightings.objects.get(fort__external_id=poi.external_id)
        if fort_sighting:
            return FortSightingSerializer(fort_sighting,fields=('team', 'slots_available')).data
        return None


    class Meta:
        model = Forts
        fields = '__all__'


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