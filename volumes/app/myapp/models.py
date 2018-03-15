from django.db import models
from django.utils import timezone
from rest_framework.authtoken.models import Token


class Pokemon(models.Model):
    poke_nr = models.IntegerField(primary_key=True)
    poke_name_ger = models.CharField(max_length=30)
    poke_name_eng = models.CharField(max_length=30)

    class Meta:
        # Sort the Data by this:
        ordering = ('poke_nr',)

    def __str__(self):
        return str(self.poke_nr) + ' - ' + self.poke_name_ger


class PokePosition(models.Model):
    poke_report_time = models.DateTimeField(default=timezone.now)
    poke_pos_id = models.IntegerField(primary_key=True, auto_created=True)
    poke_lvl = models.IntegerField(default=0)
    poke_iv = models.FloatField(default=.0)
    poke_lat = models.FloatField()
    poke_lon = models.FloatField()
    poke_nr = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    poke_despawn_time = models.DateTimeField()
