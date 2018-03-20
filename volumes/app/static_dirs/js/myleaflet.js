"use strict"

var mymap = L.map('mapid').setView([48.0, 7.8], 13);
var layerGroup = undefined;

//var url = 'https://tiles.venezilu.de/styles/osm-bright/{z}/{x}/{y}.png'
var url = 'https://korona.geog.uni-heidelberg.de/tiles/roads/x={x}&y={y}&z={z}'
L.tileLayer(url, {

    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
    maxZoom: 18,
    id: 'openstreetmap'
}).addTo(mymap);

var getData = function () {
    $.getJSON("/api/pokepositions/", function(data) {
        if (layerGroup !== undefined) {
            layerGroup.clearLayers();
        }
        else {
            layerGroup = L.layerGroup()
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

getDataPerodically();