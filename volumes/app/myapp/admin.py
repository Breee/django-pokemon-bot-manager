from django.contrib import admin
from .models import PointOfInterest, Pokemon, PokemonSpawn, PokemonType, SpawnPoint, Quest, Mapper

from rest_framework.authtoken.admin import TokenAdmin


class PointOfInterestAdmin(admin.ModelAdmin):
    search_fields = ['type', 'name', 'poi_id', 'last_modified']


class QuestAdmin(admin.ModelAdmin):
    search_fields = ['quest_id', 'pokestop_id', 'pokemon_id', 'quest_item_id', 'quest_reward_type']


# Register your models here.
admin.site.register(Pokemon)
admin.site.register(PokemonSpawn)
admin.site.register(SpawnPoint)
admin.site.register(PokemonType)
admin.site.register(Quest, QuestAdmin)
admin.site.register(Mapper)
admin.site.register(PointOfInterest, PointOfInterestAdmin)


TokenAdmin.raw_id_fields = ('user',)
