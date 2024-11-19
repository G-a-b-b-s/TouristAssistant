import json

from Itinerary import Itinerary
from PointOfInterest import POI

with open('POIs.json', 'r') as file:
    data = json.load(file)

POIs = []
for entry in data['tourist_attractions']:
    POIs.append(POI(entry['name'], entry['type'], entry['position']['latitude'], entry['position']['longitude'], entry['tags']))

itinerary = Itinerary(POIs, 3)
print(itinerary)