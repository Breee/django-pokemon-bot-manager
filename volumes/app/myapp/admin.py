from django.contrib import admin
from myapp.models import GymDefenders, FortSightings, Forts, AllowedDiscordServer, IngressPortals, MysterySightings, Nests, Pokestops, Raids, Sightings, Spawnpoints, Trshash, TrsQuest, TrsSpawn, TrsSpawnsightings, TrsStatus, TrsUsage, Weather

from rest_framework.authtoken.admin import TokenAdmin

class QuestAdmin(admin.ModelAdmin):
    search_fields = ['guid']


# Register your models here.
admin.site.register(GymDefenders)
admin.site.register(FortSightings)
admin.site.register(Forts)
admin.site.register(AllowedDiscordServer)
admin.site.register(IngressPortals)
admin.site.register(Pokestops)
admin.site.register(Raids)
admin.site.register(MysterySightings)
admin.site.register(Nests)
admin.site.register(Sightings)
admin.site.register(Spawnpoints)
admin.site.register(TrsQuest, QuestAdmin)
admin.site.register(TrsSpawnsightings)
admin.site.register(TrsSpawn)
admin.site.register(TrsStatus)
admin.site.register(Trshash)


TokenAdmin.raw_id_fields = ('user',)
