from django.conf.urls import url, include
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from myapp.api.rest_api import get_pokemon, UserList, UserDetail, PokemonPositionSet

router = routers.DefaultRouter()

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'pokemon/', get_pokemon, name='rest_get_pokemon'),
    url(r'pokepositions/$', PokemonPositionSet.as_view()),
    url(r'users/$', UserList.as_view()),
    url(r'users/(?P<pk>[0-9]+)/$', UserDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)

