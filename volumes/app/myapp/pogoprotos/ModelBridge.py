import json
from typing import Union

from django.utils import timezone

from myapp.models import PointOfInterest, PokemonSpawn, Pokemon, SpawnPoint, Quest
from pogoprotos.data.quests import quest_pb2
from pogoprotos.data.quests.client_quest_pb2 import ClientQuest
from pogoprotos.map.fort.fort_data_pb2 import FortData
from pogoprotos.map.map_cell_pb2 import MapCell
from pogoprotos.map.pokemon.map_pokemon_pb2 import MapPokemon
from pogoprotos.map.pokemon.wild_pokemon_pb2 import WildPokemon
from pogoprotos.map.spawn_point_pb2 import SpawnPoint as SpawnPoint_pb2
from pogoprotos.networking.responses.disk_encounter_response_pb2 import DiskEncounterResponse
from pogoprotos.networking.responses.encounter_response_pb2 import EncounterResponse
from pogoprotos.networking.responses.fort_details_response_pb2 import FortDetailsResponse
from pogoprotos.networking.responses.fort_search_response_pb2 import FortSearchResponse
from pogoprotos.networking.responses.gym_get_info_response_pb2 import GymGetInfoResponse


def update_map_poi(fort: FortData):

    def get_if_not_empty(new_value, old_value):
        return new_value if new_value is not None and new_value != '' else old_value

    if fort.type == 1:
        fort_type = 'pokestop'
    elif fort.type == 0:
        fort_type = 'gym'
    else:
        return
    queryset = PointOfInterest.objects.filter(poi_id=fort.id)
    if queryset.exists():
        poi_object: PointOfInterest = queryset.first()
        if poi_object.last_modified != fort.last_modified_timestamp_ms:
            poi_object.poi_id = get_if_not_empty(fort.id, poi_object.poi_id)
            poi_object.enabled = get_if_not_empty(fort.enabled, poi_object.enabled)
            poi_object.type = get_if_not_empty(fort_type, poi_object.type)
            poi_object.last_modified = get_if_not_empty(fort.last_modified_timestamp_ms,
                                                        poi_object.last_modified)
            poi_object.save()
    else:
        PointOfInterest.objects.create(poi_id=fort.id,
                                       longitude=fort.longitude,
                                       latitude=fort.latitude,
                                       type=fort_type,
                                       last_modified=fort.last_modified_timestamp_ms)


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
    disappear_time = timezone.now() + timezone.timedelta(minutes=10)
    print(pokemon)
    if hasattr(pokemon, 'expiration_timestamp_ms'):
        if pokemon.expiration_timestamp_ms != -1:
            disappear_time = timezone.now() + timezone.timedelta(milliseconds=pokemon.expiration_timestamp_ms)

        # sometimes the 'expiration_timestamp_ms' is too damn high. Then ignore it.
        if disappear_time > timezone.now() + timezone.timedelta(hours=2):
            disappear_time = timezone.now() + timezone.timedelta(minutes=10)

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
    disappear_time = timezone.now() + timezone.timedelta(minutes=10)
    print(pokemon)
    if hasattr(pokemon, 'time_till_hidden_ms'):
        if pokemon.time_till_hidden_ms != -1:
            disappear_time = timezone.now() + timezone.timedelta(
                milliseconds=pokemon.time_till_hidden_ms)

    # sometimes the 'time_till_hidden_ms' is too damn high. Then ignore it.
    if disappear_time > timezone.now() + timezone.timedelta(hours=2):
        disappear_time = timezone.now() + timezone.timedelta(minutes=10)

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
        update_map_poi(fort)
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


