let map;
let directionsService;
let directionsRenderer;

let advancedMarkerElement;
let pinElement;

let currentDay = 0;
const data = [];
const routes = {};
let markers = [];
const centerCoords = { lat: 0, lng: 0 };

const days = document.getElementById('days');
const list = document.getElementById('list');
const form = document.getElementById('form');
const numOfDaysHandle = document.getElementById('num-of-days');
const cityNameHandle = document.getElementById('city-name');
const touristTypeHandle = document.getElementById('tourist-type');

const getData = async () => {
    const params = new URLSearchParams({
        "city-name": cityNameHandle.value,
        "num-of-days": numOfDaysHandle.value,
        "tourist-type": touristTypeHandle.value
    }).toString();

    await fetch('/locations/?' + params)
        .then((res) => res.json())
        .then((json) => {
            // list.innerHTML = '';
            // let i = 0;
            for (const day of json) {
                const dailyList = [];
                for (const poi of day) {
                    dailyList.push({
                        'lat': poi['position']['latitude'],
                        'lon': poi['position']['longitude'],
                        'name': poi['name'],
                        'id': poi['id']
                    });
                }
                data.push(dailyList);
            }

            // for (const day of json) {
            //     // const dailyList = document.createElement('ol');
            //     // const header = document.createElement('h3');
            //     // header.innerHTML = `Day ${i + 1}:`;
            //     // dailyList.appendChild(header);
                
            //     const dailyList = [];
            //     for (const poi of day) {
            //         const { latitude, longitude } = poi['position'];
            //         const name = poi['name'];
            //         const { hour, minute } = poi['time'];

            //         const item = document.createElement('li');
            //         // item.innerHTML = `${hour}:${minute} - ${name}`;
            //         item.innerHTML = name
            //         // dailyList.appendChild(item);
            //     }
            //     // list.appendChild(dailyList);
            //     i++;
            // }
        });
};

const getRoute = (prev, next) => (event) => {
    const request = {
        origin: { lat: prev['lat'], lng: prev['lon'] },
        destination: { lat: next['lat'], lng: next['lon'] },
        travelMode: 'TRANSIT',
        // transitOptions: {
        // departureTime: new Date(), // Optionally set the departure time
        // },
    };

    if (directionsRenderer != undefined) {
        directionsRenderer.setMap(null);
    }
    
    directionsRenderer = new google.maps.DirectionsRenderer({
        map: map
    });

    // Get directions and render on the map
    directionsService.route(request, function (response, status) {
        if (status === google.maps.DirectionsStatus.OK) {
            directionsRenderer.setDirections(response);
        } else {
            alert("Directions request failed due to " + status);
        }
    });
}

async function initMap() {
    const { Map } = await google.maps.importLibrary("maps");
    const { AdvancedMarkerElement, PinElement } = await google.maps.importLibrary("marker");

    advancedMarkerElement = AdvancedMarkerElement;
    pinElement = PinElement;

    map = new Map(document.getElementById("map"), {
        center: centerCoords,
        zoom: 12,
        mapId: 'MAPID'
    });
    directionsService = new google.maps.DirectionsService();
    // directionsRenderer = new google.maps.DirectionsRenderer({
    //     map: map
    // });

    let i = 1;
    data[currentDay].forEach(x => {
        const pin = new PinElement({
            glyph: `${i++}`,
            glyphColor: 'white'
        });
        const marker = new AdvancedMarkerElement({
            map,
            position: {
                lat: x['lat'],
                lng: x['lon']
            },
            title: x['name'],
            content: pin.element
        });
        markers.push(marker);
    });
}
  
// initMap();

const changeDay = (i) => (event) => {
    event.preventDefault();

    if (currentDay == i) return;

    if (directionsRenderer != undefined) {
        directionsRenderer.setMap(null);
        directionsRenderer = undefined;
    };

    list.innerHTML = '';
    let k = 0;
    data[i].forEach(x => {
        const li = document.createElement('li');
        li.innerHTML = x.name;
        if (k == 0) {
            li.addEventListener('click', () => {
                // directionsRenderer.setDirections(null);
                if (directionsRenderer != undefined) {
                    directionsRenderer.setMap(null);
                    directionsRenderer = undefined;
                };
            });
        } else {
            li.addEventListener('click', getRoute(data[i][k - 1], data[i][k]));
        }

        // list.innerHTML += `<li>${x.name}</li>`;
        list.appendChild(li);
        k++;
    });

    currentDay = i;

    markers.forEach(x => x.setMap(null));
    markers = [];

    let j = 1;
    data[i].forEach(x => {
        const pin = new pinElement({
            glyph: `${j++}`,
            glyphColor: 'white'
        });
        const marker = new advancedMarkerElement({
            map,
            position: {
                lat: x['lat'],
                lng: x['lon']
            },
            title: x['name'],
            content: pin.element
        });
        markers.push(marker);
    });
};

form.addEventListener('submit', async (event) => {
    event.preventDefault();
    await getData();
    let i = 0;
    data.forEach(day => {
        const dayButton = document.createElement('button');
        dayButton.innerHTML = i + 1;
        dayButton.addEventListener('click', changeDay(i));
        days.appendChild(dayButton);
        i++
    });

    list.innerHTML = '';
    let k = 0;
    data[0].forEach(x => {
        const li = document.createElement('li');
        li.innerHTML = x.name;
        if (k == 0) {
            li.addEventListener('click', () => {
                // directionsRenderer.setDirections(null);
                if (directionsRenderer != undefined) {
                    directionsRenderer.setMap(null);
                    directionsRenderer = undefined;
                };
            });
        } else {
            li.addEventListener('click', getRoute(data[0][k - 1], data[0][k]));
        }

        // list.innerHTML += `<li>${x.name}</li>`;
        list.appendChild(li);
        k++;
    });

    centerCoords.lat = data[0][0]['lat'];
    centerCoords.lng = data[0][0]['lon'];

    initMap();
})