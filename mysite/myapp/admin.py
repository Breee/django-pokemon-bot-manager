from django.contrib import admin
from .models import PokePosition, Pokemon
# Register your models here.
admin.site.register(Pokemon)
admin.site.register(PokePosition)
