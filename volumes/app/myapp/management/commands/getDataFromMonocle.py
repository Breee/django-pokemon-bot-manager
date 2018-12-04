from django.core.management.base import BaseCommand
from myapp.models import Pokemon, PointOfInterest
from django.db import connections


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def updatePointOfInterests(poi_dict: list, poi_type: str):
    for point_of_interest in poi_dict:
        queryset = PointOfInterest.objects.filter(poi_id=point_of_interest['external_id'])
        if queryset.exists():
            poi_object = queryset.first()
            poi_object.latitude = point_of_interest['lat']
            poi_object.longitude = point_of_interest['lon']
            poi_object.name = point_of_interest['name']
            poi_object.image_url = point_of_interest['url']
            poi_object.type = poi_type
            if 'park' in point_of_interest:
                poi_object.park = point_of_interest['park'] is not None
                poi_object.save()
        else:
            PointOfInterest.objects.create(poi_id=point_of_interest['external_id'],
                                           latitude=point_of_interest['lat'],
                                           longitude=point_of_interest['lon'],
                                           name=point_of_interest['name'],
                                           image_url=point_of_interest['url'],
                                           type=poi_type)

            poi_object = queryset.first()
            if 'park' in point_of_interest:
                poi_object.park = point_of_interest['park'] is not None
            poi_object.save()


class Command(BaseCommand):
    help = 'updates the pokemon data from monocle db'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def handle(self, *args, **options):
        sql_query = 'SELECT * FROM pokestops'
        with connections['monocle'].cursor() as cursor:
            cursor.execute(sql_query)
            pokestops = dictfetchall(cursor)
            updatePointOfInterests(pokestops, 'pokestop')

        sql_query = 'SELECT * FROM forts'
        with connections['monocle'].cursor() as cursor:
            cursor.execute(sql_query)
            gyms = dictfetchall(cursor)
            updatePointOfInterests(gyms, 'gym')

