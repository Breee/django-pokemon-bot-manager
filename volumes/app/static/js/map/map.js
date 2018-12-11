"use strict";

function MapCookie() {
    this.pokestopsHidden = getBooleanCookieValue('pokestopsHidden', true);
    this.gymsHidden = getBooleanCookieValue('gymsHidden', false);
    this.regularPokemonHidden = getBooleanCookieValue('regularPokemonHidden', false);
    this.ivPokemonHidden = getBooleanCookieValue('ivPokemonHidden', false);
    this.mapperHidden = getBooleanCookieValue('mapperHidden', true);
}

MapCookie.prototype.toggleCookieSetting = function (name) {
    this[name] = !this[name];
    setCookie(name, this[name], 365);
    return this[name]
};

function setCheckboxes () {
    var checkboxes = $( "input:checkbox" );
    for (var checkbox in checkboxes) {
        if (checkboxes.hasOwnProperty(checkbox)) {
            var cb = checkboxes[checkbox];
            if (cb.tagName === 'INPUT') {
                var cb_bool = mapCookie[cb.name];
                $(cb).attr( {checked: (!cb_bool)});
                $(cb).prop( {checked: (!cb_bool)});
            }
        }
    }

}

var mapCookie = new MapCookie();
setCheckboxes();

var csrftoken = getCookie('csrftoken');
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
});

var pokedex = undefined;
$.getJSON('/api/pokedex/', function (data) {
    pokedex = data;
});

var getPokemonData = function () {
    $.getJSON("/api/pokemon/spawns", function(data) {
        addPokemonsToMap(data)
    });
};

var getPointOfInterestData = function() {
    $.getJSON("/api/poi/all", function (data) {
        addPointsOfInterestToMap(data);
    });
};

var getMapperData = function() {
    $.getJSON("/api/mapper", function (data) {
        addMapperToMap(data);
    });
};


var togglePokestops = function() {
    var pokestopsHidden = mapCookie.toggleCookieSetting('pokestopsHidden');
    toggleMapLayer(pokestopLayer, pokestopsHidden);
};

var toggleGyms = function() {
    var gymsHidden = mapCookie.toggleCookieSetting('gymsHidden');
    toggleMapLayer(gymLayer, gymsHidden);
};

var toggleIVPokemon = function() {
    var ivPokemonHidden = mapCookie.toggleCookieSetting('ivPokemonHidden');
    toggleMapLayer(ivPokemonLayer, ivPokemonHidden);
};

var toggleRegularPokemon = function() {
    var regularPokemonHidden = mapCookie.toggleCookieSetting('regularPokemonHidden');
    toggleMapLayer(regularPokemonLayer, regularPokemonHidden);
};

var toggleMapper = function() {
    var mapperHidden = mapCookie.toggleCookieSetting('mapperHidden');
    toggleMapLayer(mapperLayer, mapperHidden);
};


var update_time = function() {
    var date = new Date();
    return date.getTime();
};

var last_update = 0;
var loading_initial = true;

function reloadData(data) {
    var model = data.model;
    var instance = data.instance;
        // if pokestop not yet loaded or another pokemon update is not long ago, wait a sec
        if (!loading_initial) {
            if (pokedex === undefined) {
                setTimeout(function () {
                    reloadData(data)
                }, 200);
                return
            }
            loading_initial = true;
            last_update = update_time();
            if (model === "PokemonSpawn") {
                getPokemonData();
            }
            else if (model === "PointOfInterest") {
               addPointOfInterestToMap(instance)
            }
            else if (model === "Mapper") {
                var marker = get_mapper_marker(instance);
                updateLayer(mapperLayer, mapperDict, marker, instance.id)
            }
            else if (model === "Quest") {
                parseQuestData(instance);
            }
            else {
                getPointOfInterestData();
                getPokemonData();
                getMapperData();
                getQuestInfo();
                waitForInitials();
            }
        }
}

function waitForInitials() {
    setTimeout(function () {
                    if (pokestopLayer !== undefined && gymLayer !== undefined &&
                        regularPokemonLayer !== undefined && ivPokemonLayer !== undefined &&
                        mapperLayer !== undefined) {
                        waitForInitials()
                    }
                    else {
                        loading_initial = false;
                    }
                },200)

}

var websocket_protocol = 'ws://';
if (location.protocol === 'https:') {
    websocket_protocol = 'wss://'
}

var updateSocket = new ReconnectingWebSocket(
websocket_protocol + window.location.host +
'/ws/update/');

updateSocket.onmessage = function(e) {
    var data = JSON.parse(e.data);
    console.log(data);
    if (data.type === 'change') {
        reloadData(data)
    }
};

reloadData({});

$( function() {
    $( "#datepicker" ).datepicker();
} );

mymap.on('moveend', function() {
    /*
     * TODO: Get only objects inside map bounds
     * bounds are stored in mymap.getBounds();
     * The api has to be changed to support this.
     * you can use a simple "is point in rectangle" function
     * shouldn't be too hard
     */
});