def parse_fort_details_response(fort_details: FortDetailsResponse):

    def get_if_not_empty(new_value, old_value):
        return new_value if new_value is not None and new_value != '' else old_value

    queryset = PointOfInterest.objects.filter(poi_id=fort_details.fort_id)
    img_url = fort_details.image_urls
    if isinstance(img_url, list):
        img_url = img_url[0]
    elif isinstance(img_url, str):
        img_url.replace('[', '')
        img_url.replace(']', '')
        img_url.replace('\'', '')
    else:
        for field in img_url:
            img_url = field
            break

    if queryset.exists():
        fort_object = queryset.first()
        fort_object.name = get_if_not_empty(fort_details.name, fort_object.name)
        fort_object.image_url = get_if_not_empty(img_url, fort_object.image_url)
        fort_object.longitude = get_if_not_empty(fort_details.longitude, fort_object.longitude)
        fort_object.latitude = get_if_not_empty(fort_details.latitude, fort_object.latitude)
        fort_object.description = get_if_not_empty(fort_details.description,
                                                   fort_object.description)

        fort_object.save()
    else:
        queryset = PointOfInterest.objects.filter(longitude=fort_details.longitude,
                                                  latitude=fort_details.latitude)
        if queryset.exists():
            fort_object = queryset.first()
            fort_object.name = get_if_not_empty(fort_details.name, fort_object.name)
            fort_object.image_url = get_if_not_empty(img_url, fort_object.image_url)
            fort_object.longitude = get_if_not_empty(fort_details.longitude, fort_object.longitude)
            fort_object.latitude = get_if_not_empty(fort_details.latitude, fort_object.latitude)
            fort_object.description = get_if_not_empty(fort_details.description,
                                                       fort_object.description)

            fort_object.save()
        else:
            PointOfInterest.objects.create(
                name=fort_details.name,
                image_url=img_url,
                longitude=fort_details.longitude,
                latitude=fort_details.latitude,
                description=fort_details.description
            )


def parse_gym_get_info_response(gym_info: GymGetInfoResponse):
    def get_if_not_empty(new_value, old_value):
        return new_value if new_value is not None and new_value != '' else old_value

    fort_data = gym_info.gym_status_and_defenders.pokemon_fort_proto
    queryset = PointOfInterest.objects.filter(poi_id=fort_data.id)

    if queryset.exists():
        fort_object = queryset.first()
        fort_object.name = get_if_not_empty(gym_info.name, fort_object.name)
        fort_object.image_url = get_if_not_empty(gym_info.url, fort_object.image_url)
        if fort_data.is_ex_raid_eligible:
            fort_object.park = True
        fort_object.description = get_if_not_empty(gym_info.description, fort_object.description)
        fort_object.save()


def get_quest_id(quest: quest_pb2.Quest):
    return str(quest.quest_id)


def get_quest_conditions_dict(quest: quest_pb2.Quest):
    quest_condition = {'goal': {}}
    for field in quest.goal.condition:
        quest_condition['goal']['condition'] = {'type': field.type}
    return quest_condition


def get_quest_rewards_dict(quest: quest_pb2.Quest):
    quest_rewards = {}
    for field in quest.quest_rewards:
        quest_rewards = {'type': field.type}
        if field.type == 2:
            quest_rewards['item'] = {'item': field.item.item,
                                     'amount': field.item.amount}
        elif field.type == 3:
            print(get_quest_id(quest))
            print(quest.quest_rewards)
            quest_rewards['stardust'] = field.stardust
        elif field.type == 7:
            quest_rewards['pokemon_encounter'] = {
                'pokemon_id': field.pokemon_encounter.pokemon_id
            }
        else:
            NotImplementedError('Quest_Reqard_Type: ' + str(get_quest_id(quest)))
    return quest_rewards


def add_quest(quest):
    quest = quest.quest
    Quest.objects.create(quest_id=get_quest_id(quest),
                         quest_type=quest.quest_type,
                         pokestop_id=quest.fort_id,
                         quest_timestamp=quest.creation_timestamp_ms,
                         quest_template=quest.template_id,
                         quest_conditions=json.dumps(get_quest_conditions_dict(quest)),
                         quest_rewards=json.dumps(get_quest_rewards_dict(quest)),
                         cell_id=quest.s2_cell_id)


def update_quest(quest):
    quest = quest.quest
    quest_object = Quest.objects.get(quest_id=get_quest_id(quest))
    quest_object.quest_type = quest.quest_type
    quest_object.pokestop_id = quest.fort_id
    quest_object.quest_timestamp = quest.creation_timestamp_ms
    quest_object.quest_template = quest.template_id
    quest_object.cell_id = quest.s2_cell_id
    quest_object.quest_conditions = json.dumps(get_quest_conditions_dict(quest))
    quest_object.quest_rewards = json.dumps(get_quest_rewards_dict(quest))
    quest_object.save()


def parse_fort_search_response(fort_search: FortSearchResponse):
    quest: ClientQuest = fort_search.challenge_quest
    quest_id = get_quest_id(quest.quest)
    if not Quest.objects.filter(quest_id=quest_id).exists():
        add_quest(quest)
    else:
        update_quest(quest)


def parse_disk_encounter_response(disk_encounter: DiskEncounterResponse):
    print(disk_encounter)
