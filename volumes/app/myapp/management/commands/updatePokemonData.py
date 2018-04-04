from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
import json
from myapp.models import Pokemon


class UpdatePokemonDataHelpers:

        def createPokemon(self, json_data):
            pokemon = Pokemon(number=json_data['number'],
                          name_english=json_data['name_english'],
                          name_german=json_data['name_german'],
                          name_french=json_data['name_french'],
                          flee_rate=json_data['flee_rate'],
                          capture_rate=json_data['capture_rate'],
                          max_cp=json_data['max_cp'],
                          egg_distance=json_data['egg_distance'],
                          )
            if json_data['rarity'] is not None:
                pokemon.rarity = json_data['rarity']
            self.stdout.write(str(pokemon))
            pokemon.save()


class Command(BaseCommand):
    help = 'updates the pokemon data from various sources'
    helperFunctions = UpdatePokemonDataHelpers()

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
                    self.helperFunctions.createPokemon(json_data)

