from django.urls import path, include
from django.conf.urls import url
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from myapp.api.rest_api import PokedexSet, UserList, UserDetail, PokemonPositionSet

router = routers.DefaultRouter()

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path(r' ', include(router.urls)),
    path('pokedex/', PokedexSet.get_pokemon, name='rest_get_pokemon'),
    path('pokedex/init', PokedexSet.init_pokemon, name='rest_init_pokemon'),
    path('pokepositions/', PokemonPositionSet.as_view()),
    path('users/', UserList.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

#urlpatterns = format_suffix_patterns(urlpatterns)
