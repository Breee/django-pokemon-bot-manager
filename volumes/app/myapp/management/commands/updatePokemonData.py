from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
import json
from myapp.models import Pokemon, PointOfInterest


class UpdatePokemonDataHelpers:

        def __init__(self, stdout):
            self.stdout = stdout

        def create_pokemon(self, json_data):
            pokemon = Pokemon(number=json_data['number'],
                              name_english=json_data['name_english'],
                              name_german=json_data['name_german'],
                              name_french=json_data['name_french'],
                              flee_rate=json_data['flee_rate'],
                              capture_rate=json_data['capture_rate'],
                              max_cp=json_data['max_cp'],
                              egg_distance=json_data['egg_distance'],)
            if json_data['rarity'] is not None:
                pokemon.rarity = json_data['rarity']
            self.stdout.write(str(pokemon))
            pokemon.save()

        def create_point_of_interest(self, json_data):
            poi = PointOfInterest(poi_id=self._safe_get_dict_value(json_data, 'poi_id'),
                                  name=self._safe_get_dict_value(json_data, 'name'),
                                  latitude=self._safe_get_dict_value(json_data, 'latitude'),
                                  longitude=self._safe_get_dict_value(json_data, 'longitude'),
                                  type=self._safe_get_dict_value(json_data, 'type'))
            self.stdout.write(str(poi))
            poi.save()


        @staticmethod
        def _safe_get_dict_value(dictionary, key):
            if key in dictionary:
                return dictionary[key]
            else:
                return None


class Command(BaseCommand):
    help = 'updates the pokemon data from various sources'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helperFunctions = UpdatePokemonDataHelpers(self.stdout)

#    def add_arguments(self, parser):
#        parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):

        pokemon_file = "jsonData/pokemon.json"
        with open(pokemon_file) as pokemon_json:
            pokemon = json.load(pokemon_json)
            for json_data in pokemon:
                try:
                    Pokemon.objects.get(number=json_data['number'])
                except ObjectDoesNotExist:
                    self.helperFunctions.create_pokemon(json_data)

        pokestop_file = 'jsonData/pokestop.json'
        with open(pokestop_file) as poi_json:
            pokestops = json.load(poi_json)
            for json_data in pokestops:
                try:
                    PointOfInterest.objects.get(poi_id=json_data['poi_id'])
                except ObjectDoesNotExist:
                    self.helperFunctions.create_point_of_interest(json_data)

        gym_file = 'jsonData/gym.json'
        with open(gym_file) as poi_json:
            gyms = json.load(poi_json)
            for json_data in gyms:
                try:
                    PointOfInterest.objects.get(poi_id=json_data['poi_id'])
                except ObjectDoesNotExist:
                    self.helperFunctions.create_point_of_interest(json_data)
