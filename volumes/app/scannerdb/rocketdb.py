# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
import django.db.models.options as options
options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('in_db',)
from django.db import models


class Gomap(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()

    class Meta:
        db_table = 'gomap'
        in_db = 'rocketdb'
        app_label = 'scannerdb'


class Gym(models.Model):
    gym_id = models.CharField(primary_key=True, max_length=50)
    team_id = models.SmallIntegerField()
    guard_pokemon_id = models.SmallIntegerField()
    slots_available = models.SmallIntegerField()
    enabled = models.IntegerField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    total_cp = models.SmallIntegerField()
    is_in_battle = models.IntegerField()
    gender = models.SmallIntegerField(blank=True, null=True)
    form = models.SmallIntegerField(blank=True, null=True)
    costume = models.SmallIntegerField(blank=True, null=True)
    weather_boosted_condition = models.SmallIntegerField(blank=True, null=True)
    shiny = models.IntegerField(blank=True, null=True)
    last_modified = models.DateTimeField()
    last_scanned = models.DateTimeField()

    class Meta:
        db_table = 'gym'
        in_db = 'rocketdb'
        app_label = 'scannerdb'


class Gymdetails(models.Model):
    gym_id = models.CharField(primary_key=True, max_length=50)
    name = models.CharField(max_length=191)
    description = models.TextField(blank=True, null=True)
    url = models.CharField(max_length=191)
    last_scanned = models.DateTimeField()

    class Meta:
        
        db_table = 'gymdetails'
        in_db = 'rocketdb'
        app_label = 'scannerdb'


class Gymmember(models.Model):
    gym_id = models.CharField(max_length=191)
    pokemon_uid = models.BigIntegerField()
    last_scanned = models.DateTimeField()
    deployment_time = models.DateTimeField()
    cp_decayed = models.SmallIntegerField()

    class Meta:
        
        db_table = 'gymmember'
        in_db = 'rocketdb'
        app_label = 'scannerdb'


class Gympokemon(models.Model):
    pokemon_uid = models.BigIntegerField(primary_key=True)
    pokemon_id = models.SmallIntegerField()
    cp = models.SmallIntegerField()
    trainer_name = models.CharField(max_length=191)
    num_upgrades = models.SmallIntegerField(blank=True, null=True)
    move_1 = models.SmallIntegerField(blank=True, null=True)
    move_2 = models.SmallIntegerField(blank=True, null=True)
    height = models.FloatField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    stamina = models.SmallIntegerField(blank=True, null=True)
    stamina_max = models.SmallIntegerField(blank=True, null=True)
    cp_multiplier = models.FloatField(blank=True, null=True)
    additional_cp_multiplier = models.FloatField(blank=True, null=True)
    iv_defense = models.SmallIntegerField(blank=True, null=True)
    iv_stamina = models.SmallIntegerField(blank=True, null=True)
    iv_attack = models.SmallIntegerField(blank=True, null=True)
    gender = models.SmallIntegerField(blank=True, null=True)
    form = models.SmallIntegerField(blank=True, null=True)
    costume = models.SmallIntegerField(blank=True, null=True)
    weather_boosted_condition = models.SmallIntegerField(blank=True, null=True)
    shiny = models.IntegerField(blank=True, null=True)
    last_seen = models.DateTimeField()

    class Meta:
        
        db_table = 'gympokemon'
        in_db = 'rocketdb'
        app_label = 'scannerdb'


class Hashkeys(models.Model):
    key = models.CharField(primary_key=True, max_length=20)
    maximum = models.SmallIntegerField()
    remaining = models.SmallIntegerField()
    peak = models.SmallIntegerField()
    expires = models.DateTimeField(blank=True, null=True)
    last_updated = models.DateTimeField()

    class Meta:
        
        db_table = 'hashkeys'
        in_db = 'rocketdb'
        app_label = 'scannerdb'


class Locationaltitude(models.Model):
    cellid = models.BigIntegerField(primary_key=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    last_modified = models.DateTimeField(blank=True, null=True)
    altitude = models.FloatField()

    class Meta:
        
        db_table = 'locationaltitude'
        in_db = 'rocketdb'
        app_label = 'scannerdb'


class Mainworker(models.Model):
    worker_name = models.CharField(primary_key=True, max_length=50)
    message = models.TextField(blank=True, null=True)
    method = models.CharField(max_length=50)
    last_modified = models.DateTimeField()
    accounts_working = models.IntegerField()
    accounts_captcha = models.IntegerField()
    accounts_failed = models.IntegerField()
    success = models.IntegerField()
    fail = models.IntegerField()
    empty = models.IntegerField()
    skip = models.IntegerField()
    captcha = models.IntegerField()
    start = models.IntegerField()
    elapsed = models.IntegerField()

    class Meta:
        
        db_table = 'mainworker'
        in_db = 'rocketdb'
        app_label = 'scannerdb'


class Playerlocale(models.Model):
    location = models.CharField(primary_key=True, max_length=50)
    country = models.CharField(max_length=2)
    language = models.CharField(max_length=2)
    timezone = models.CharField(max_length=50)

    class Meta:
        
        db_table = 'playerlocale'
        in_db = 'rocketdb'
        app_label = 'scannerdb'


class Pokemon(models.Model):
    encounter_id = models.BigIntegerField(primary_key=True)
    spawnpoint_id = models.BigIntegerField()
    pokemon_id = models.SmallIntegerField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    disappear_time = models.DateTimeField()
    individual_attack = models.SmallIntegerField(blank=True, null=True)
    individual_defense = models.SmallIntegerField(blank=True, null=True)
    individual_stamina = models.SmallIntegerField(blank=True, null=True)
    move_1 = models.SmallIntegerField(blank=True, null=True)
    move_2 = models.SmallIntegerField(blank=True, null=True)
    cp = models.SmallIntegerField(blank=True, null=True)
    cp_multiplier = models.FloatField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    height = models.FloatField(blank=True, null=True)
    gender = models.SmallIntegerField(blank=True, null=True)
    form = models.SmallIntegerField(blank=True, null=True)
    costume = models.SmallIntegerField(blank=True, null=True)
    catch_prob_1 = models.FloatField(blank=True, null=True)
    catch_prob_2 = models.FloatField(blank=True, null=True)
    catch_prob_3 = models.FloatField(blank=True, null=True)
    rating_attack = models.CharField(max_length=2, blank=True, null=True)
    rating_defense = models.CharField(max_length=2, blank=True, null=True)
    weather_boosted_condition = models.SmallIntegerField(blank=True, null=True)
    last_modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        
        db_table = 'pokemon'
        in_db = 'rocketdb'
        app_label = 'scannerdb'


class Pokestop(models.Model):
    pokestop_id = models.CharField(primary_key=True, max_length=50)
    enabled = models.IntegerField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    last_modified = models.DateTimeField(blank=True, null=True)
    lure_expiration = models.DateTimeField(blank=True, null=True)
    active_fort_modifier = models.SmallIntegerField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)
    name = models.CharField(max_length=250, blank=True, null=True)
    image = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        
        db_table = 'pokestop'
        in_db = 'rocketdb'
        app_label = 'scannerdb'


class Raid(models.Model):
    gym_id = models.CharField(primary_key=True, max_length=50)
    level = models.IntegerField()
    spawn = models.DateTimeField()
    start = models.DateTimeField()
    end = models.DateTimeField()
    pokemon_id = models.SmallIntegerField(blank=True, null=True)
    cp = models.IntegerField(blank=True, null=True)
    move_1 = models.SmallIntegerField(blank=True, null=True)
    move_2 = models.SmallIntegerField(blank=True, null=True)
    last_scanned = models.DateTimeField()
    form = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        db_table = 'raid'
        in_db = 'rocketdb'
        app_label = 'scannerdb'


class Scannedlocation(models.Model):
    cellid = models.BigIntegerField(primary_key=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    last_modified = models.DateTimeField(blank=True, null=True)
    done = models.IntegerField()
    band1 = models.SmallIntegerField()
    band2 = models.SmallIntegerField()
    band3 = models.SmallIntegerField()
    band4 = models.SmallIntegerField()
    band5 = models.SmallIntegerField()
    midpoint = models.SmallIntegerField()
    width = models.SmallIntegerField()

    class Meta:
        
        db_table = 'scannedlocation'
        in_db = 'rocketdb'
        app_label = 'scannerdb'


class Scanspawnpoint(models.Model):
    scannedlocation = models.ForeignKey(Scannedlocation, models.DO_NOTHING)
    spawnpoint = models.ForeignKey('Spawnpoint', models.DO_NOTHING, primary_key=True)

    class Meta:
        
        db_table = 'scanspawnpoint'
        unique_together = (('spawnpoint', 'scannedlocation'),)
        in_db = 'rocketdb'
        app_label = 'scannerdb'


class Spawnpoint(models.Model):
    id = models.BigIntegerField(primary_key=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    last_scanned = models.DateTimeField()
    kind = models.CharField(max_length=4)
    links = models.CharField(max_length=4)
    missed_count = models.IntegerField()
    latest_seen = models.SmallIntegerField()
    earliest_unseen = models.SmallIntegerField()

    class Meta:
        
        db_table = 'spawnpoint'
        in_db = 'rocketdb'
        app_label = 'scannerdb'


class Spawnpointdetectiondata(models.Model):
    encounter_id = models.BigIntegerField()
    spawnpoint_id = models.BigIntegerField()
    scan_time = models.DateTimeField()
    tth_secs = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        
        db_table = 'spawnpointdetectiondata'
        in_db = 'rocketdb'
        app_label = 'scannerdb'


class Token(models.Model):
    token = models.TextField()
    last_updated = models.DateTimeField()

    class Meta:
        
        db_table = 'token'
        in_db = 'rocketdb'
        app_label = 'scannerdb'


class Trainer(models.Model):
    name = models.CharField(primary_key=True, max_length=50)
    team = models.SmallIntegerField()
    level = models.SmallIntegerField()
    last_seen = models.DateTimeField()

    class Meta:
        
        db_table = 'trainer'
        in_db = 'rocketdb'
        app_label = 'scannerdb'


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
    quest_template = models.CharField(max_length=100, blank=True, null=True)
    quest_task = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        
        db_table = 'trs_quest'
        in_db = 'rocketdb'
        app_label = 'scannerdb'


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
        in_db = 'rocketdb'
        app_label = 'scannerdb'


class TrsSpawnsightings(models.Model):
    encounter_id = models.BigIntegerField()
    spawnpoint_id = models.BigIntegerField()
    scan_time = models.DateTimeField()
    tth_secs = models.IntegerField(blank=True, null=True)

    class Meta:
        
        db_table = 'trs_spawnsightings'
        in_db = 'rocketdb'
        app_label = 'scannerdb'


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
        in_db = 'rocketdb'
        app_label = 'scannerdb'


class Versions(models.Model):
    key = models.CharField(max_length=191)
    val = models.SmallIntegerField()

    class Meta:
        
        db_table = 'versions'
        in_db = 'rocketdb'
        app_label = 'scannerdb'


class Weather(models.Model):
    s2_cell_id = models.CharField(primary_key=True, max_length=50)
    latitude = models.FloatField()
    longitude = models.FloatField()
    cloud_level = models.SmallIntegerField(blank=True, null=True)
    rain_level = models.SmallIntegerField(blank=True, null=True)
    wind_level = models.SmallIntegerField(blank=True, null=True)
    snow_level = models.SmallIntegerField(blank=True, null=True)
    fog_level = models.SmallIntegerField(blank=True, null=True)
    wind_direction = models.SmallIntegerField(blank=True, null=True)
    gameplay_weather = models.SmallIntegerField(blank=True, null=True)
    severity = models.SmallIntegerField(blank=True, null=True)
    warn_weather = models.SmallIntegerField(blank=True, null=True)
    world_time = models.SmallIntegerField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        
        db_table = 'weather'
        in_db = 'rocketdb'
        app_label = 'scannerdb'


class Workerstatus(models.Model):
    username = models.CharField(primary_key=True, max_length=50)
    worker_name = models.CharField(max_length=50)
    success = models.IntegerField()
    fail = models.IntegerField()
    no_items = models.IntegerField()
    skip = models.IntegerField()
    captcha = models.IntegerField()
    last_modified = models.DateTimeField()
    message = models.CharField(max_length=191)
    last_scan_date = models.DateTimeField()
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    class Meta:
        db_table = 'workerstatus'
        in_db = 'rocketdb'
        app_label = 'scannerdb'
