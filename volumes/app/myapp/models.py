import json
import re

from django.db.models import *
from django.core.exceptions import ValidationError
from django.utils import timezone
from rest_framework.authtoken.models import Token


class PokemonType(Model):
    name = TextField()
    name_german = TextField(null=True)
    color = CharField(max_length=6)
    damage = ManyToManyField('self')

    def clean(self):
        if len(self.color) < 6:
            raise ValidationError('color is no valid rgb hex')


class PokemonMove(Model):
    name = TextField()
    type = ForeignKey(PokemonType, on_delete=CASCADE)
    damage = SmallIntegerField()
    energy = SmallIntegerField()
    dps = SmallIntegerField()
    legacy = BooleanField(default=False)


class Pokemon(Model):
    number = IntegerField(primary_key=True)
    name_german = TextField(db_index=True, null=True)
    name_english = TextField(db_index=True, null=True)
    name_french = TextField(null=True)
    flee_rate = FloatField(null=True)
    capture_rate = FloatField(null=True)
    max_cp = IntegerField(null=True)
    rarity = TextField(default="normal", null=True)
    egg_distance = IntegerField(null=True)
    types = ManyToManyField(PokemonType)
    moves = ManyToManyField(PokemonMove)

    class Meta:
        # Sort the Data by this:
        ordering = ('number',)

    def __str__(self):
        if self.name_german is not None:
            name = self.name_german
        else:
            name = str(self.number)
        return str(self.number) + ' - ' + name


class PokemonSpawn(Model):
    encounter_id = CharField(max_length=200, default=None, null=True, blank=True)
    report_time = DateTimeField(default=timezone.now)
    pokemon_object = ForeignKey(Pokemon, on_delete=CASCADE)
    latitude = FloatField()
    longitude = FloatField()
    disappear_time = DateTimeField(db_index=True)
    individual_attack = SmallIntegerField(default=None, null=True, blank=True)
    individual_defense = SmallIntegerField(default=None, null=True, blank=True)
    individual_stamina = SmallIntegerField(default=None, null=True, blank=True)
    moves = ManyToManyField(PokemonMove, default=None, blank=True)
    cp = SmallIntegerField(default=None, null=True, blank=True)
    cp_multiplier = FloatField(default=None, null=True, blank=True)
    weight = FloatField(default=None, null=True, blank=True)
    height = FloatField(default=None, null=True, blank=True)
    gender = SmallIntegerField(default=None, null=True, blank=True)
    costume = SmallIntegerField(default=None, null=True, blank=True)
    form = SmallIntegerField(default=None, null=True, blank=True)
    weather_boosted_condition = SmallIntegerField(default=None, null=True, blank=True)
    last_modified = DateTimeField(default=timezone.now, null=True, db_index=True, blank=True)
    level = IntegerField(default=None, null=True, blank=True)
    _individual_percentage = FloatField(default=None, null=True, blank=True)
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)

    @property
    def individual_percentage(self):
        if self._individual_percentage:
            return self._individual_percentage
        elif self.individual_attack or self.individual_defense or self.individual_stamina:
            iv_att = self.individual_attack if self.individual_attack else 0
            iv_stam = self.individual_stamina if self.individual_stamina else 0
            iv_def = self.individual_defense if self.individual_defense else 0
            self._individual_percentage = (iv_att + iv_stam + iv_def)/3
            return self._individual_percentage
        else:
            return None

    @individual_percentage.setter
    def individual_percentage(self, value):
        self._individual_percentage = value


class PointOfInterest(Model):
    """Model for storing pokestops, gyms and stuff in the future"""
    report_time = DateTimeField(default=timezone.now)
    poi_id = TextField(default=None, null=True)
    enabled = BooleanField(default=True)
    longitude = FloatField()
    latitude = FloatField()
    last_modified = BigIntegerField(default=None, null=True)
    last_updated = DateTimeField(default=timezone.now, null=True)
    name = TextField(default=None, null=True)
    description = TextField(default=None, null=True)
    image_url = URLField(default=None, null=True)
    type = TextField()
    active_fort_modifier = SmallIntegerField(default=None, null=True)  # Don't know what dis does
    park = BooleanField(default=False)
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)

    def __repr__(self):
        return self.name

    def __str__(self):
        if self.name is not None:
            name = self.name
        else:
            name = str(self.id)
        return ' '.join([self.type, name])


class PokeStopLure(Model):
    report_time = DateTimeField(default=timezone.now)
    point_of_interest = ForeignKey(PointOfInterest, on_delete=CASCADE)
    expiration_time = DateTimeField()


