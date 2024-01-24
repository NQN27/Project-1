document.addEventListener('DOMContentLoaded', function() {
    var map = L.map('map').setView([21.0314522, 105.8529442], 13);
    
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 18,
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    var startMarker, endMarker;

    map.on('click', function(e) {
        if (!startMarker) {
            startMarker = L.marker(e.latlng).addTo(map).bindPopup('Start').openPopup();
        } else if (!endMarker) {
            endMarker = L.marker(e.latlng).addTo(map).bindPopup('End').openPopup();
        } else {
            map.removeLayer(startMarker);
            map.removeLayer(endMarker);
            startMarker = L.marker(e.latlng).addTo(map).bindPopup('Start').openPopup();
            endMarker = null;
        }
    });

    document.getElementById('findPath').addEventListener('click', function() {
        if (startMarker && endMarker) {
            var start = startMarker.getLatLng();
            var end = endMarker.getLatLng();
            fetch('/find_path', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    start: [start.lat, start.lng],
                    end: [end.lat, end.lng]
                })
            })
            .then(response => response.json())
            .then(data => {
                // Add the line to the map
                L.polyline(data.path, {color: 'blue'}).addTo(map);
                // Clear markers
                map.removeLayer(startMarker);
                map.removeLayer(endMarker);
                startMarker = endMarker = null;
            })
            .catch(error => console.error('Error:', error));
        } else {
            alert('Please select both a start and an end point.');
        }
    });
});
