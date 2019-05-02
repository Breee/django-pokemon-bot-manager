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
var myMap = myLeaflet.mymap;

console.log(myMap.getBounds());

var csrftoken = getCookie('csrftoken');
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
});


var toggleMapObjects = function(type) {
    myLeaflet.toggleMapObjectsHidden(type);
};

var websocket_protocol = 'ws://';
if (location.protocol === 'https:') {
    websocket_protocol = 'wss://'
}

var updateSocket = new ReconnectingWebSocket(
websocket_protocol + window.location.host +
'/ws/update/map');


if (myLeaflet.allLayersSet) {
    updateSocket.onmessage = function(e) {
        var data = JSON.parse(e.data);
        if (data.type === 'viewport_information_request') {
            var msg_type = "viewport_information_answer";
            var corners = myLeaflet.getMapCorners();
            var msg = {"type" : msg_type, 'corners' : corners};
            updateSocket.send(JSON.stringify(msg));
        }
        else if (data.type === 'pokestops'){
            var pokestops = data.pokestops;
            myLeaflet.addMapObjectsToMap(pokestops,'pokestop');
        }
        else if (data.type === 'gyms') {
            var gyms = data.gyms;
            myLeaflet.addMapObjectsToMap(gyms, 'gym');
        }
        else if (data.type === 'change'){
            myLeaflet.addMapObjectsToMap(data.instance,data.model);
            //myMap.invalidateSize();
        }

    };

    myMap.on('moveend', function() {
        var currZoom = myMap.getZoom();
        var diff = myMap.lastZoom - currZoom;
        if(diff >= 0){
  	       console.log('Moved or zoomed out');
  	       // Corners of the map
  	       var corners = myLeaflet.getMapCorners();
           var msg = {"type" : "viewport_information_answer", 'corners' : corners};
           updateSocket.send(JSON.stringify(msg));
        } else if(diff < 0) {
            // do nothing if zoomed in.
  	       console.log('zoomed in');
        } else {
            // do nothing if nothing changed.
  	       console.log('no change');
        }
        myMap.lastZoom = currZoom;
    });
}
