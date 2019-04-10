# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Common(models.Model):
    key = models.CharField(max_length=32)
    val = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        
        db_table = 'common'


class FortSightings(models.Model):
    id = models.BigAutoField(primary_key=True)
    fort = models.ForeignKey('Forts', models.DO_NOTHING, unique=True, blank=True, null=True)
    last_modified = models.IntegerField(blank=True, null=True)
    team = models.PositiveIntegerField(blank=True, null=True)
    guard_pokemon_id = models.SmallIntegerField(blank=True, null=True)
    guard_pokemon_form = models.SmallIntegerField(blank=True, null=True)
    slots_available = models.SmallIntegerField(blank=True, null=True)
    is_in_battle = models.IntegerField(blank=True, null=True)
    updated = models.IntegerField(blank=True, null=True)
    is_ex_raid_eligible = models.IntegerField(blank=True, null=True)

    class Meta:
        
        db_table = 'fort_sightings'
        unique_together = (('fort', 'last_modified'),)


class Forts(models.Model):
    external_id = models.CharField(unique=True, max_length=35, blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)
    name = models.CharField(max_length=128, blank=True, null=True)
    url = models.CharField(max_length=200, blank=True, null=True)
    sponsor = models.SmallIntegerField(blank=True, null=True)
    weather_cell_id = models.BigIntegerField(blank=True, null=True)
    park = models.CharField(max_length=128, blank=True, null=True)
    parkid = models.BigIntegerField(blank=True, null=True)
    edited_by = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'forts'

    def __str__(self):
        return f'{self.name}'


class GymDefenders(models.Model):
    id = models.BigAutoField(primary_key=True)
    fort = models.ForeignKey(Forts, models.DO_NOTHING, null=True)
    external_id = models.BigIntegerField()
    pokemon_id = models.SmallIntegerField(blank=True, null=True)
    form = models.SmallIntegerField(blank=True, null=True)
    team = models.PositiveIntegerField(blank=True, null=True)
    owner_name = models.CharField(max_length=128, blank=True, null=True)
    nickname = models.CharField(max_length=128, blank=True, null=True)
    cp = models.IntegerField(blank=True, null=True)
    stamina = models.IntegerField(blank=True, null=True)
    stamina_max = models.IntegerField(blank=True, null=True)
    atk_iv = models.SmallIntegerField(blank=True, null=True)
    def_iv = models.SmallIntegerField(blank=True, null=True)
    sta_iv = models.SmallIntegerField(blank=True, null=True)
    move_1 = models.SmallIntegerField(blank=True, null=True)
    move_2 = models.SmallIntegerField(blank=True, null=True)
    last_modified = models.IntegerField(blank=True, null=True)
    battles_attacked = models.IntegerField(blank=True, null=True)
    battles_defended = models.IntegerField(blank=True, null=True)
    num_upgrades = models.SmallIntegerField(blank=True, null=True)
    created = models.IntegerField(blank=True, null=True)

    class Meta:
        
        db_table = 'gym_defenders'


class IngressPortals(models.Model):
    external_id = models.CharField(unique=True, max_length=35, blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)
    name = models.CharField(max_length=128, blank=True, null=True)
    url = models.CharField(max_length=200, blank=True, null=True)
    updated = models.BigIntegerField()
    imported = models.BigIntegerField(blank=True, null=True)
    checked = models.IntegerField(blank=True, null=True)

    class Meta:
        
        db_table = 'ingress_portals'


class MysterySightings(models.Model):
    id = models.BigAutoField(primary_key=True)
    pokemon_id = models.SmallIntegerField(blank=True, null=True)
    spawn_id = models.BigIntegerField(blank=True, null=True)
    encounter_id = models.BigIntegerField(blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)
    first_seen = models.IntegerField(blank=True, null=True)
    first_seconds = models.SmallIntegerField(blank=True, null=True)
    last_seconds = models.SmallIntegerField(blank=True, null=True)
    seen_range = models.SmallIntegerField(blank=True, null=True)
    atk_iv = models.PositiveIntegerField(blank=True, null=True)
    def_iv = models.PositiveIntegerField(blank=True, null=True)
    sta_iv = models.PositiveIntegerField(blank=True, null=True)
    move_1 = models.SmallIntegerField(blank=True, null=True)
    move_2 = models.SmallIntegerField(blank=True, null=True)
    gender = models.SmallIntegerField(blank=True, null=True)
    form = models.SmallIntegerField(blank=True, null=True)
    cp = models.SmallIntegerField(blank=True, null=True)
    level = models.SmallIntegerField(blank=True, null=True)
    weather_boosted_condition = models.SmallIntegerField(blank=True, null=True)
    weather_cell_id = models.BigIntegerField(blank=True, null=True)

    class Meta:
        
        db_table = 'mystery_sightings'
        unique_together = (('encounter_id', 'spawn_id'),)


class Nests(models.Model):
    nest_id = models.BigAutoField(primary_key=True)
    lat = models.FloatField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)
    pokemon_id = models.IntegerField(blank=True, null=True)
    updated = models.BigIntegerField(blank=True, null=True)
    type = models.IntegerField()
    nest_submitted_by = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        
        db_table = 'nests'


