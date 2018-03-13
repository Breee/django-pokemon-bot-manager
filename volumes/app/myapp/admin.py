from django.contrib import admin
from .models import PokePosition, Pokemon
# Register your models here.
admin.site.register(Pokemon)
admin.site.register(PokePosition)

from rest_framework.authtoken.admin import TokenAdmin

TokenAdmin.raw_id_fields = ('user',)