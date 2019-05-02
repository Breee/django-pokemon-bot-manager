# Add recognized model option to django
from django.db import models

class AllowedDiscordServer(models.Model):
    server_id = models.CharField(db_index=True, max_length=128)
    name = models.CharField(max_length=128, default=None, blank=True, null=True)

class MessageType(models.Model):
    CHOICES = [('P', "pokestop"), ('G', 'gym'), ('S','spawn')]
    message_type = models.CharField(choices=CHOICES, max_length=128)

class SentMessages(models.Model):
    session_key = models.CharField(db_index=True, max_length=128)
    message_type = models.ForeignKey(MessageType, on_delete=models.CASCADE)

class Pokedex(models.Model):
    pokemon_id = models.IntegerField(primary_key=True)
    name_en = models.CharField(max_length=128,default=None, blank=True, null=True)
    name_ger = models.CharField(max_length=128, default=None, blank=True, null=True)
    name_fr = models.CharField(max_length=128, default=None, blank=True, null=True)
