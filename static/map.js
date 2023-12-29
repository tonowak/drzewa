// EPSG:2180
let polishCoordinates = "+proj=tmerc +lat_0=0 +lon_0=19 +k=0.9993 +x_0=500000 +y_0=-5300000 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs +type=crs";

let map = L.map('map').setView([52.231714, 21.003478], 16);

const tiles = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);


const popup = L.popup();

function onMapClick(e) {
    let projectedCoordinates = proj4(polishCoordinates, [e.latlng.lng, e.latlng.lat]);
    let x = projectedCoordinates[0];
    let y = projectedCoordinates[1];

    fetch(`/query/${x}/${y}`)
        .then(response => response.json())
        .then(data => {
            // Display the response in a popup
            popup
                .setLatLng(e.latlng)
                .setContent(data['description'])
                .openOn(map);
        });
}

map.on('click', onMapClick);