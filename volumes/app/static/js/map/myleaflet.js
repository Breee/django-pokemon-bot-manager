"use strict";


function MyLeaflet() {
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


    this.mymap = L.map('map', {
        center: [47.9960526, 7.8464833],
        zoom: 17
    });
    this.lastZoom = this.mymap.getZoom();

    var mapObjectTypes = [['ivPokemon', 1000], ['regularPokemon', 1000], ['pokestop',900], ['gym', 900], ['mapper', 900], ['quest', 1000], ['raid', 1000]];
    this.mapObjects = {};

    for (var object_type in mapObjectTypes) {
        var type = mapObjectTypes[object_type][0];
        var zIndex = mapObjectTypes[object_type][1];
        this.mapObjects[type] = new MapObject(mapCookie, type + 'Hidden', this.mymap, zIndex);
    }

    var url = 'https://maps.wikimedia.org/osm-intl/{z}/{x}/{y}.png';

    L.tileLayer(url, {
        attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
        maxZoom: 18,
        id: 'openstreetmap'
    }).addTo(this.mymap);

    var sidebar = L.control.sidebar('sidebar').addTo(this.mymap);

    this.getMapCorners = function () {
        var corners = {'top_left': this.mymap.getBounds().getNorthWest(),
                          'bottom_left': this.mymap.getBounds().getSouthWest(),
                          'top_right': this.mymap.getBounds().getNorthEast(),
                          'bottom_right': this.mymap.getBounds().getSouthEast()};
        return corners;
    };


    this.addMapObjectsToMap = function(data, model) {
        var pokestopObjectInstance = this.mapObjects['pokestop'];
        if (pokestopObjectInstance.layer === undefined) {
            pokestopObjectInstance.layer = L.markerClusterGroup({
                maxClusterRadius: 120,
                disableClusteringAtZoom: 17,
                iconCreateFunction: clusterIcon
            });
        }
        var gymObjectInstance = this.mapObjects['gym'];
        if (gymObjectInstance.layer === undefined) {
            gymObjectInstance.layer = L.markerClusterGroup({
                maxClusterRadius: 120,
                disableClusteringAtZoom: 15,
                iconCreateFunction: clusterIcon
            });
        }
        var raidObjectInstance = this.mapObjects['raid'];
        if (raidObjectInstance.layer === undefined) {
            raidObjectInstance.layer = L.markerClusterGroup({
                maxClusterRadius: 120,
                disableClusteringAtZoom: 15,
                iconCreateFunction: clusterIcon

            });
        }
        for (var i in data) {
            this.addSingleMapObjectToMap(data[i], model);
        }
        addLayersToMap(this);
    };

    this.addSingleMapObjectToMap = function(instance, model) {
        var marker = undefined;
        var pokestopDict = this.mapObjects['pokestop'].markers;
        var gymDict = this.mapObjects['gym'].markers;
        var raidDict = this.mapObjects['raid'].markers;
        var questDict = this.mapObjects['quest'].markers;
        var mapperDict = this.mapObjects['mapper'].markers;
        var ivPokemonDict = this.mapObjects['ivPokemon'].markers;
        var regularPokemonDict = this.mapObjects['regularPokemon'].markers;
        var pokestopLayer = this.mapObjects['pokestop'].layer;
        var gymLayer = this.mapObjects['gym'].layer;
        var raidLayer = this.mapObjects['raid'].layer;
        var ivPokemonLayer = this.mapObjects['ivPokemon'].layer;
        var regularPokemonLayer = this.mapObjects['regularPokemon'].layer;
        var mapperLayer = this.mapObjects['mapper'].layer;

        if (model === 'pokestop' || type === 'gym' ) {
            marker = get_poi_marker(instance, model);
            if (model === 'pokestop') {
                updateLayer(pokestopLayer, pokestopDict, marker, instance.external_id);
            } else if (type === 'gym') {
                updateLayer(gymLayer, gymDict, marker, instance.poi_id);
            }
        }
    };

    function addLayersToMap(_this) {
        for (var objectKey in _this.mapObjects) {
            if (_this.mapObjects.hasOwnProperty(objectKey)) {
                var mapObject = _this.mapObjects[objectKey];
                if (mapObject.layer !== undefined) {
                    mapObject.addToMap();
                }
            }
        }
    }


    function get_pokemon_marker(pokemon) {
        var popup = getPokemonPopupData(pokemon);
        var marker = L.marker([pokemon.latitude, pokemon.longitude],
            {
                title: pokedex[pokemon.pokemon_object - 1].name_german,
                icon: L.icon({
                    iconUrl: "/static/img/pokemons/" + pokemon.pokemon_object + '.png',
                    iconSize: [32, 32],
                    popupAnchor: [0, -15]
                })
            });
        marker.bindPopup(popup);
        return marker
    }

    function get_raid_marker(raid, lat, lon) {
        return L.marker([lat, lon],
            {
                title: pokedex[raid.pokemon_id - 1].name_german,
                icon: L.icon({
                    iconUrl: "/static/img/pokemons/" + raid.pokemon_id + '.png',
                    iconSize: [32, 32],
                    popupAnchor: [0, -15]
                })
            });
    }

    function updateLayer(layer, dict, marker, id) {
        if (dict.hasOwnProperty(id)) {
            var old_marker = dict[id];
            layer.removeLayer(old_marker);
            dict[id] = marker;
            layer.addLayer(marker);
        } else {
            dict[id] = marker;
            layer.addLayer(marker);
        }


    }

    var id_to_item = {
        701: {"ger": "Himmihberre", "en":"Razz Berry"},
        705: {"ger": "Sananabeere", "en":"Pinap Berry"},
        703: {"ger": "Nanabeere", "en":"Nana Berry"},
        708: {"ger": "Silberne Sananabeere", "en":"Silver Pinap Berry"},
        1301: {"ger": "Sonderbonbon", "en":"Rare Candy"},
        201: {"ger": "Beleber", "en":"Revive"},
        101: {"ger": "Trank", "en":"Potion"},
        102: {"ger": "Supertrank", "en":"Great Potion"},
        103: {"ger": "Hypertrank", "en":"Hyper Potion"},
        1: {"ger": "Pokeball", "en":"Pokeball"},
        2: {"ger": "Superball", "en":"Greatball"},
        3: {"ger": "Hyperball", "en":"Ultraball"},
    };

    function getItemName(id, language) {
        if (id_to_item[id] == undefined){
            return id;
        }
        var item_name = id_to_item[id][language];
        return item_name;
    }


    function get_poi_marker(poi, type) {
        var popup = "";
        var icon_url = '';
        var shadow_url = '';
        if (type === 'gym') {
            icon_url = "/static/img/map/gym.png";
            if (poi.park === true) {
                icon_url = "/static/img/map/ex_gym.png";
            }
        } else if (type === 'pokestop'){
            popup += "<div class=\"pokestop-popup text-center card\">";
            popup += "<div class=\"card-body\">";
            popup += "<h5 class=\"card-title\">"+ poi.name + "</h5>";
            var poi_img =  "<img src=\"" + poi.url + "\" class=\"rounded-circle\" alt=\"" + poi.name + "\"width=\"100\" height=\"100\">";

            if (poi.hasOwnProperty('quest')) {
                var quest = poi.quest;
                if (quest != null) {
                    var quest_reward = JSON.parse(quest.quest_reward)[0];
                    var reward_human_readable = "";
                    switch (quest_reward.type) {
                        case 2:
                            icon_url = "https://raw.githubusercontent.com/nileplumb/PkmnShuffleMap/master/PMSF_icons_large/rewards/reward_" + quest_reward.item.item + '_' + quest_reward.item.amount + ".png?raw=true";
                            reward_human_readable = quest_reward.item.amount+ "x "+ getItemName(quest_reward.item.item, 'en') ;
                            break;
                        case 3:
                            icon_url = "https://raw.githubusercontent.com/nileplumb/PkmnShuffleMap/master/PMSF_icons_large/rewards/reward_stardust_" + quest_reward.stardust + ".png?raw=true";
                            reward_human_readable = quest_reward.stardust + " Stardust";
                            break;
                        case 7:
                            var encounter_id = quest_reward.pokemon_encounter.pokemon_id;
                            icon_url = "https://raw.githubusercontent.com/nileplumb/PkmnShuffleMap/master/PMSF_icons_large/pokemon_icon_" + ("000" + encounter_id).slice(-3) + "_00.png?raw=true";
                            reward_human_readable = ("000" + encounter_id).slice(-3);
                            break;
                    }
                    var quest_figure = "<figure><img src=\"" + icon_url + "\" width=\"70\" height=\"70\" class='figure-img'>" +
                        "<figcaption class='figure-caption'>"
                        + reward_human_readable + "</figcaption></figure>" ;
                    var images = "<div class='row text-center justify-content-center'><div class='column'>" +
                        poi_img+"</div><div class='column'>" +
                        quest_figure+"</div></div>";
                    popup += images;
                    popup += "<p class='font-weight-bold'>Quest: "+ quest.quest_task + "</p>";
                    shadow_url = "/static/img/map/Pstop-quest-small.png";
                } else {
                    icon_url = "/static/img/map/Pstop.png";
                }
            }
            popup += "</div>";
            popup += "</div>";
        }

        var marker = L.marker([poi.lat, poi.lon],
            {
                title: poi.name,
                icon: L.icon({
                    iconUrl: icon_url,
                    shadowUrl: shadow_url,
                    iconSize: [35, 35],
                    shadowSize: [50, 50],
                    popupAnchor: [25, 0],
                    shadowAnchor: [0, 0],
                    iconAnchor: [5, -5]
                })
            });
        marker.bindPopup(popup);

         // send clicks on POI's to the server this is in preparation for Quests!
        //L.DomEvent.addListener(marker, 'click', function (event) {
        //    updateSocket.send(JSON.stringify({
        //        "type": "open_pokestop_request",
        //        "pokestop_id": poi.external_id
        //    }));
        //});
        return marker;
    }


    var getPokemonPopupData = function (pokemon) {
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
            var iv_proc = Math.round(((iv_sta + iv_att + iv_def) / 45) * 10000) / 100;
            var iv_str = '<b>IV:</b>' + iv_proc + '% ' + '(A' + iv_att + '|D' + iv_def + '|S' + iv_sta + ')<br>';
            var cp_str = '<b>CP:</b>' + pokemon.cp + '<br>';
        } else {
            iv_str = '';
            cp_str = '';
        }

        var maps_str = '<a href="https://www.google.com/maps/place/' + pokemon.latitude + ',' +
            pokemon.longitude + '" target="_blank" title="Open in Google Maps">' + 'Maps</a><br>';

        return '<h3>' + pokedex[pokemon.pokemon_object - 1].name_german + ' (' + pokemon.pokemon_object + ')' + '</h3>' +
            '<b>Despawn Time</b> ' + date_str + date.toLocaleTimeString('de-DE') + '<br>' +
            iv_str + cp_str + maps_str;
    };
    var getRaidPopupData = function (raid) {
        var date = new Date(raid.time_end);

        var today = new Date();
        var date_str = '';
        if (date.getDate() > today.getDate()) {
            date_str = date.toLocaleDateString('de-DE') + ' ';
        }

        var maps_str = '<a href="https://www.google.com/maps/place/' + raid.gym.latitude + ',' +
            raid.gym.longitude + '" target="_blank" title="Open in Google Maps">' + 'Maps</a><br>';

        return '<h3>level '+ raid.level +' raid' + pokedex[raid.pokemon_id - 1].name_german + ' (' + raid.pokemon_id + ')' + '</h3>' +
            '<b>Despawn Time</b> ' + date_str + date.toLocaleTimeString('de-DE') + '<br>' + maps_str;
    };


}

