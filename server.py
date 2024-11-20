import json
from flask import Flask, render_template, request

from Pathfinding.PointOfInterest import POI
from Pathfinding.Itinerary import Itinerary

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('mainPage.html')

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/map')
def map():
    return render_template('map.html')

@app.post('/save-tourist-data')
def save_tourist_data():
    with open('data/tourist_data.json', 'r') as file:
        data = json.load(file)
    data.append(request.get_json())
    with open('data/tourist_data.json', 'w') as file:
        json.dump(data, file)

    return 'Data saved successfully!'

@app.get('/itinerary/<int:num_of_days>')
def itinerary(num_of_days: int):
    with open('Pathfinding/POIs.json', 'r') as file:
        data = json.load(file)
    POIs = []
    for entry in data['tourist_attractions']:
        POIs.append(POI(entry['name'], entry['type'], entry['position']['latitude'], entry['position']['longitude'], entry['tags']))
    it = Itinerary(POIs, num_of_days)
    return it.to_json()