from typing import Union

from django.utils import timezone

from myapp.models import PointOfInterest, PokemonSpawn, Pokemon
from pogoprotos.map.fort.fort_data_pb2 import FortData
from pogoprotos.map.map_cell_pb2 import MapCell
from pogoprotos.map.pokemon.map_pokemon_pb2 import MapPokemon
from pogoprotos.map.pokemon.nearby_pokemon_pb2 import NearbyPokemon
from pogoprotos.map.pokemon.wild_pokemon_pb2 import WildPokemon
from pogoprotos.networking.responses.encounter_response_pb2 import EncounterResponse


def update_poi(fort: FortData, virtual: bool = False):
    if fort.type == 1:
        fort_type = 'pokestop'
    elif fort.type == 0:
        fort_type = 'arena'
    else:
        return
    queryset = PointOfInterest.objects.filter(longitude__gte=fort.longitude - 0.0002,
                                              longitude__lte=fort.longitude + 0.0002,
                                              latitude__gte=fort.latitude - 0.0002,
                                              latitude__lte=fort.latitude + 0.0002)
    if queryset.exists():
        if queryset.count() > 1:
            print(fort_type, ' is not unique! ' + str(fort.latitude) + ', ' + str(fort.longitude))
        else:
            poi_object: PointOfInterest = queryset.first()
            poi_object.poi_id = fort.id
            poi_object.enabled = fort.enabled
            poi_object.type = fort_type
            poi_object.save()
            # print(fort_type, ' updated')
    else:
        PointOfInterest.objects.create(poi_id=fort.id,
                                       longitude=fort.longitude,
                                       latitude=fort.latitude,
                                       type=fort_type)
        print(fort_type, ' created')


def add_pokemon_spawn(pokemon: Union[MapPokemon, WildPokemon]):
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


def update_pokemon_spawn(pokemon: Union[MapPokemon, WildPokemon]):
    pokemon_object = PokemonSpawn.objects.get(encounter_id=pokemon.encounter_id)
    if hasattr(pokemon, 'pokemon_display'):
        if hasattr(pokemon.pokemon_display, 'weather_boosted_condition'):
            pokemon_object.weather_boosted_condition = pokemon.pokemon_display.weather_boosted_condition
        if hasattr(pokemon.pokemon_display, 'gender'):
            pokemon_object.gender = pokemon.pokemon_display.gender
        if hasattr(pokemon.pokemon_display, 'form'):
            pokemon_object.gender = pokemon.pokemon_display.form
        if hasattr(pokemon.pokemon_display, 'form'):
            pokemon_object.costume = pokemon.pokemon_display.costume
    if hasattr(pokemon, 'pokemon_data'):
        pokemon_object.individual_stamina = pokemon.pokemon_data.individual_stamina
        pokemon_object.individual_attack = pokemon.pokemon_data.individual_attack
        pokemon_object.individual_defense = pokemon.pokemon_data.individual_defense
        pokemon_object.cp = pokemon.pokemon_data.cp
        pokemon_object.cp_multiplier = pokemon.pokemon_data.cp_multiplier

    pokemon_object.save()
    print('pokemonspawn saved')


def parse_map_cell(map_cell: MapCell):
    for fort in map_cell.forts:
        update_poi(fort)
    for pokemon in map_cell.catchable_pokemons:
        add_pokemon_spawn(pokemon)
    for pokemon in map_cell.wild_pokemons:
        add_pokemon_spawn(pokemon)


def parse_encounter_response(encounter: EncounterResponse):
    # parse pokemon
    pokemon = encounter.wild_pokemon
    queryset = PokemonSpawn.objects.filter(encounter_id=pokemon.encounter_id)
    if queryset.exists():
        update_pokemon_spawn(pokemon)
    else:
        add_pokemon_spawn(pokemon)




