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





var mymap = L.map('map').setView([47.9960526,7.8464833], 15);
var ivPokemonLayer = undefined;
var ivPokemonDict= {};
var regularPokemonLayer = undefined;
var regularPokemonDict= {};
var pokestopLayer = undefined;
var pokestopDict= {};
var gymLayer = undefined;
var gymDict= {};
var mapperLayer = undefined;
var mapperDict = {};
var questDict = {};

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
        if (regularPokemonLayer === undefined && ivPokemonLayer === undefined) {
            regularPokemonLayer = L.layerGroup();
            ivPokemonLayer = L.layerGroup();
        }
        for (var i in data) {
            if (data.hasOwnProperty(i)) {
                var pokemon = data[i];
                var marker = get_pokemon_marker(pokemon);
                if (pokemon.individual_stamina !== null || pokemon.individual_attack !== null || pokemon.individual_defense !== null) {
                    updateLayer(ivPokemonLayer, ivPokemonDict, marker, pokemon.encounter_id)
                } else {
                    updateLayer(regularPokemonLayer, regularPokemonDict, marker, pokemon.encounter_id)
                }
            }
        }
        if (!mapCookie.ivPokemonHidden) {
            ivPokemonLayer.addTo(mymap);
        }
        if (!mapCookie.regularPokemonHidden) {
            regularPokemonLayer.addTo(mymap);
        }
}

function get_pokemon_marker(pokemon) {
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
    return marker
}

function updateLayer(layer, dict, marker, id) {
    if (dict.hasOwnProperty(id)) {
        var old_marker = dict[id];
        layer.removeLayer(old_marker);
        dict[id] = marker;
        layer.addLayer(marker);
    }
    else {
       dict[id] = marker;
        layer.addLayer(marker);
    }


}

function getQuestInfo() {
    $.getJSON('/api/quest/', parseQuestData);
}

function parseQuestData(data) {
    if (pokestopLayer !== undefined) {
        for (var key in data) {
            if (data.hasOwnProperty(key)) {
                var quest = data[key];
                var poi_id = quest.pokestop_id;
                var marker = pokestopDict[poi_id];
                if (questDict.hasOwnProperty(poi_id)) {
                    popup = questDict[poi_id][1];
                    marker._popup.setContent(popup + 'Quest: ' + quest.quest_template + '<br>')
                } else {
                    var popup = marker._popup._content;

                    questDict[poi_id] = [marker, popup];
                    marker._popup.setContent(popup + 'Quest: ' + quest.quest_template + '<br>')
                }
                updateLayer(pokestopLayer, pokestopDict, marker, poi_id);
            }
        }
    }
    else {
        setTimeout(function () {
            parseQuestData(data);
        }, 2000)
    }
}


function addMapperToMap(data) {
    if (mapperLayer === undefined) {
        mapperLayer = L.layerGroup();
    }
    for (var i in data) {
            if (data.hasOwnProperty(i)) {
                var mapper = data[i];
                var marker = get_mapper_marker(mapper);

                updateLayer(mapperLayer, mapperDict, marker, mapper.uuid)
            }
        }
        if (!mapCookie.mapperHidden) {
            mapperLayer.addTo(mymap);
        }
}

function get_mapper_marker(mapper) {
    var popup = mapper.name + '<br>';
    popup += mapper.uuid + '<br>';
    popup += mapper.longitude + '<br>';
    popup += mapper.latitude + '<br>';
    var updated = new Date(mapper.updated);
    popup += 'updated: ' + updated.toLocaleTimeString('de-DE') + '<br>';
    var marker = L.marker([mapper.latitude, mapper.longitude],
        {
            title: mapper.name,
            icon: L.icon({
                iconUrl: '/static/img/map/iphone.png',
                iconSize: [20, 20],
                popupAnchor: [-3, -76]
            })
        });
    marker.bindPopup(popup);
    return marker;
}


function addPointOfInterestToMap(data) {
        if (pokestopLayer === undefined) {
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
        for (var i in data) {
            if (data.hasOwnProperty(i)) {

                var poi = data[i];
                var marker = get_poi_marker(poi);
                var type = poi.type;
                if (type === 'pokestop') {
                    updateLayer(pokestopLayer, pokestopDict, marker, poi.poi_id)
                }
                else if (type === 'gym') {
                    updateLayer(gymLayer, gymDict, marker, poi.poi_id)
                }
            }
        }
        if (!mapCookie.gymsHidden) {
            gymLayer.addTo(mymap);
        }
        if (!mapCookie.pokestopsHidden) {
            pokestopLayer.addTo(mymap);
        }
}


function get_poi_marker(poi) {
    var type = poi.type;
    var popup = "" + poi.name + "<br>";
    if (poi.image_url !== null) {
        popup += '<img style="width:125px; height: 125px; object-fit: cover;" src="' + poi.image_url + '" /><br>'
    }


    var icon_url = '';
    if (type === 'gym') {
        icon_url = "/static/img/map/gym.png";
        if (poi.park === true) {
            icon_url = "/static/img/map/ex_gym.png";
        }
    }
    else {
        icon_url = "/static/img/map/pstop.png";
    }

    var marker = L.marker([poi.latitude, poi.longitude],
            {
                title: poi.name,
                icon: L.icon({
                    iconUrl: icon_url,
                    iconSize: [32, 32],
                    popupAnchor: [-3, -76]
                })
            });
    marker.bindPopup(popup);
    return marker;
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


