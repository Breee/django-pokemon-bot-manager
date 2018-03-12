from django.conf.urls import url, include
from rest_framework import routers

from myapp.api.rest_api import PokemonPositionSet, PokemonSet

router = routers.DefaultRouter()
router.register(r'pokepositions', PokemonPositionSet)
router.register(r'pokemon', PokemonSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
]