MyLeaflet.prototype.addMapObjectsToMap = function(data, model) {
    this.addMapObjectsToMap(data, model);
};
MyLeaflet.prototype.addSingleMapObjectToMap = function(instance, model) {
    this.addSingleMapObjectToMap(instance, model);
};
MyLeaflet.prototype.allLayersSet = function allLayersSet() {
        var bool = true;
        for (var key in this.mapObjects) {
            if (this.mapObjects.hasOwnProperty(key)) {
                var mapObject = this.mapObjects[key];
                bool = bool && mapObject.layer !== undefined
            }
        }
        return bool;
    };

MyLeaflet.prototype.toggleMapObjectsHidden = function(type) {
    if (this.mapObjects.hasOwnProperty(type)) {
        this.mapObjects[type].toggleHidden();
    }
};

function MapObject(cookie, cookieName, map, zIndex) {
    this.objects = {};
    this.markers = {};
    this.layer = undefined;
    this.cookie = cookie;
    this.cookieName = cookieName;
    this.onMap = false;
    this.map = map;
    this.zIndex = zIndex
}

MapObject.prototype.addToMap = function () {
        if (this.isHidden()) {
            if (this.onMap) {
                this.layer.remove(this.map);
            }
        } else {
            if (!this.onMap) {
                this.layer.addTo(this.map);
            }
        }
        this.onMap = !this.onMap;
    };

MapObject.prototype.isHidden = function () {
    return this.cookie[this.cookieName];
};

MapObject.prototype.toggleHidden = function () {
    this.cookie.toggleCookieSetting(this.cookieName);
    this.addToMap()
};