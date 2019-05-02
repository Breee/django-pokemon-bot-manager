from django.core.management.base import BaseCommand, CommandError
from core_app.models import Pokedex
import csv

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('pokedex_file')

    def handle(self, *args, **options):
        with open(options['pokedex_file'], 'r') as pokedex_file:
            # skip header
            next(pokedex_file)
            reader = csv.reader(pokedex_file, delimiter=',')
            for row in reader:
                pokemon_id = row[0]
                pokemon_name_en = row[2]
                pokemon_name_ger = row[3]
                pokedex_entry = Pokedex.objects.create(pokemon_id=pokemon_id,name_en=pokemon_name_en,name_ger=pokemon_name_ger)
                pokedex_entry.save()

