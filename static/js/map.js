const map = L.map('map').setView([50.054166, 19.935083], 13);
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);
['tourist_attractions']
const list = document.getElementById('list');

const pointsOfInterest = [];
let i = 1;

fetch('/itinerary/3')
    .then((res) => res.json())
    .then((json) => {
        for (const day of json) {
            const dailyList = document.createElement('ol');

            const header = document.createElement('h3');
            header.innerHTML = `Day ${i++}:`;
            dailyList.appendChild(header);

            for (const poi of day) {
                const { latitude, longitude } = poi['position'];
                const name = poi['name'];
    
                const marker = L.marker([latitude, longitude]).addTo(map);
                marker.bindPopup(name).openPopup();
                pointsOfInterest.push(marker);
    
                const item = document.createElement('li');
                item.innerHTML = name;
                dailyList.appendChild(item);
            }
            list.appendChild(dailyList);
        }
    })
