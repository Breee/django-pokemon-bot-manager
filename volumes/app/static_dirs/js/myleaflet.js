var mymap = L.map('mapid').setView([48.0, 7.8], 13);
  L.tileLayer('https://tiles.venezilu.de/styles/osm-bright/{z}/{x}/{y}.png', {
        attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
        maxZoom: 18,
        id: 'openstreetmap',
  }).addTo(mymap);
  $.getJSON("http://localhost:8000/api/pokepositions", function(data) {
    for (var i in data) {
        var pokemon = data[i];
        var popup = "" + pokemon.poke_despawn_time + "<br>" +
                    "" + pokemon.poke_nr;
        L.marker([pokemon.poke_lat, pokemon.poke_lon],
            {title: "test",
             icon: L.icon({
                 iconUrl: "/static/img/pokemons/" + pokemon.poke_nr + '.png',
                 iconSize: [32, 32],
                 popupAnchor: [-3, -76]
             }) }).addTo(mymap).bindPopup(popup);
    }
  });
