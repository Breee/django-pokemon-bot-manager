"use strict"

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

var getData = function () {
    $.getJSON("/api/pokemon/spawns", function(data) {
        if (layerGroup !== undefined) {
            layerGroup.clearLayers();
        }
        else {
            layerGroup = L.markerClusterGroup();
        }
        for (var i in data) {
            var pokemon = data[i];
            var popup = "" + pokemon.poke_despawn_time + "<br>" +
                "" + pokemon.poke_nr;
            var marker = L.marker([pokemon.poke_lat, pokemon.poke_lon],
                {title: "test",
                    icon: L.icon({
                        iconUrl: "/static/img/pokemons/" + pokemon.poke_nr + '.png',
                        iconSize: [32, 32],
                        popupAnchor: [-3, -76]
                    }) });
            marker.bindPopup(popup);
            layerGroup.addLayer(marker);
        }
        layerGroup.addTo(mymap);

    });
};

var getDataPerodically = function() {
    setTimeout(function () {

            getData();
            getDataPerodically()
        }
            , 1000);
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

getPOI();

var poiHidden = false;

var togglePOI = function() {
     if (poiHidden) {
         getPOI();
     }
     else {
         if (poiLayer !== undefined) {
             poiLayer.clearLayers()
         }
     }
};