from typing import List
from datetime import datetime
import asyncio
import json

import googlemaps.distance_matrix
import requests
from numpy import argmin
from traveltimepy import TravelTimeSdk, Location, Coordinates, CyclingPublicTransport, Property
import googlemaps

from Pathfinding.PointOfInterest import POI

APP_ID = "3cdde15e"
API_KEY = "e8ac78393d22ef73de21cf68fb8aadd6"
GOOGLE_API_KEY = 'AIzaSyCUws2hUjBLhWoiMCxt2qnPQYjI4TCTCbY'
GOOGLE_GEOCODE_URL = "https://maps.googleapis.com/maps/api/geocode/json"
# {
#     "name": "Wieliczka Salt Mine",
#     "type": "Natural Site",
#     "position": {
#         "latitude": 49.983056,
#         "longitude": 20.055000
#     },
#     "tags": ["salt mine", "UNESCO", "underground", "tour"]
# },
# {
#     "name": "Benedictine Abbey in Tyniec",
#     "type": "Monastery",
#     "position": {
#         "latitude": 50.009778,
#         "longitude": 19.798833
#     },
#     "tags": ["monastery", "religion", "history", "scenic"]
# },

class Locations:
    pois: List[POI]
    ids: List[str]
    opening_hours = []
    matrix: List[List[int]]

    def __init__(self, pois: List[POI]):
        self.pois = pois
        self.ids = []
        self.opening_hours = []
        self.matrix = [[0 for _ in range(len(self.pois))]
            for _ in range(len(self.pois))]
        # self.get_place_ids()
        self.get_opening_hours()
        self.get_distance_matrix()
        # asyncio.run(self.fetch_distance())
    
    def get_distance_matrix(self):
        origins = [x.id for x in self.pois]
        destinations = [x.id for x in self.pois]
        url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins="
        url += f"place_id:{origins[0]}"
        for id in origins[1:]:
            url += f"|place_id:{id}"
        url += "&destinations="
        url += f"place_id:{destinations[0]}"
        for id in destinations[1:]:
            url += f"|place_id:{id}"
        url += f"&key={GOOGLE_API_KEY}"
        result = requests.get(url)
        if result.status_code == 200:
            data = result.json()
            for i, row in enumerate(data['rows']):
                for j, value in enumerate(row['elements']):
                    # if value['status'] == 'OK':
                    self.matrix[i][j] = int(value['duration']['value']) if value['status'] == 'OK' else float('inf')
        else:
            print("Distance matrix error")
        

    async def fetch_distance(self):
        sdk = TravelTimeSdk(APP_ID, API_KEY)

        locations: List[Location] = []
        for poi in self.pois:
            locations.append(Location(id=poi.name, coords=Coordinates(lat=poi.latitude, lng=poi.longitude)))
        
        search_ids = {}
        ids = [x.id for x in locations]
        for i, id in enumerate(ids):
            search_ids[id] = ids[:i] + ids[(i + 1):]
        
        results = await sdk.time_filter_async(
            locations=locations,
            search_ids=search_ids,
            departure_time=datetime.now(),
            transportation=CyclingPublicTransport(),
            properties=[Property.TRAVEL_TIME]
        )
        
        self.matrix = [[0 for _ in range(len(self.pois))]
                        for _ in range(len(self.pois))]

        names = [x.name for x in self.pois]
        for ind in results:
            i = names.index(ind.search_id)
            for x in ind.locations:
                j = names.index(x.id)
                travel_time = x.properties[0].travel_time
                self.matrix[i][j] = travel_time
                # self.matrix[j][i] = travel_time

    def get_place_ids(self):
        url = 'https://maps.googleapis.com/maps/api/geocode/json'

        for poi in self.pois:
            params = {
                'latlng': f'{poi.latitude}, {poi.longitude}',
                'key': GOOGLE_API_KEY
            }
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                if data['results']:
                    place_id = data['results'][0].get('place_id')
                    # formatted_address = data['results'][0].get('formatted_address')
            self.ids.append(place_id)

    def get_opening_hours(self):
        for id in self.ids:
            url = f'https://places.googleapis.com/v1/places/{id}'
            params = {
                'fields': 'regularOpeningHours',
                'key': GOOGLE_API_KEY
            }
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                if 'regularOpeningHours' in data:
                    periods = data['regularOpeningHours']['periods']
                    self.opening_hours.append(periods)
                else:
                    self.opening_hours.append(None)


    def get_daily_sets(self, num_of_days: int) -> List[List[POI]]:
        included = set()

        result = []

        current = 0
        sum_time = 0
        included.add(current)
        for _ in range(num_of_days):
            daily = []
            while True:
                daily.append(current)
                distances = [x for x in self.matrix[current]]
                for x in included:
                    distances[x] = float('inf')
                next = argmin(distances)

                sum_time += distances[next]
                sum_time += 2 * 60 * 60
                included.add(next)

                current = next
                if sum_time >= 10 * 60 * 60:
                    sum_time = 0
                    break
            result.append(daily)
        
        result_poi = []
        for daily_set in result:
            result_poi.append([self.pois[x] for x in daily_set])
        return result_poi

    def daily_sets_to_json(daily_sets: List[List[POI]]):
        result = []
        for day in daily_sets:
            result.append([poi.to_json() for poi in day])
        return result

# with open('Pathfinding/POIs.json', 'r') as file:
#     data = json.load(file)
# POIs = []
# for entry in data['tourist_attractions']:
#     POIs.append(POI(entry['name'], entry['type'], entry['position']['latitude'], entry['position']['longitude'], entry['tags']))

# print(POIs)
# l = Locations(POIs)
# print(l.get_daily_sets(3))