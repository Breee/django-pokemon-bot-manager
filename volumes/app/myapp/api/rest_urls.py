from django.urls import path, include
from rest_framework import routers
from myapp.api.rest_api import *

router = routers.DefaultRouter()

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path(r' ', include(router.urls)),
    path('pokedex/', PokedexSet.as_view(), name='rest_get_pokemon'),
    path('pokemon/spawns', PokemonSpawnSet.as_view()),
    path('poi/all', PointOfInterestSet.as_view()),
    path('quest/', QuestSet.as_view()),
    path('rdm/', RealDeviceMapBlackHole.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

#urlpatterns = format_suffix_patterns(urlpatterns)
