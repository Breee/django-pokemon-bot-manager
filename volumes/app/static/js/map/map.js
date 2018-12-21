"use strict";

function MapCookie() {
    this.pokestopHidden = getBooleanCookieValue('pokestopHidden', true);
    this.gymHidden = getBooleanCookieValue('gymHidden', false);
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

var myLeaflet = new MyLeaflet();

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

function getData(type) {
    function parseData(data) {
        myLeaflet.addMapObjectsToMap(data, type);
    }
    if (type === 'PokemonSpawn') {
        $.getJSON("/api/pokemon/spawns", parseData);
    }
    else if (type === 'PointOfInterest') {
        $.getJSON("/api/poi/all", parseData);
    }
    else if (type === 'Mapper') {
        $.getJSON("/api/mapper", parseData);
    }
    else if (type === 'Quest') {
        $.getJSON('/api/quest/', parseData);
    }
    else if (type === 'Raid') {
        $.getJSON('/api/raid/', function (data) {
            console.log(data)
        });
    }
    else {
        console.log('NotImplementedError: ' + type)
    }
}

var toggleMapObjects = function(type) {
    myLeaflet.toggleMapObjectsHidden(type);
};

var websocket_protocol = 'ws://';
if (location.protocol === 'https:') {
    websocket_protocol = 'wss://'
}

var updateSocket = new ReconnectingWebSocket(
websocket_protocol + window.location.host +
'/ws/update/');

function reloadData(data) {
    var model = data.model;
    var instance = data.instance;
        // if pokestop not yet loaded or another pokemon update is not long ago, wait a sec
        if (pokedex === undefined) {
            setTimeout(function () {
                reloadData(data)
            }, 200);
            return
        }
        if (model === "PokemonSpawn") {
            myLeaflet.addSingleMapObjectToMap(instance, model);
        }
        else if (model === "PointOfInterest") {
            myLeaflet.addSingleMapObjectToMap(instance, model);
        }
        else if (model === "Mapper") {
            myLeaflet.addSingleMapObjectToMap(instance, model);
        }
        else if (model === "Quest") {
            myLeaflet.addSingleMapObjectToMap(instance, model);
        }
        /*
            this condition should only fit in initial state
         */
        else {
            getData('PointOfInterest');
            getData('PokemonSpawn');
            getData('Mapper');
            getData('Quest');
            waitForInitials();
        }
}

function waitForInitials() {
    setTimeout(function () {
    if (myLeaflet.allLayersSet) {

        // add this function after initials are loaded to avoid errors
        updateSocket.onmessage = function(e) {
            var data = JSON.parse(e.data);
            if (data.type === 'change') {
                    console.log(data.type , data.model);
                    reloadData(data)
            }
        };
    }
    else {
        waitForInitials();
    }
},200)

}


reloadData({});

$( function() {
    $( "#datepicker" ).datepicker();
} );

/*mymap.on('moveend', function() {
    /*
     * TODO: Get only objects inside map bounds
     * bounds are stored in mymap.getBounds();
     * The api has to be changed to support this.
     * you can use a simple "is point in rectangle" function
     * shouldn't be too hard
     */
/*});*/