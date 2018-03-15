from django.conf.urls import url, include
from rest_framework import routers
from rest_framework.authtoken import views

from myapp.api.rest_api import get_pokemon, UserList, UserDetail, PokemonPositionSet, PokmonPositionSet2

router = routers.DefaultRouter()
router.register(r'pokepositions', PokemonPositionSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^pokemon/', get_pokemon, name='rest_get_pokemon'),
    url(r'^pokepositions2/$', PokmonPositionSet2.as_view()),
    url(r'^users/$', UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', UserDetail.as_view()),
]