class Payments(models.Model):
    selly_id = models.CharField(max_length=100)
    product_id = models.IntegerField()
    email = models.CharField(max_length=250)
    value = models.IntegerField()
    quantity = models.IntegerField()
    timestamp = models.IntegerField()

    class Meta:
        
        db_table = 'payments'


class Pokestops(models.Model):
    external_id = models.CharField(unique=True, max_length=35, blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)
    name = models.CharField(max_length=128, blank=True, null=True)
    url = models.CharField(max_length=200, blank=True, null=True)
    updated = models.IntegerField(blank=True, null=True)
    quest_id = models.SmallIntegerField(blank=True, null=True)
    reward_id = models.SmallIntegerField(blank=True, null=True)
    deployer = models.CharField(max_length=40, blank=True, null=True)
    lure_start = models.CharField(max_length=40, blank=True, null=True)
    expires = models.IntegerField(blank=True, null=True)
    quest_submitted_by = models.CharField(max_length=200, blank=True, null=True)
    edited_by = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'pokestops'

    def __str__(self):
        return f'{self.name}'


class Raids(models.Model):
    external_id = models.BigIntegerField(unique=True, blank=True, null=True)
    fort = models.ForeignKey(Forts, models.DO_NOTHING, blank=True, null=True)
    level = models.PositiveIntegerField(blank=True, null=True)
    pokemon_id = models.SmallIntegerField(blank=True, null=True)
    move_1 = models.SmallIntegerField(blank=True, null=True)
    move_2 = models.SmallIntegerField(blank=True, null=True)
    time_spawn = models.IntegerField(blank=True, null=True)
    time_battle = models.IntegerField(blank=True, null=True)
    time_end = models.IntegerField(blank=True, null=True)
    last_updated = models.IntegerField(blank=True, null=True)
    cp = models.IntegerField(blank=True, null=True)
    submitted_by = models.CharField(max_length=200, blank=True, null=True)
    form = models.SmallIntegerField(blank=True, null=True)
    is_exclusive = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'raids'
    def __str__(self):
        return f'{self.fort.name}: level {self.level} : pokemon_id {self.pokemon_id}'


class Sightings(models.Model):
    id = models.BigAutoField(primary_key=True)
    pokemon_id = models.SmallIntegerField(blank=True, null=True)
    spawn_id = models.BigIntegerField(blank=True, null=True)
    expire_timestamp = models.IntegerField(blank=True, null=True)
    encounter_id = models.BigIntegerField(unique=True, blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)
    atk_iv = models.PositiveIntegerField(blank=True, null=True)
    def_iv = models.PositiveIntegerField(blank=True, null=True)
    sta_iv = models.PositiveIntegerField(blank=True, null=True)
    move_1 = models.SmallIntegerField(blank=True, null=True)
    move_2 = models.SmallIntegerField(blank=True, null=True)
    gender = models.SmallIntegerField(blank=True, null=True)
    form = models.SmallIntegerField(blank=True, null=True)
    cp = models.SmallIntegerField(blank=True, null=True)
    level = models.SmallIntegerField(blank=True, null=True)
    updated = models.IntegerField(blank=True, null=True)
    weather_boosted_condition = models.SmallIntegerField(blank=True, null=True)
    weather_cell_id = models.BigIntegerField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    costume = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        
        db_table = 'sightings'


class SightingsTemp(models.Model):
    id = models.BigAutoField(primary_key=True)
    pokemon_id = models.SmallIntegerField(blank=True, null=True)
    spawn_id = models.BigIntegerField(blank=True, null=True)
    expire_timestamp = models.IntegerField(blank=True, null=True)
    encounter_id = models.BigIntegerField(unique=True, blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)
    atk_iv = models.PositiveIntegerField(blank=True, null=True)
    def_iv = models.PositiveIntegerField(blank=True, null=True)
    sta_iv = models.PositiveIntegerField(blank=True, null=True)
    move_1 = models.SmallIntegerField(blank=True, null=True)
    move_2 = models.SmallIntegerField(blank=True, null=True)
    gender = models.SmallIntegerField(blank=True, null=True)
    form = models.SmallIntegerField(blank=True, null=True)
    cp = models.SmallIntegerField(blank=True, null=True)
    level = models.SmallIntegerField(blank=True, null=True)
    updated = models.IntegerField(blank=True, null=True)
    weather_boosted_condition = models.SmallIntegerField(blank=True, null=True)
    weather_cell_id = models.BigIntegerField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)

    class Meta:
        
        db_table = 'sightings_temp'


class Spawnpoints(models.Model):
    spawn_id = models.BigIntegerField(unique=True, blank=True, null=True)
    despawn_time = models.SmallIntegerField(blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)
    updated = models.IntegerField(blank=True, null=True)
    duration = models.PositiveIntegerField(blank=True, null=True)
    failures = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        
        db_table = 'spawnpoints'


