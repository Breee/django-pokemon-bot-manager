from django.contrib import admin
from scannerdb.rocketdb import *
from core_app.models import AllowedDiscordServer, Pokedex
from rest_framework.authtoken.admin import TokenAdmin

class QuestAdmin(admin.ModelAdmin):
    search_fields = ['guid']


# Register your models here.
admin.site.register(AllowedDiscordServer)
admin.site.register(Pokedex)

admin.site.register(Gym)
admin.site.register(Gymdetails)
admin.site.register(Gymmember)
admin.site.register(Gympokemon)
admin.site.register(Raid)
admin.site.register(Pokestop)
admin.site.register(Spawnpoint)
admin.site.register(TrsQuest, QuestAdmin)
admin.site.register(TrsSpawnsightings)
admin.site.register(TrsSpawn)
admin.site.register(TrsStatus)


TokenAdmin.raw_id_fields = ('user',)
