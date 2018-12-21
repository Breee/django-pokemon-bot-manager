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


    var mymap = L.map('map').setView([47.9960526, 7.8464833], 17);

    var mapObjectTypes = ['ivPokemon', 'regularPokemon', 'pokestop', 'gym', 'mapper', 'quest', 'raid'];
    this.mapObjects = {};

    for (var object_type in mapObjectTypes) {
        var type = mapObjectTypes[object_type];
        this.mapObjects[type] = new MapObject(mapCookie, type + 'Hidden', mymap);
    }

    var url = 'https://maps.wikimedia.org/osm-intl/{z}/{x}/{y}.png';

    L.tileLayer(url, {
        attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
        maxZoom: 18,
        id: 'openstreetmap'
    }).addTo(mymap);

    var sidebar = L.control.sidebar('sidebar').addTo(mymap);

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

    this.addMapObjectsToMap = function(data, model) {
        if (model === 'PointOfInterest') {
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
        } else if (model === 'PokemonSpawn') {
            var ivPokemonObjectInstance = this.mapObjects['ivPokemon'];
            var regularPokemonObjectInstance = this.mapObjects['regularPokemon'];
            if (regularPokemonObjectInstance.layer === undefined && ivPokemonObjectInstance.layer === undefined) {
                regularPokemonObjectInstance.layer = L.layerGroup();
                ivPokemonObjectInstance.layer = L.layerGroup();
            }
        } else {
            var mapObjectInstance = this.mapObjects[model.toLowerCase()];
            mapObjectInstance.layer = new L.LayerGroup();
        }
        for (var i in data) {
            if (data.hasOwnProperty(i)) {
                var instance = data[i];
                this.addSingleMapObjectToMap(instance, model);
            }
        }
        addLayersToMap(this);

    };

    this.addSingleMapObjectToMap = function(instance, model) {
        var marker = undefined;
        var pokestopDict = this.mapObjects['pokestop'].markers;
        var gymDict = this.mapObjects['gym'].markers;
        var questDict = this.mapObjects['quest'].markers;
        var mapperDict = this.mapObjects['mapper'].markers;
        var ivPokemonDict = this.mapObjects['ivPokemon'].markers;
        var regularPokemonDict = this.mapObjects['regularPokemon'].markers;

        var pokestopLayer = this.mapObjects['pokestop'].layer;
        var gymLayer = this.mapObjects['gym'].layer;
        var ivPokemonLayer = this.mapObjects['ivPokemon'].layer;
        var regularPokemonLayer = this.mapObjects['regularPokemon'].layer;
        var mapperLayer = this.mapObjects['mapper'].layer;

        if (model === 'PokemonSpawn') {
            marker = get_pokemon_marker(instance);
            if (instance.individual_stamina !== null || instance.individual_attack !== null || instance.individual_defense !== null) {
                updateLayer(ivPokemonLayer, ivPokemonDict, marker, instance.encounter_id)
            } else {
                updateLayer(regularPokemonLayer, regularPokemonDict, marker, instance.encounter_id)
            }
        } else if (model === 'PointOfInterest') {
            marker = get_poi_marker(instance);
            var type = instance.type;
            if (type === 'pokestop') {
                if (questDict.hasOwnProperty(instance.poi_id)) {
                    setQuestPopup(instance.poi_id, this);
                }
                updateLayer(pokestopLayer, pokestopDict, marker, instance.poi_id);
            } else if (type === 'gym') {
                updateLayer(gymLayer, gymDict, marker, instance.poi_id);
            }
        } else if (model === 'Mapper') {
            marker = get_mapper_marker(instance);
            updateLayer(mapperLayer, mapperDict, marker, instance.id);
        } else if (model === 'Quest') {
            var poi_id = instance.pokestop_id;

            if (pokestopDict.hasOwnProperty(poi_id)) {
                marker = pokestopDict[poi_id];
                if (!this.mapObjects['quest'].markers.hasOwnProperty(poi_id)) {
                    var popup = marker._popup._content;
                    questDict[poi_id] = [marker, popup, instance];
                }
                setQuestPopup(poi_id, this);

                updateLayer(pokestopLayer, pokestopDict, marker, poi_id);
            }
        } else {
            console.log('NotImplementedError: ' + instance)
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
        } else {
            dict[id] = marker;
            layer.addLayer(marker);
        }


    }


    function setQuestPopup(poi_id, _this) {
        if (!_this.mapObjects['quest'].markers.hasOwnProperty(poi_id)) {
            return
        }
        var marker = questDict[poi_id][0];
        var popup = questDict[poi_id][1];
        var quest = questDict[poi_id][2];
        popup += 'Quest: ' + quest.quest_template + '<br>';

        var reward;
        var quest_rewards = JSON.parse(quest.quest_rewards);
        switch (quest_rewards.type) {
            case 2:
                var quest_item_id_name = ("000" + quest_rewards.item.item).slice(-4);
                reward = quest_rewards.item.amount + 'x ' +
                    '<img src="/static/img/Texture2D/Item_' + quest_item_id_name + '.png"' +
                    ' class="quest_reward" alt="item_' + quest_item_id_name + '" align="middle">';
                break;
            case 3:
                reward = quest_rewards.stardust +
                    ' <img src="/static/img/Texture2D/stardust_painted.png" alt="stardust" ' +
                    'class="quest_reward" align="middle">';
                break;
            case 7:
                reward = '<img src="/static/img/pokemons/' + quest.quest_pokemon_id + '.png"' +
                    ' class="quest_reward" alt="item_' +
                    pokedex[quest.quest_pokemon_id].name_german + '" align="middle">';
                break;
        }
        popup += 'Reward: ' + reward + '<br>';
        marker._popup.setContent(popup);
        marker.setIcon(L.icon({
                iconUrl: '/static/img/Texture2D/pokestop_near.png',
                iconSize: [32, 32],
                popupAnchor: [-3, -76]
            }
        ));
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


    function get_poi_marker(poi) {
        var type = poi.type;
        var popup = "" + poi.name + "<br>";
        popup += (poi.description !== '') ? '' : poi.description + '<br>';
        if (poi.image_url !== null) {
            popup += '<img style="width:125px; height: 125px; object-fit: cover;" src="' + poi.image_url + '" /><br>'
        }

        var icon_url = '';
        if (type === 'gym') {
            icon_url = "/static/img/map/gym.png";
            if (poi.park === true) {
                icon_url = "/static/img/map/ex_gym.png";
            }
        } else {
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

        // send clicks on POI's to the server
        // this is in preparation for Quests!
        L.DomEvent.addListener(marker, 'click', function (event) {
            updateSocket.send(JSON.stringify({
                "type": "click",
                "poi": poi.name
            }));
        });
        return marker;
    }


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

function MapObject(cookie, cookieName, map) {
    this.objects = {};
    this.markers = {};
    this.layer = undefined;
    this.cookie = cookie;
    this.cookieName = cookieName;
    this.onMap = false;
    this.map = map;
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