class Raid(Model):
    gym = ForeignKey(PointOfInterest, on_delete=CASCADE)
    level = IntegerField(db_index=True)
    spawn = DateTimeField(db_index=True)
    start = DateTimeField(db_index=True)
    end = DateTimeField(db_index=True)
    pokemon = ForeignKey(Pokemon, default=None, null=True, on_delete=CASCADE)
    cp = IntegerField(default=None, null=True)
    moves = ManyToManyField(PokemonMove, default=None)
    last_scanned = DateTimeField(default=timezone.now, db_index=True)


class GymPokemon(Model):
    report_time = DateTimeField(default=timezone.now)
    pokemon_nr = ForeignKey(Pokemon, on_delete=CASCADE)
    pokemon_uid = BigIntegerField(default=None, null=True)
    base_cp = SmallIntegerField(default=None, null=True)
    num_upgrades = SmallIntegerField(default=None, null=True)
    moves = ManyToManyField(PokemonMove, default=None)
    height = FloatField(default=None, null=True)
    weight = FloatField(default=None, null=True)
    stamina = SmallIntegerField(default=None, null=True)
    stamina_max = SmallIntegerField(default=None, null=True)
    cp_multiplier = FloatField(default=None, null=True)
    additional_cp_multiplier = FloatField(default=None, null=True)
    iv_defense = SmallIntegerField(default=None, null=True)
    iv_stamina = SmallIntegerField(default=None, null=True)
    iv_attack = SmallIntegerField(default=None, null=True)
    costume = SmallIntegerField(default=None, null=True)
    form = SmallIntegerField(default=None, null=True)
    shiny = SmallIntegerField(default=None, null=True)
    last_seen = DateTimeField(default=timezone.now)


class GymStatus(Model):
    report_time = DateTimeField(default=timezone.now)
    current_team_id = IntegerField(default=0)
    interactable = BooleanField(default=True)
    occupied_since = DateTimeField(default=timezone.now)
    last_modified = DateTimeField(default=timezone.now)
    guard_pokemon_id = ForeignKey(Pokemon, on_delete=CASCADE)
    total_cp = IntegerField(default=None, null=True)
    slots_available = IntegerField(default=None)
    slots_available.null = True
    lowest_pokemon_motivation = FloatField(default=None)
    lowest_pokemon_motivation.null = True
    gym_pokemon = ManyToManyField(GymPokemon, through='GymMemberRelation')


class GymMemberRelation(Model):
    gym_status = ForeignKey(GymStatus, on_delete=CASCADE)
    gym_pokemon = ForeignKey(GymPokemon, on_delete=CASCADE)
    current_cp = IntegerField(default=None, null=True)
    current_stamina = IntegerField(default=None, null=True)


class SpawnPoint(Model):
    longitude = FloatField()
    latitude = FloatField()
    spawn_point_id = IntegerField(default=None, null=True, blank=True)
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)


class Quest(Model):
    quest_id = CharField(max_length=128, primary_key=True)
    quest_type = BigIntegerField()
    pokestop_id = CharField(max_length=128)
    quest_timestamp = BigIntegerField()
    quest_conditions = TextField()
    quest_rewards = TextField()
    quest_template = CharField(max_length=128)
    quest_pokemon_id = SmallIntegerField(default=None, null=True, blank=True)
    quest_reward_type = CharField(max_length=128, default=None, null=True, blank=True)
    quest_item_id = IntegerField(default=None, null=True, blank=True)
    quest_item_amount = SmallIntegerField(default=None, null=True, blank=True)
    target = SmallIntegerField(default=None, null=True, blank=True)
    cell_id = BigIntegerField()
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.quest_reward_type is None:
            data = json.loads(self.quest_rewards)
            if 'pokemon_encounter' in data:
                self.quest_reward_type = 'pokemon_encounter'
                self.quest_pokemon_id = data['pokemon_encounter']['pokemon_id']
            elif'item' in data:
                self.quest_reward_type = 'item'
                self.quest_item_id = data['item']['item']
                self.quest_item_amount = data['item']['amount']
            data = json.loads(self.quest_conditions)
            if 'goal' in 'data':
                if 'condition' in data['goal']:
                    self.target = data['goal']['condition']['type']
        super().save(*args, **kwargs)


class Mapper(Model):
    uuid = UUIDField(db_index=True)
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)
    name = CharField(max_length=128, default=None, null=True)
    longitude = FloatField(default=None, null=True)
    latitude = FloatField(default=None, null=True)
    trainerlevel = SmallIntegerField(default=None, null=True)


class AllowedDiscordServer(Model):
    server_id = CharField(db_index=True, max_length=128)
    name = CharField(max_length=128, default=None, blank=True, null=True)
