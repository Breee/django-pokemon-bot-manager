"use strict";

function clusterIcon(cluster) {
		var childCount = cluster.getChildCount();

		var c = ' marker-cluster-';
		if (childCount < 10) {
			c += 'small';
		} else if (childCount < 100) {
			c += 'medium';
		} else {
			c += 'large';
		}

		return new L.DivIcon({
            html: '<div style="opacity: 0.5;" ><span>' + childCount + '</span></div>',
            className: 'marker-cluster' + c,
            iconSize: new L.Point(40, 40)
		});
}





var mymap = L.map('map').setView([47.9960526,7.8464833], 13);
var ivpokemonGroup = undefined;
var pokemonGroup = undefined;
var pokestopLayer = undefined;
var gymLayer = undefined;
var mapperLayer = undefined;
var url = 'https://maps.wikimedia.org/osm-intl/{z}/{x}/{y}.png';

L.tileLayer(url, {
    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
    maxZoom: 18,
    id: 'openstreetmap'
}).addTo(mymap);

var sidebar = L.control.sidebar('sidebar').addTo(mymap);

var get_popup_data = function(pokemon) {
    var date = new Date(pokemon.disappear_time);

    var today = new Date();
    var date_str = '';
    if (date.getDate() > today.getDate()) {
        date_str = date.toLocaleDateString('de-DE') + ' ';
    }
    if (pokemon.individual_stamina != null) {
        var iv_sta = pokemon.individual_stamina;
        var iv_att = pokemon.individual_attack;
        var iv_def = pokemon.individual_defense;
        var iv_proc = Math.round(((iv_sta + iv_att + iv_def)/45)*10000)/100;
        var iv_str = '<b>IV:</b>' + iv_proc + '% ' + '(A' + iv_att + '|D' + iv_def + '|S' + iv_sta + ')<br>';
        var cp_str = '<b>CP:</b>' + pokemon.cp + '<br>';
    }
    else {
        iv_str = '';
        cp_str = '';
    }

    var maps_str = '<a href="https://www.google.com/maps/place/' + pokemon.latitude + ',' +
        pokemon.longitude + '" target="_blank" title="Open in Google Maps">' + 'Maps</a><br>';

    return '<h3>' + pokedex[pokemon.pokemon_object -1].name_german + ' (' + pokemon.pokemon_object + ')' + '</h3>' +
        '<b>Despawn Time</b> ' + date_str + date.toLocaleTimeString('de-DE') + '<br>' +
         iv_str + cp_str + maps_str;
};

function addPokemonToMap(data) {
        if (pokemonGroup !== undefined && ivpokemonGroup !== undefined) {
            pokemonGroup.clearLayers();
            ivpokemonGroup.clearLayers();
        }
        else {
            pokemonGroup = L.layerGroup();
            ivpokemonGroup = L.layerGroup();
        }
        for (var i in data) {
            if (data.hasOwnProperty(i)) {
                var pokemon = data[i];

                var popup = get_popup_data(pokemon);
                var marker = L.marker([pokemon.latitude, pokemon.longitude],
                    {
                        title: pokedex[pokemon.pokemon_object - 1].name_german,
                        icon: L.icon({
                            iconUrl: "/static/img/pokemons/" + pokemon.pokemon_object + '.png',
                            iconSize: [32, 32],
                            popupAnchor: [-3, -76]
                        })
                    });
                marker.bindPopup(popup);
                if (pokemon.individual_stamina !== null || pokemon.individual_attack !== null || pokemon.individual_defense !== null) {
                    ivpokemonGroup.addLayer(marker);
                } else {
                    pokemonGroup.addLayer(marker);
                }
            }
        }
        if (!mapCookie.ivPokemonHidden) {
            ivpokemonGroup.addTo(mymap);
        }
        if (!mapCookie.regularPokemonHidden) {
            pokemonGroup.addTo(mymap);
        }
}

function getQuestInfo(successFn) {
    $.getJSON('/api/quest/', function(data) {
        var quests = {}
        for (var key in data) {
            quests[data[key].pokestop_id] = data[key];
        }
        successFn(quests);
    })
}


