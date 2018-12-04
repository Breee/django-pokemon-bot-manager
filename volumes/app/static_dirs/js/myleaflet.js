"use strict"

var pokedex = undefined;

$.getJSON('/api/pokedex/', function (data) {
    pokedex = data;
});

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
});

var mymap = L.map('map').setView([47.9960526,7.8464833], 13);
var layerGroup = undefined;
var poiLayer = undefined;
//var url = 'https://tiles.venezilu.de/styles/osm-bright/{z}/{x}/{y}.png'
//var url = 'https://korona.geog.uni-heidelberg.de/tiles/roads/x={x}&y={y}&z={z}'
var url = 'https://maps.wikimedia.org/osm-intl/{z}/{x}/{y}.png'

L.tileLayer(url, {
    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
    maxZoom: 18,
    id: 'openstreetmap'
}).addTo(mymap);

var sidebar = L.control.sidebar('sidebar').addTo(mymap);

var get_popup_data = function(pokemon) {
    var date = new Date(pokemon.disappear_time);
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
        '<b>Despawn Time</b> ' + date.toLocaleTimeString('de-DE') + '<br>' +
         iv_str + cp_str + maps_str;
};

var getData = function () {
    $.getJSON("/api/pokemon/spawns", function(data) {


        if (layerGroup !== undefined) {
            layerGroup.clearLayers();
        }
        else {
            layerGroup = L.layerGroup();
        }
        for (var i in data) {
            var pokemon = data[i];

            var popup = get_popup_data(pokemon);
            var marker = L.marker([pokemon.latitude, pokemon.longitude],
                {title: "test",
                    icon: L.icon({
                        iconUrl: "/static/img/pokemons/" + pokemon.pokemon_object + '.png',
                        iconSize: [32, 32],
                        popupAnchor: [-3, -76]
                    }) });
            marker.bindPopup(popup);
            layerGroup.addLayer(marker);
        }
        layerGroup.addTo(mymap);

    });
};

$( function() {
    $( "#datepicker" ).datepicker();
} );

var getPOI = function() {
    $.getJSON("/api/poi/all", function (data) {
        if (poiLayer !== undefined) {
            poiLayer.clearLayers();
        } else {
            poiLayer = L.markerClusterGroup({
                maxClusterRadius: 120,
                disableClusteringAtZoom: 17
            });
        }
        for (var i in data) {
            var poi = data[i];
            var popup = "" + poi.name + "<br>";
            if (poi.type === "pokestop") {
                var marker = L.marker([poi.latitude, poi.longitude],
                    {
                        title: poi.name,
                        icon: L.icon({
                            iconUrl: "https://png.icons8.com/color/1600/pokestop-blue.png",
                            iconSize: [32, 32],
                            popupAnchor: [-3, -76]
                        })
                    });
            } else if (poi.type === "gym") {
                var marker = L.marker([poi.latitude, poi.longitude],
                    {
                        title: poi.name,
                        icon: L.icon({
                            iconUrl: "https://vignette.wikia.nocookie.net/pokemon/images/2/29/Gym_Leader_file.png",
                            iconSize: [32, 32],
                            popupAnchor: [-3, -76]
                        })
                    });
            } else {
                var marker = L.marker([poi.latitude, poi.longitude],
                    {
                        title: poi.name,
                        icon: L.icon({
                            iconUrl: "https://png.icons8.com/color/1600/pokestop-blue.png",
                            iconSize: [32, 32],
                            popupAnchor: [-3, -76]
                        })
                    });
            }
            marker.bindPopup(popup);
            poiLayer.addLayer(marker);
        }
        poiLayer.addTo(mymap);

    });
};

var poiHidden = true;

var togglePOI = function() {
     if (poiHidden) {
         getPOI();
     }
     else {
         if (poiLayer !== undefined) {
             poiLayer.clearLayers()
         }
     }
     poiHidden = !poiHidden;
};

var update_time = function() {
    var date = new Date();
    return date.getTime();
};

var last_update = 0;
var waiting = false;

function reloadData() {
    // if pokestop not yet loaded or another pokemon update is not long ago, wait a sec
    if (pokedex === undefined || update_time() < last_update + 200) {
        var timeout = (pokedex === undefined) ? 100 : 1000;
        if (!waiting) {
            setTimeout(function () {
                reloadData();
            }, timeout);
        }
        return;
    }
    else {
        last_update = update_time();
    }
    if (!poiHidden) {
        getPOI();
    }
    getData();
}

var websocket_protocol = 'ws://';
if (location.protocol === 'https:') {
    websocket_protocol = 'wss://'
}

var updateSocket = new WebSocket(
websocket_protocol + window.location.host +
'/ws/update/');

updateSocket.onmessage = function(e) {
    var data = JSON.parse(e.data);
    console.log(data);
    if (data.type === 'change') {
        reloadData()
    }
};

reloadData();