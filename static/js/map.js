const KEY = '5b3ce3597851110001cf6248c1165c3152674d6f8772a009456e8361';
const router = new L.Routing.OSRMv1(KEY);

const colors = ['red', 'blue', 'green', 'purple', 'darkred', 'darkgreen', 'darkpurple'];

const map = L.map('map').setView([50.054166, 19.935083], 13);
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

const list = document.getElementById('list');
const form = document.getElementById('form');
const numOfDaysHandle = document.getElementById('num-of-days');

const routes = [];

const getData = (numOfDays) => fetch('/itinerary/' + numOfDays)
    .then((res) => {
        console.log(res.body);;
        return res.json();
    })
    .then((json) => {
        list.innerHTML = '';
        let i = 0;
        
        for (const route of routes)
            map.removeControl(route);

        for (const day of json) {
            const dailyList = document.createElement('ol');
            const color = colors[i];
            const header = document.createElement('h3');
            header.innerHTML = `Day ${i + 1}:`;
            dailyList.appendChild(header);

            const routeCoordinates = [];
            const names = [];

            for (const poi of day) {
                const { latitude, longitude } = poi['position'];
                const name = poi['name'];

                names.push(name);
                routeCoordinates.push(L.latLng(latitude, longitude));

                const item = document.createElement('li');
                item.innerHTML = name;
                dailyList.appendChild(item);
            }
            list.appendChild(dailyList);

            const route = L.Routing.control({
                waypoints: routeCoordinates,
                router: router,
                formatter: null,
                routeWhileDragging: false,
                fitSelectedRoutes: false,
                addWaypoints: false,
                createMarker: (i, waypoint, n) => {
                    const marker = L.marker(waypoint.latLng, {
                        icon: L.AwesomeMarkers.icon({
                            icon: 'plus-circled',
                            markerColor: color,
                            prefix: 'ion'
                        })
                    });
                    marker.bindPopup(names[i]);
                    return marker;
                },
                lineOptions: {
                    styles: [
                        { color: color, opacity: 0.7, weight: 5}
                    ]
                }
            });
            route.addTo(map);
            routes.push(route);
            i++;
        }
    });

form.addEventListener('submit', (event) => {
    event.preventDefault();
    getData(numOfDaysHandle.value)
});

getData(numOfDaysHandle.value);