function addMapperToMap(data) {
    if (mapperLayer !== undefined) {
            mapperLayer.clearLayers();
        } else {
            mapperLayer = L.layerGroup();
    }
    for (var i in data) {
            if (data.hasOwnProperty(i)) {
                var mapper = data[i];
                console.log('test')
                var popup = mapper.name + '<br>';
                popup += mapper.uuid + '<br>';
                popup += mapper.longitude + '<br>';
                popup += mapper.latitude + '<br>';
                popup += 'updated: ' + mapper.updated + '<br>';
                var marker = L.marker([mapper.latitude, mapper.longitude],
                    {
                        title: data.name,
                        icon: L.icon({
                            iconUrl: '/static/img/map/iphone.png',
                            iconSize: [20, 20],
                            popupAnchor: [-3, -76]
                        })
                    });
                marker.bindPopup(popup);

                mapperLayer.addLayer(marker);
            }
        }
        if (!mapCookie.mapperHidden) {
            mapperLayer.addTo(mymap);
        }
}


function addPointOfInterestToMap(data) {
        if (pokestopLayer !== undefined) {
            gymLayer.clearLayers();
            pokestopLayer.clearLayers();
        } else {
            gymLayer = L.markerClusterGroup({
                maxClusterRadius: 120,
                disableClusteringAtZoom: 15,
                iconCreateFunction: clusterIcon
            });
            pokestopLayer = L.markerClusterGroup({
                maxClusterRadius: 120,
                disableClusteringAtZoom: 17,
                iconCreateFunction: clusterIcon
            });
        }
        getQuestInfo(function (quests) {
            for (var i in data) {
                if (data.hasOwnProperty(i)) {

                    var poi = data[i];
                    var popup = "" + poi.name + "<br>";
                    var marker;
                    if (poi.image_url !== null) {
                        popup += '<img style="width:125px; height: 125px; object-fit: cover;" src="' + poi.image_url + '" /><br>'
                    }
                    if (poi.type === "pokestop") {
                        marker = L.marker([poi.latitude, poi.longitude],
                                {
                                    title: poi.name,
                                    icon: L.icon({
                                        iconUrl: "/static/img/map/pstop.png",
                                        iconSize: [32, 32],
                                        popupAnchor: [-3, -76]
                                    })
                                });
                        if (poi.poi_id in quests) {
                            popup += 'Quest: ' + quests[poi.poi_id].quest_template + '<br>';
                        }
                        marker.bindPopup(popup);
                        pokestopLayer.addLayer(marker);
                    }
                    else if (poi.type === "gym") {
                        var iconUrl = "/static/img/map/gym.png";
                        if (poi.park === true) {
                            iconUrl = "/static/img/map/ex_gym.png"
                        }
                        marker = L.marker([poi.latitude, poi.longitude],
                            {
                                title: poi.name,
                                icon: L.icon({
                                    iconUrl: iconUrl,
                                    iconSize: [32, 32],
                                    popupAnchor: [-3, -76]
                                }),
                                opacity: 0.8
                            });
                        marker.bindPopup(popup);
                        gymLayer.addLayer(marker);
                    } else {
                        marker = L.marker([poi.latitude, poi.longitude],
                            {
                                title: poi.name,
                                icon: L.icon({
                                    iconUrl: "/static/img/map/pstop.png",
                                    iconSize: [32, 32],
                                    popupAnchor: [-3, -76]
                                })
                            });
                        marker.bindPopup(popup);
                        pokestopLayer.addLayer(marker);
                    }
                }
            }
            if (!mapCookie.gymsHidden) {
                gymLayer.addTo(mymap);
            }
            if (!mapCookie.pokestopsHidden) {
                pokestopLayer.addTo(mymap);
            }
        });
}



var toggleMapLayer = function(layer, bool) {
     if (!bool) {
        layer.addTo(mymap);
    }
    else {
        layer.remove(mymap);
    }
    return !bool;
};


