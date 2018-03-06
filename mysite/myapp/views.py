from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .models import Pokemon, PokePosition
from .serializers import PokemonSerializer
import csv


@csrf_exempt
def test(request):
    """
    Load Pokedex if Database is empty
    Todo: Write real init!
    """
    if Pokemon.objects.count() == 0:
        with open('pokedex.csv') as pokedex:
            reader = csv.DictReader(pokedex)
            for poke in reader:
                newpoke = Pokemon(poke_nr=poke['species_id'], poke_name_eng=poke['identifier'])
                newpoke.save()
            pokedex.close()
        with open('pokedex_ger.csv') as pokedex_ger:
            reader = csv.DictReader(pokedex_ger)
            for poke in reader:
                pid = poke['Ndex']
                newpoke = Pokemon(poke_nr=int(pid), poke_name_ger=poke['German'])
                newpoke.save()
            pokedex.close()
    """
    List all Pokemon with JSON
    """
    if request.method == 'GET':
        poke = Pokemon.objects.all()
        serializer = PokemonSerializer(poke, many=True)
        return JsonResponse(serializer.data, safe=False)
