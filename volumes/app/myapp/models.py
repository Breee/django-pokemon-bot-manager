from django.db.models import *
from django.utils import timezone
from rest_framework.authtoken.models import Token


class PokemonType(Model):
    name = TextField()
    color = CharField(max_length=3)
    damage = SmallIntegerField()
    energy = SmallIntegerField()
    dps = SmallIntegerField()
    legacy = BooleanField(default=False)


class PokemonMove(Model):
    name = TextField()
    type = ForeignKey(PokemonType, on_delete=CASCADE)


class Pokemon(Model):
    poke_nr = IntegerField(primary_key=True)
    poke_name_ger = CharField(max_length=30, db_index=True)
    poke_name_eng = CharField(max_length=30)
    types = ManyToManyField(PokemonType)

    class Meta:
        # Sort the Data by this:
        ordering = ('poke_nr',)

    def __str__(self):
        return str(self.poke_nr) + ' - ' + self.poke_name_ger


class PokemonSpawn(Model):
    report_time = DateTimeField(default=timezone.now)
    poke_nr = ForeignKey(Pokemon, on_delete=CASCADE)
    latitude = FloatField()
    longitude = FloatField()
    disappear_time = DateTimeField(db_index=True)
    individual_attack = SmallIntegerField(default=None, null=True)
    individual_defense = SmallIntegerField(default=None, null=True)
    individual_stamina = SmallIntegerField(default=None, null=True)
    move_1 = ForeignKey(PokemonMove, default=None, null=True, on_delete=CASCADE)
    move_2 = ForeignKey(PokemonMove, default=None, null=True, on_delete=CASCADE)
    cp = SmallIntegerField(default=None, null=True)
    cp_multiplier = FloatField(default=None, null=True)
    weight = FloatField(default=None, null=True)
    height = FloatField(default=None, null=True)
    gender = SmallIntegerField(default=None, null=True)
    costume = SmallIntegerField(default=None, null=True)
    form = SmallIntegerField(default=None, null=True)
    weather_boosted_condition = SmallIntegerField(default=None, null=True)
    last_modified = DateTimeField(default=timezone.now, null=True, db_index=True)
    level = IntegerField(default=None, null=True)
    _individual_percentage = FloatField(default=None, null=True)

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
    id = TextField(default=None, null=True)
    enabled = BooleanField(default=None, null=True)
    longitude = FloatField()
    latitude = FloatField()
    last_modified = DateTimeField(default=None, null=True)
    last_updated = DateTimeField(default=timezone.now, null=True)
    name = TextField(default=None, null=True)
    description = TextField(default=None, null=True)
    image_url = URLField(default=None, null=True)
    type = TextField()
    active_fort_modifier = SmallIntegerField(default=None, null=True)  # Don't know what dis does
    park = BooleanField(default=False)


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
    move_1 = ForeignKey(PokemonMove, default=None, null=True, on_delete=CASCADE)
    move_2 = ForeignKey(PokemonMove, default=None, null=True, on_delete=CASCADE)
    last_scanned = DateTimeField(default=timezone.now, db_index=True)


class GymMemberRelation(Model):
    current_cp = IntegerField(default=None, null=True)
    current_stamina = IntegerField(default=None, null=True)


class GymPokemon(Model):
    report_time = DateTimeField(default=timezone.now)
    pokemon_nr = ForeignKey(Pokemon, on_delete=CASCADE)
    pokemon_uid = BigIntegerField(default=None, null=True)
    base_cp = SmallIntegerField(default=None, null=True)
    num_upgrades = SmallIntegerField(default=None, null=True)
    move_1 = ForeignKey(PokemonMove, default=None, null=True, on_delete=CASCADE)
    move_2 = ForeignKey(PokemonMove, default=None, null=True, on_delete=CASCADE)
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
    gym_pokemon = ManyToManyField(GymPokemon, through=GymMemberRelation)
