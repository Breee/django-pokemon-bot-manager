from typing import Union

from django.utils import timezone

from myapp.models import PointOfInterest, PokemonSpawn, Pokemon, SpawnPoint
from pogoprotos.map.fort.fort_data_pb2 import FortData
from pogoprotos.map.map_cell_pb2 import MapCell
from pogoprotos.map.pokemon.map_pokemon_pb2 import MapPokemon
from pogoprotos.map.pokemon.wild_pokemon_pb2 import WildPokemon
from pogoprotos.map.spawn_point_pb2 import SpawnPoint as SpawnPoint_pb2
from pogoprotos.networking.responses.encounter_response_pb2 import EncounterResponse


def update_poi(fort: FortData):
    if fort.type == 1:
        fort_type = 'pokestop'
    elif fort.type == 0:
        fort_type = 'gym'
    else:
        return
    queryset = PointOfInterest.objects.filter(poi_id=fort.fort_id)
    if queryset.exists():
        poi_object: PointOfInterest = queryset.first()
        poi_object.poi_id = fort.id
        poi_object.enabled = fort.enabled
        poi_object.type = fort_type
        poi_object.save()
    else:
        PointOfInterest.objects.create(poi_id=fort.id,
                                       longitude=fort.longitude,
                                       latitude=fort.latitude,
                                       type=fort_type)


def add_map_pokemon_spawn(pokemon: MapPokemon):
    # check if encounter was processed before
    queryset = PokemonSpawn.objects.filter(encounter_id=pokemon.encounter_id)
    if queryset.exists():
        return

    pokemon_object = Pokemon.objects.filter(number=pokemon.pokemon_id)

    # check if pokemon with number exists
    if pokemon_object.exists():
        pokemon_object = pokemon_object.first()
    else:
        raise NotImplementedError('Pokemon ' + pokemon['pokemon_id'])

    # compute disappear time
    disappear_time = timezone.now() + timezone.timedelta(minutes=30)
    print(pokemon)
    if hasattr(pokemon, 'expiration_timestamp_ms'):
        if pokemon.expiration_timestamp_ms != -1:
            disappear_time = timezone.now() + timezone.timedelta(milliseconds=pokemon.expiration_timestamp_ms)

    # create pokemon
    PokemonSpawn.objects.create(encounter_id=pokemon.encounter_id,
                                pokemon_object=pokemon_object,
                                latitude=pokemon.latitude,
                                longitude=pokemon.longitude,
                                disappear_time=disappear_time)
    # update pokemon with optional additional data
    update_pokemon_spawn(pokemon)


def add_wild_pokemon_spawn(pokemon: WildPokemon):
    # check if encounter was processed before
    queryset = PokemonSpawn.objects.filter(encounter_id=pokemon.encounter_id)
    if queryset.exists():
        return

    pokemon_object = Pokemon.objects.filter(number=pokemon.pokemon_data.pokemon_id)

    # check if pokemon with number exists
    if pokemon_object.exists():
        pokemon_object = pokemon_object.first()
    else:
        raise NotImplementedError('Pokemon ' + pokemon.pokemon_data.pokemon_id)

    # compute disappear time
    disappear_time = timezone.now() + timezone.timedelta(minutes=30)
    print(pokemon)
    if hasattr(pokemon, 'time_till_hidden_ms'):
        if pokemon.time_till_hidden_ms != -1:
            disappear_time = timezone.now() + timezone.timedelta(
                milliseconds=pokemon.expiration_timestamp_ms)

    # create pokemon
    PokemonSpawn.objects.create(encounter_id=pokemon.encounter_id,
                                pokemon_object=pokemon_object,
                                latitude=pokemon.latitude,
                                longitude=pokemon.longitude,
                                disappear_time=disappear_time)
    # update pokemon with optional additional data
    update_pokemon_spawn(pokemon)


def update_pokemon_spawn(pokemon: Union[MapPokemon, WildPokemon]):
    pokemon_object = PokemonSpawn.objects.get(encounter_id=pokemon.encounter_id)
    if hasattr(pokemon, 'pokemon_display'):
        if hasattr(pokemon.pokemon_display, 'weather_boosted_condition'):
            pokemon_object.weather_boosted_condition = pokemon.pokemon_display.weather_boosted_condition
        if hasattr(pokemon.pokemon_display, 'gender'):
            pokemon_object.gender = pokemon.pokemon_display.gender
        if hasattr(pokemon.pokemon_display, 'form'):
            pokemon_object.gender = pokemon.pokemon_display.form
        if hasattr(pokemon.pokemon_display, 'costume'):
            pokemon_object.costume = pokemon.pokemon_display.costume
    if hasattr(pokemon, 'pokemon_data'):
        if hasattr(pokemon.pokemon_data, 'individual_stamina'):
            pokemon_object.individual_stamina = pokemon.pokemon_data.individual_stamina
        if hasattr(pokemon.pokemon_data, 'individual_attack'):
            pokemon_object.individual_attack = pokemon.pokemon_data.individual_attack
        if hasattr(pokemon.pokemon_data, 'individual_defense'):
            pokemon_object.individual_defense = pokemon.pokemon_data.individual_defense
        pokemon_object.cp = pokemon.pokemon_data.cp
        pokemon_object.cp_multiplier = pokemon.pokemon_data.cp_multiplier

    pokemon_object.save()
    print('pokemonspawn saved')


def add_spawn_point(map_cell: MapCell, spawn_point: SpawnPoint_pb2):
    queryset = SpawnPoint.objects.filter(longitude=spawn_point.longitude,
                                         latitude=spawn_point.latitude)
    if not queryset.exists():
        SpawnPoint.objects.create(longitude=spawn_point.longitude,
                                  latitude=spawn_point.latitude)
        print('spawn point created')


def parse_map_cell(map_cell: MapCell):
    for fort in map_cell.forts:
        update_poi(fort)
    for pokemon in map_cell.catchable_pokemons:
        add_map_pokemon_spawn(pokemon)
    for pokemon in map_cell.wild_pokemons:
        add_wild_pokemon_spawn(pokemon)
    for spawn_point in map_cell.spawn_points:
        queryset = SpawnPoint.objects.filter(id=map_cell.s2_cell_id)
        if not queryset.exists():
            add_spawn_point(map_cell, spawn_point)


def parse_encounter_response(encounter: EncounterResponse):
    # parse pokemon
    pokemon = encounter.wild_pokemon
    queryset = PokemonSpawn.objects.filter(encounter_id=pokemon.encounter_id)
    if queryset.exists():
        print('trying update')
        update_pokemon_spawn(pokemon)
    else:
        print('trying add')
        add_wild_pokemon_spawn(pokemon)




