# Generated by Django 2.1.3 on 2018-12-14 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0014_auto_20181214_1324'),
    ]

    operations = [
        migrations.CreateModel(
            name='AllowedDiscordServer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default=None, max_length=128, null=True)),
            ],
        ),
    ]