class TrsQuest(models.Model):
    guid = models.CharField(db_column='GUID', primary_key=True, max_length=50)  # Field name made lowercase.
    quest_type = models.IntegerField()
    quest_timestamp = models.IntegerField()
    quest_stardust = models.SmallIntegerField()
    quest_pokemon_id = models.SmallIntegerField()
    quest_reward_type = models.SmallIntegerField()
    quest_item_id = models.SmallIntegerField()
    quest_item_amount = models.IntegerField()
    quest_target = models.IntegerField()
    quest_condition = models.CharField(max_length=500, blank=True, null=True)
    quest_reward = models.CharField(max_length=1000, blank=True, null=True)
    quest_task = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        
        db_table = 'trs_quest'


class TrsSpawn(models.Model):
    spawnpoint = models.CharField(unique=True, max_length=16)
    latitude = models.FloatField()
    longitude = models.FloatField()
    spawndef = models.IntegerField()
    earliest_unseen = models.IntegerField()
    last_scanned = models.DateTimeField(blank=True, null=True)
    first_detection = models.DateTimeField()
    last_non_scanned = models.DateTimeField(blank=True, null=True)
    calc_endminsec = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        
        db_table = 'trs_spawn'


class TrsSpawnsightings(models.Model):
    encounter_id = models.BigIntegerField()
    spawnpoint_id = models.BigIntegerField()
    scan_time = models.DateTimeField()
    tth_secs = models.IntegerField(blank=True, null=True)

    class Meta:
        
        db_table = 'trs_spawnsightings'


class TrsStatus(models.Model):
    origin = models.CharField(primary_key=True, max_length=50)
    currentpos = models.CharField(db_column='currentPos', max_length=50, blank=True, null=True)  # Field name made lowercase.
    lastpos = models.CharField(db_column='lastPos', max_length=50, blank=True, null=True)  # Field name made lowercase.
    routepos = models.IntegerField(db_column='routePos', blank=True, null=True)  # Field name made lowercase.
    routemax = models.IntegerField(db_column='routeMax', blank=True, null=True)  # Field name made lowercase.
    routemanager = models.CharField(max_length=255, blank=True, null=True)
    rebootcounter = models.IntegerField(db_column='rebootCounter', blank=True, null=True)  # Field name made lowercase.
    lastprotodatetime = models.CharField(db_column='lastProtoDateTime', max_length=50, blank=True, null=True)  # Field name made lowercase.
    lastpogorestart = models.CharField(db_column='lastPogoRestart', max_length=50, blank=True, null=True)  # Field name made lowercase.
    init = models.TextField(blank=True, null=True)
    rebootingoption = models.TextField(db_column='rebootingOption', blank=True, null=True)  # Field name made lowercase.
    restartcounter = models.TextField(db_column='restartCounter', blank=True, null=True)  # Field name made lowercase.
    lastpogoreboot = models.CharField(db_column='lastPogoReboot', max_length=50, blank=True, null=True)  # Field name made lowercase.
    globalrebootcount = models.IntegerField(blank=True, null=True)
    globalrestartcount = models.IntegerField(blank=True, null=True)

    class Meta:
        
        db_table = 'trs_status'


class TrsUsage(models.Model):
    usage_id = models.AutoField(primary_key=True)
    instance = models.CharField(max_length=100, blank=True, null=True)
    cpu = models.FloatField(blank=True, null=True)
    memory = models.FloatField(blank=True, null=True)
    garbage = models.IntegerField(blank=True, null=True)
    timestamp = models.IntegerField(blank=True, null=True)

    class Meta:
        
        db_table = 'trs_usage'


class Trshash(models.Model):
    hashid = models.AutoField(primary_key=True)
    hash = models.CharField(max_length=255)
    type = models.CharField(max_length=10)
    id = models.CharField(max_length=255)
    count = models.IntegerField()
    modify = models.DateTimeField()

    class Meta:
        
        db_table = 'trshash'


class Users(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.CharField(max_length=250)
    password = models.CharField(max_length=250, blank=True, null=True)
    temp_password = models.CharField(max_length=250, blank=True, null=True)
    expire_timestamp = models.IntegerField()
    session_id = models.CharField(max_length=100, blank=True, null=True)
    login_system = models.CharField(max_length=40)
    access_level = models.IntegerField(blank=True, null=True)

    class Meta:
        
        db_table = 'users'


class Weather(models.Model):
    s2_cell_id = models.BigIntegerField(unique=True, blank=True, null=True)
    condition = models.PositiveIntegerField(blank=True, null=True)
    alert_severity = models.PositiveIntegerField(blank=True, null=True)
    warn = models.IntegerField(blank=True, null=True)
    day = models.PositiveIntegerField(blank=True, null=True)
    updated = models.IntegerField(blank=True, null=True)

    class Meta:
        
        db_table = 'weather'

class AllowedDiscordServer(models.Model):
    server_id = models.CharField(db_index=True, max_length=128)
    name = models.CharField(max_length=128, default=None, blank=True, null=True)
