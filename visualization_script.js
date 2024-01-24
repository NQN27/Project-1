let currentStep = 0;
let states = [];
let visualizationInterval;
let intervalSpeed = 1000; // Interval speed in milliseconds
let map;

function loadJSON(filename, callback) {   
    const xobj = new XMLHttpRequest();
    xobj.overrideMimeType("application/json");
    xobj.open('GET', filename, true);
    xobj.onreadystatechange = function () {
        if (xobj.readyState == 4 && xobj.status == "200") {
            callback(xobj.responseText);
        }
    };
    xobj.send(null);
}

function updateVisualization() {
    if (currentStep < states.length) {
        let state = states[currentStep];

        // Clear previous data
        map.eachLayer(function (layer) {
            if (layer instanceof L.Marker || layer instanceof L.Polyline) {
                map.removeLayer(layer);
            }
        });

        // Add polyline for the path
        let pathLatLngs = state.path.map(coords => [coords[0], coords[1]]);
        L.polyline(pathLatLngs, { color: 'blue', weight: 4 }).addTo(map);

        // Add marker for the current node
        L.circleMarker(state.current, { color: 'red', radius: 6 }).addTo(map);

        // Add markers for the open set
        state.open_set.forEach(coord => {
            L.circleMarker(coord, { color: 'green', radius: 4 }).addTo(map);
        });

        currentStep++;
    } else {
        clearInterval(visualizationInterval);
    }
}

function loadSearch(type) {
    clearInterval(visualizationInterval);
    currentStep = 0;
    loadJSON(type + '_states.json', function(response) {
        states = JSON.parse(response);
        updateVisualization();
        visualizationInterval = setInterval(updateVisualization, intervalSpeed);
    });
}

document.addEventListener('DOMContentLoaded', function() {
    map = L.map('map').setView([21.0314522, 105.8529442], 13);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 18,
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    document.getElementById('a_star_plus').addEventListener('click', function() { loadSearch('a_star_plus'); });
    document.getElementById('ucs').addEventListener('click', function() { loadSearch('ucs'); });
    document.getElementById('a_star_memory').addEventListener('click', function() { loadSearch('a_star_memory'); });
    document.getElementById('a_star').addEventListener('click', function() { loadSearch('a_star'); });

    // Optionally, load one of the searches by default
    // loadSearch('a_star_plus');
});
