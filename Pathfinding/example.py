import json

from Graph import Graph
from PointOfInterest import POI

with open('POIs.json', 'r') as file:
    data = json.load(file)

POIs = []
for entry in data['tourist_attractions']:
    POIs.append(POI(entry['name'], entry['type'], entry['position']['latitude'], entry['position']['longitude'], entry['tags']))

graph = Graph(POIs)
optimal_path = graph.optimal_path(0)
print(optimal_path)