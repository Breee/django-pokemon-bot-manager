# Generated by Django 2.1.4 on 2018-12-11 21:36

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0010_auto_20181210_0014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pokemonspawn',
            name='_individual_percentage',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='pokemonspawn',
            name='costume',
            field=models.SmallIntegerField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='pokemonspawn',
            name='cp',
            field=models.SmallIntegerField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='pokemonspawn',
            name='cp_multiplier',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='pokemonspawn',
            name='form',
            field=models.SmallIntegerField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='pokemonspawn',
            name='gender',
            field=models.SmallIntegerField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='pokemonspawn',
            name='height',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='pokemonspawn',
            name='individual_attack',
            field=models.SmallIntegerField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='pokemonspawn',
            name='individual_defense',
            field=models.SmallIntegerField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='pokemonspawn',
            name='individual_stamina',
            field=models.SmallIntegerField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='pokemonspawn',
            name='last_modified',
            field=models.DateTimeField(blank=True, db_index=True, default=django.utils.timezone.now, null=True),
        ),
        migrations.AlterField(
            model_name='pokemonspawn',
            name='level',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='pokemonspawn',
            name='moves',
            field=models.ManyToManyField(blank=True, default=None, null=True, to='myapp.PokemonMove'),
        ),
        migrations.AlterField(
            model_name='pokemonspawn',
            name='weather_boosted_condition',
            field=models.SmallIntegerField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='pokemonspawn',
            name='weight',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
    ]