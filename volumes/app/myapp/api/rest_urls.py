from django.conf.urls import url, include
from rest_framework import routers
from rest_framework.authtoken import views

from myapp.api.rest_api import set_token, get_pokemon, UserList, UserDetail, PokemonPositionSet

router = routers.DefaultRouter()
router.register(r'pokepositions', PokemonPositionSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^settoken/', set_token, name='rest_settoken'),
    url(r'^pokemon/', get_pokemon, name='rest_get_pokemon'),
    url(r'^api-token-auth/', views.obtain_auth_token),
    url(r'^users/$', UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', UserDetail.as_view()),
]