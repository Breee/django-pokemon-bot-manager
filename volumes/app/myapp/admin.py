from django.contrib import admin
from .models import PointOfInterest, Pokemon, PokemonSpawn, PokemonType

from rest_framework.authtoken.admin import TokenAdmin

# Register your models here.
admin.site.register(Pokemon)
admin.site.register(PokemonSpawn)
admin.site.register(PokemonType)
admin.site.register(PointOfInterest)


TokenAdmin.raw_id_fields = ('user',)
