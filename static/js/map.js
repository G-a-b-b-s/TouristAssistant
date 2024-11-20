const map = L.map('map').setView([50.054166, 19.935083], 13);
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

const list = document.getElementById('list');
const form = document.getElementById('form');
const numOfDaysHandle = document.getElementById('num-of-days');

const pointsOfInterest = [];
let i = 1;

const getData = (numOfDays) => fetch('/itinerary/' + numOfDays)
    .then((res) => res.json())
    .then((json) => {
        list.innerHTML = '';
        i = 1;

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
    });

form.addEventListener('submit', (event) => {
    event.preventDefault();
    getData(numOfDaysHandle.value)
})

getData(numOfDaysHandle.value)