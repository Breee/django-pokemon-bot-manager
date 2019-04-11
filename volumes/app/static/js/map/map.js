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
'/ws/update/pokestops');

if (myLeaflet.allLayersSet) {
    updateSocket.onmessage = function(e) {
        var data = JSON.parse(e.data);
        if (data.type === 'viewport_information_request') {
            console.log(data.type , data.text);
            var msg_type = "viewport_information_answer";
            var corners = {'top_left': myMap.getBounds().getNorthWest(),
                'bottom_left': myMap.getBounds().getSouthWest(),
                'top_right': myMap.getBounds().getNorthEast(),
                'bottom_right': myMap.getBounds().getSouthEast()};
            var msg = {"type" : msg_type, 'corners' : corners};
            updateSocket.send(JSON.stringify(msg));
        }
        else if (data.type === 'pokestops'){
            var pokestops = data.pokestops;
            console.log(pokestops);
            myLeaflet.addMapObjectsToMap(pokestops,'pokestop');
            //pokestops.forEach(el => {
            //    el.type = 'pokestop';
            //    myLeaflet.addSingleMapObjectToMap(el,'PointOfInterest')
            //})
        }
    };

    myMap.on('moveend', function() {
        var msg_type = "viewport_information_answer";
        var currZoom = myMap.getZoom();
        var diff = myMap.lastZoom - currZoom;
        if(diff >= 0){
  	       console.log('Moved or zoomed out');
  	       // Center of the map
  	       var center = myMap.getCenter();
  	       // Corners of the map
  	       var corners = {'top_left': myMap.getBounds().getNorthWest(),
            'bottom_left': myMap.getBounds().getSouthWest(),
            'top_right': myMap.getBounds().getNorthEast(),
            'bottom_right': myMap.getBounds().getSouthEast()};
           var msg = {"type" : msg_type, 'corners' : corners, 'center' : center};
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
